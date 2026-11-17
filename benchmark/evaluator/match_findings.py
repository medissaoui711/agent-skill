#!/usr/bin/env python3
"""Order-invariant conservative matcher for isolated benchmark evaluation."""
from __future__ import annotations
import argparse
import sys
from typing import Any
from common import (
    deduplicate_findings_detailed, load_json, normalize_findings, write_json,
    _canonical,
)


def _edge_cost(candidate: dict[str, Any], reference: dict[str, Any], tolerance: int,
               localization_weight: int) -> int | None:
    if candidate["file"] != reference["file"] or candidate["category"] != reference["category"]:
        return None
    a, b = candidate.get("line"), reference.get("line")
    if a is None or b is None:
        return localization_weight
    distance = abs(a - b)
    if distance > tolerance:
        return None
    return distance


def _solve(candidates: list[dict[str, Any]], expected: list[dict[str, Any]],
           tolerance: int, localization_weight: int | None = None) -> tuple[int, int, list[tuple[int, int]]]:
    """Successive shortest augmenting paths; returns max flow then min cost."""
    n, m = len(candidates), len(expected)
    if not n or not m:
        return 0, 0, []
    if localization_weight is None:
        localization_weight = min(n, m) * tolerance + 1
    source, candidate_start, expected_start, sink = 0, 1, 1 + n, 1 + n + m
    graph: list[list[list[int]]] = [[] for _ in range(sink + 1)]
    pair_edges: dict[tuple[int, int], list[int]] = {}

    def add_edge(u: int, v: int, capacity: int, cost: int) -> list[int]:
        forward = [v, len(graph[v]), capacity, cost]
        reverse = [u, len(graph[u]), 0, -cost]
        graph[u].append(forward)
        graph[v].append(reverse)
        return forward

    for i in range(n):
        add_edge(source, candidate_start + i, 1, 0)
    for j in range(m):
        add_edge(expected_start + j, sink, 1, 0)
    for i, candidate in enumerate(candidates):
        for j, reference in enumerate(expected):
            cost = _edge_cost(candidate, reference, tolerance, localization_weight)
            if cost is not None:
                pair_edges[(i, j)] = add_edge(candidate_start + i, expected_start + j, 1, cost)

    flow = total_cost = 0
    node_count = len(graph)
    while True:
        infinity = 10**30
        distance = [infinity] * node_count
        previous: list[tuple[int, int] | None] = [None] * node_count
        distance[source] = 0
        # Bellman-Ford handles negative reverse edges without external dependencies.
        for _ in range(node_count - 1):
            changed = False
            for u in range(node_count):
                if distance[u] == infinity:
                    continue
                for edge_index, edge in enumerate(graph[u]):
                    v, _, capacity, cost = edge
                    candidate_distance = distance[u] + cost
                    if capacity and candidate_distance < distance[v]:
                        distance[v] = candidate_distance
                        previous[v] = (u, edge_index)
                        changed = True
            if not changed:
                break
        if previous[sink] is None:
            break
        node = sink
        while node != source:
            u, edge_index = previous[node]  # type: ignore[misc]
            edge = graph[u][edge_index]
            edge[2] -= 1
            graph[node][edge[1]][2] += 1
            node = u
        flow += 1
        total_cost += distance[sink]

    pairs = sorted((i, j) for (i, j), edge in pair_edges.items() if edge[2] == 0)
    return flow, total_cost, pairs


def _objective(candidates: list[dict[str, Any]], expected: list[dict[str, Any]],
               tolerance: int, localization_weight: int | None = None) -> tuple[int, int]:
    flow, cost, _ = _solve(candidates, expected, tolerance, localization_weight)
    return flow, cost


def _forced_edge_objective(candidates: list[dict[str, Any]], expected: list[dict[str, Any]],
                           tolerance: int, candidate_index: int,
                           expected_index: int, localization_weight: int) -> tuple[int, int] | None:
    edge_cost = _edge_cost(candidates[candidate_index], expected[expected_index],
                           tolerance, localization_weight)
    if edge_cost is None:
        return None
    remaining_candidates = candidates[:candidate_index] + candidates[candidate_index + 1:]
    remaining_expected = expected[:expected_index] + expected[expected_index + 1:]
    flow, cost = _objective(remaining_candidates, remaining_expected, tolerance, localization_weight)
    return flow + 1, cost + edge_cost


def match(findings: list[dict[str, Any]], truth_payload: Any, tolerance: int = 3) -> dict[str, Any]:
    if isinstance(tolerance, bool) or not isinstance(tolerance, int) or tolerance < 0:
        raise ValueError("line tolerance must be a non-negative integer.")
    if not isinstance(truth_payload, dict) or not isinstance(truth_payload.get("findings"), list):
        raise ValueError("Ground truth must be an object containing a findings array.")

    candidates_input = normalize_findings(findings)
    expected = normalize_findings(truth_payload)
    unique, duplicate_count, conflict_groups = deduplicate_findings_detailed(candidates_input)
    conflict_signatures = {
        _canonical(variant)
        for group in conflict_groups for variant in group["variants"]
    }
    quarantined = [item for item in unique if _canonical(item) in conflict_signatures]
    active_candidates = [item for item in unique if _canonical(item) not in conflict_signatures]
    expected.sort(key=_canonical)

    localization_weight = min(len(active_candidates), len(expected)) * tolerance + 1
    optimum_flow, optimum_cost, chosen_pairs = _solve(
        active_candidates, expected, tolerance, localization_weight
    )
    possible_by_candidate: dict[int, list[int]] = {}
    for i, candidate in enumerate(active_candidates):
        possible = []
        for j, reference in enumerate(expected):
            forced_objective = _forced_edge_objective(
                active_candidates, expected, tolerance, i, j, localization_weight
            )
            if forced_objective == (optimum_flow, optimum_cost):
                possible.append(j)
        possible_by_candidate[i] = possible

    # A candidate is matched only if it must be matched and has exactly one
    # reference edge across every globally optimal assignment.
    matches: list[dict[str, Any]] = []
    matched_expected_indices: set[int] = set()
    ambiguous: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = list(quarantined)

    for i, candidate in enumerate(active_candidates):
        possible = possible_by_candidate[i]
        without_candidate = active_candidates[:i] + active_candidates[i + 1:]
        candidate_must_be_matched = _objective(
            without_candidate, expected, tolerance, localization_weight
        ) != (
            optimum_flow, optimum_cost
        )
        if len(possible) == 1 and candidate_must_be_matched:
            j = possible[0]
            reference = expected[j]
            a, b = candidate.get("line"), reference.get("line")
            distance = None if a is None or b is None else abs(a - b)
            matches.append({
                "candidate": candidate,
                "expected": reference,
                "severity_exact": candidate["severity"] == reference["severity"],
                "location_within_tolerance": distance is not None and distance <= tolerance,
                "line_distance": distance,
            })
            matched_expected_indices.add(j)
        else:
            unmatched.append(candidate)
            if possible:
                ambiguous.append({
                    "candidate": candidate,
                    "possible_expected": [expected[j] for j in possible],
                    "ambiguity_reason": (
                        "multiple_optimal_references" if len(possible) > 1
                        else "candidate_not_matched_in_every_optimum"
                    ),
                })

    matches.sort(key=lambda item: (_canonical(item["candidate"]), _canonical(item["expected"])))
    unmatched.sort(key=_canonical)
    ambiguous.sort(key=lambda item: _canonical(item["candidate"]))
    false_negatives = [item for i, item in enumerate(expected) if i not in matched_expected_indices]

    localized_pairs = 0
    total_line_distance = 0
    for i, j in chosen_pairs:
        a, b = active_candidates[i].get("line"), expected[j].get("line")
        if a is not None and b is not None:
            localized_pairs += 1
            total_line_distance += abs(a - b)

    return {
        "true_positive_count": len(matches),
        "false_positive_count": len(unmatched) + duplicate_count,
        "false_negative_count": len(false_negatives),
        "duplicate_count": duplicate_count,
        "candidate_count": len(candidates_input),
        "expected_count": len(expected),
        "matches": matches,
        "unmatched_findings": unmatched,
        "false_negatives": false_negatives,
        "ambiguous_findings": ambiguous,
        "conflicting_duplicate_groups": conflict_groups,
        "optimal_assignment": {
            "maximum_cardinality": optimum_flow,
            "localized_pair_count": localized_pairs,
            "total_line_distance": total_line_distance,
            "scored_forced_matches": len(matches),
        },
        "matching_policy": {
            "path_and_category_exact": True,
            "line_tolerance": tolerance,
            "objective_priority": [
                "maximize_cardinality",
                "maximize_localized_pairs",
                "minimize_total_line_distance",
            ],
            "missing_line": "eligible but unlocalized; lower priority than localized edges",
            "ambiguous_matches": "only edges present in every optimal assignment are scored",
            "conflicting_duplicates": "quarantined from matching and reported",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("findings", help="Normalized findings JSON")
    parser.add_argument("ground_truth", help="Private ground-truth JSON; isolated environment only")
    parser.add_argument("output", help="Match result JSON")
    parser.add_argument("--line-tolerance", type=int, default=3)
    args = parser.parse_args()
    if args.line_tolerance < 0:
        parser.error("--line-tolerance must be >= 0")
    try:
        candidates = normalize_findings(load_json(args.findings))
        result = match(candidates, load_json(args.ground_truth), args.line_tolerance)
        write_json(args.output, result)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Matching complete. Independently adjudicate ambiguous and unmatched findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

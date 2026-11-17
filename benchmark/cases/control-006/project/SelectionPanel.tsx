import { useMemo } from "react";

type Props = { selectedIds: readonly string[]; currentId: string };

export function SelectionPanel({ selectedIds, currentId }: Props) {
  const selectedSet = useMemo(() => new Set(selectedIds), [selectedIds]);
  const isSelected = selectedSet.has(currentId);

  return (
    <section>
      <output>{selectedSet.size}</output>
      <span>{isSelected ? "Selected" : "Not selected"}</span>
    </section>
  );
}

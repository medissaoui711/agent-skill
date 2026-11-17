# Performance Review Task — Node.js pricing

## Contract
This function calculates a quote for one request. Pricing rules are immutable for the lifetime of the process and are loaded once at module initialization. A quote can contain many line items. Preserve item order and exact decimal-string output semantics.

## Review scope
Inspect the supplied module. Distinguish a repeatable inefficiency from speculative micro-optimization. Do not assume a particular quote size or CPU profile.

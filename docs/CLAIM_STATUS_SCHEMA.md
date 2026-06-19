# Claim Status Schema

Status: `formal_definition`  
OAK gate: `safe`  
CVCD invariant: `claim_evidence_separation`

## Purpose

Provide a shared evidence language for all Tristan repos.

## Status values

| Status | Meaning | Promotion requirement |
|---|---|---|
| `metaphor_or_vision` | generative direction | define terms |
| `formal_definition` | clear symbols/rules | examples and schema |
| `prototype` | executable artifact exists | tests or dry-run |
| `speculative_fertile` | high-potential unvalidated idea | next measurable action |
| `measured_claim` | empirical claim | data, baseline, uncertainty |
| `proven_theorem` | proof claim | assumptions and proof artifact |
| `negative_memory` | failed/rejected path | residue and next action |

## Required metadata

```yaml
status: prototype
oak_gate: needs_test
cvcd_invariant: example_invariant
source: path-or-provenance
next_action: falsifiable-next-step
```

## OAK gates

- `safe`
- `needs_test`
- `needs_measurement`
- `claim_risk`

## Governance rule

When in doubt, choose the weaker status and stronger OAK gate. The canon can promote claims later; it should not over-promote early.

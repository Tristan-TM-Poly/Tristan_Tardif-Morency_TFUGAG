# OAK Airgap Handoff Template

Status: `formal_definition`  
OAK gate: `safe`  
CVCD invariant: `safe_transfer_of_claims_between_contexts`

## Purpose

Move ideas between chats, repos, documents, and agents without losing status, source, or uncertainty.

## Handoff block

```yaml
handoff_id: OAK-HANDOFF-YYYYMMDD-short-name
source_context: "conversation, repo, file, issue, PR, or experiment"
claim_status: "formal_definition | prototype | speculative_fertile | measured_claim | proven_theorem | negative_memory"
oak_gate: "safe | needs_test | needs_measurement | claim_risk"
cvcd_invariant: "compressed invariant"
assumptions: []
evidence: []
risks: []
next_action: "smallest safe next step"
```

## Rule

A handoff should never strengthen a claim. It can preserve, clarify, split, or downgrade claims until evidence supports promotion.

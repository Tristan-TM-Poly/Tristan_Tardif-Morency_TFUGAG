# Capability targets: local AI council + delivery harness

## Local AI council

Absorbable capability pattern:

- local-first inference;
- self-hosted model experimentation;
- multi-model council / voting;
- private retrieval memory;
- small-model swarm for comparison.

OAK boundary:

- do not copy identity, likeness, voice, branding, private code, or copyrighted media;
- absorb only the architecture pattern.

## AI delivery control loop

Absorbable capability pattern:

- AI-speed code generation requires stronger downstream validation;
- track review load, hidden work, failures, remediation time;
- couple PR, CI, tests, docs, and risk gates;
- use a harness layer around agents to mediate tools, state, resource bounds and execution traces.

## TFUGA adapter plan

```text
external capability -> CapabilityCard -> license/source check -> adapter boundary -> tests -> docs -> draft PR
```

## Concrete next adapters

- `LocalAICouncilAdapter`: compare model outputs and preserve private memory boundaries.
- `DevOpsHarnessAdapter`: enforce PR/CI/OAK gates and track hidden work.
- `AgentHarnessAdapter`: standard interface for tool/state/action mediation.

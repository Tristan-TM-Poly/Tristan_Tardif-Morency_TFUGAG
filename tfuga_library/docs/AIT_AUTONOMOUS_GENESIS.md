# AIT Autonomous Genesis

`AITAutonomousGenesis` is a bounded OAK-gated genesis engine.

## It generates

- proposal seeds;
- module plans;
- action checklists;
- OAK scores;
- Markdown reports;
- draft-PR-ready next steps.

## It does not

- execute high-risk actions automatically;
- bypass repository permissions;
- call external APIs by default;
- mutate GitHub without draft PR / OAK gate.

## OAK invariant

```text
seed -> proposal -> OAK score -> gates -> docs -> tests -> draft PR
```

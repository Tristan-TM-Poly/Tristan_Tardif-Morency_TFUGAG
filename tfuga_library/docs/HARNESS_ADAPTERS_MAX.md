# TFUGA Harness Adapters Max

## Local AI Council Adapter

Compares already-produced model answers using confidence, cost hints, latency hints, and answer density. It is local-first and does not call external APIs.

## Delivery Harness Adapter

Scores hidden work and merge risk from repository delivery signals: changed files, additions, tests, docs, review notes, and CI failures.

## Agent Harness Adapter

Filters proposed actions through a small OAK-style allowlist and risk boundary.

## OAK invariant

```text
external inspiration -> local adapter -> tests -> docs -> draft PR
```

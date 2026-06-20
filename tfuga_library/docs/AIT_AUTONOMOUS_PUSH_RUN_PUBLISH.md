# AIT Autonomous Push Run Publish

`AITAutonomousPushRunPublish` is a dry-run-first OAK planner for push/run/publish workflows.

## Routes

- push: branch -> commit -> draft PR -> review
- run: local checks -> test report -> OAK score
- publish: artifact -> release notes -> review gate

## Default policy

- dry-run default;
- tests required;
- docs required;
- draft PR required for non-run phases;
- external publish disabled unless policy explicitly allows it.

## OAK invariant

```text
request -> phase -> score -> route -> gates -> checklist -> report
```

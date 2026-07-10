# AIT Control Plane Max

`AITControlPlane` unifies TFUGA/OAK modules into a single planning report.

## Inputs

- item name;
- changed files;
- additions;
- tests added;
- docs added;
- optional Quebec research layer.

## Composed layers

- DeliveryHarnessAdapter
- AITRouteSelector
- AITAutonomousPushRunPublish
- AITQuebecResearchAbsorber

## Invariant

```text
analysis -> route -> gates -> local validation -> artifact -> draft PR
```

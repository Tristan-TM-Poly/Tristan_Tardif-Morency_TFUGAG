# Production Availability Runbook

## Scope

Canonical public surface:

- `https://axiome-tristan.com/`
- `https://www.axiome-tristan.com/`
- `https://www.axiome-tristan.com/integrity/usif-bench`
- `https://www.axiome-tristan.com/healthz`

## Availability invariant

A production domain must remain attached to the last known-good READY deployment until a replacement deployment is READY and promoted.

Do **not** intentionally detach `axiome-tristan.com` or `www.axiome-tristan.com` as an intermediate deployment step. Build first, verify the candidate, then let Vercel perform the production promotion/alias transition.

## Automated OAK gate

`.github/workflows/production-availability-oak.yml` runs:

1. after production-relevant changes reach `main`;
2. every 15 minutes;
3. on manual dispatch.

It checks the apex domain, the `www` domain, USIF-Bench and the static health endpoint with bounded retries. A probe must return HTTP 200 after redirects and contain an expected semantic marker; status alone is insufficient.

On failure, the workflow opens or updates one GitHub availability incident. On verified recovery, it comments on and closes the open incident automatically.

## Deployment sequence

1. Change code on a non-production branch.
2. Review and merge only after repository checks pass.
3. Allow Vercel to build the production deployment from `main`.
4. Wait for the production smoke gate to pass.
5. If the smoke gate fails, inspect Vercel deployment state/build/runtime logs before further production mutations.
6. Keep the previous known-good deployment/domain mapping in place while diagnosing.

## OAK incident rules

During an outage:

- availability evidence overrides assumptions;
- do not claim the site is healthy until probes pass;
- do not strengthen scientific or commercial claims merely to compensate for an operational failure;
- prefer rollback/recovery over unrelated feature additions;
- preserve the failed run URL and deployment identifiers as evidence;
- record the failure mode as negative memory if it reveals a reusable deployment hazard.

## Health endpoint contract

`/healthz` is deliberately static and minimal. It proves that the public Vercel origin and routing path are serving the deployed artifact. It is not a claim that every external dependency or application feature is healthy.

Expected body marker:

```text
status=ok
```

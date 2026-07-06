# OAKShield Core OAK Policy

## 1. Authorization first

No review starts without a clear owner, scope, excluded assets, and allowed check types.

## 2. Documentation-first core

This core pack documents review rules and templates only. It does not perform network activity, active probing, or external interaction.

## 3. Sanitized observations

Observations must not contain secrets, personal data, tokens, private keys, or confidential client material.

## 4. M-minus memory

A repeated weakness becomes useful only when it creates a prevention rule or regression check.

## 5. Workflow changes are sensitive

Any future `.github/workflows/**` change must be reviewed separately because it changes the repository execution boundary.

## 6. Close criteria

An observation is closed only when remediation is implemented, a regression check exists, retained risk is documented, and validation passes.

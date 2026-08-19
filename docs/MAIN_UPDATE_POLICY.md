# TFUGAG Main Update Policy

## Purpose

Main must remain the stable canon branch. Automated systems may prepare update proposals toward main, but they must not bypass review.

## Allowed path

```text
working branch
  -> review bundle
  -> pull request
  -> tests and OAK review
  -> merge to main
```

## Forbidden path

```text
generated output
  -> direct main mutation
```

## Automatic update rule

An automatic update system may:

- detect that a branch is ready for review;
- generate a main update packet;
- summarize changed modules;
- list risks, missing tests, and required review gates;
- prepare the content needed for a Pull Request.

It must not:

- push directly to main;
- merge its own PR;
- disable tests;
- hide risk flags;
- promote claims to canon without evidence.

## Required review gates

Before any merge into main:

1. New modules must be listed.
2. New claims must be classified.
3. Tests or manual review notes must exist.
4. OAK risk flags must be reviewed.
5. Contradictions must be quarantined or resolved.
6. The update must have a clear rollback path.

## Main update packet schema

```yaml
source_branch:
target_branch: main
summary:
changed_modules:
review_gates:
risk_flags:
rollback_path:
recommendation: hold | ready_for_review | ready_to_merge
```

## Principle

Automatic preparation is allowed. Automatic canon mutation is not.

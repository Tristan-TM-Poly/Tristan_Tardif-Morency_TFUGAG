# OAK Air-Gap Protocol

## Purpose

This protocol defines how AI-generated TFUGA material may cross from a private generation space into a public repository without becoming uncontrolled publication, spam, or unsupported scientific claim.

The Air-Gap is not a mystical threshold. It is a review layer.

```text
AI generation
  -> local or connector-controlled proposal
  -> DCT-Omega packet
  -> OAK validation
  -> pull request
  -> human review
  -> merge or reject
```

## Non-negotiable rules

1. No direct autonomous publication to external journals, patent offices, social networks, or mass-posting channels.
2. No claim may be promoted as demonstrated unless it has a reproducible proof, calculation, simulation, or test.
3. All generated artifacts must expose assumptions, limits, risk, and validation status.
4. Pull requests are the only default crossing mechanism.
5. Human review remains the final authority for merge, release, and public claims.

## Artifact status labels

- `S`: speculative
- `E`: exploratory
- `X`: crystallizable
- `D`: locally demonstrated
- `C`: canonical
- `A`: archived

## Promotion gate

An artifact may move forward only if it answers:

- What is being claimed?
- What is the minimal definition?
- What assumptions are required?
- What would falsify it?
- What test, proof, or benchmark exists?
- What risk exists if published?
- What is the next smallest useful action?

## Default GitHub workflow

1. Generate material into a branch.
2. Create or update a DCT-Omega packet.
3. Add tests or examples when code is involved.
4. Open a pull request.
5. Review claim status before merge.

## OAK rejection conditions

Reject or archive material when it:

- claims universal proof without derivation;
- confuses metaphor with demonstrated mechanism;
- duplicates existing content without compression;
- proposes spam, saturation, or abusive automation;
- contains secrets, credentials, private data, or unsafe instructions;
- lacks a falsifiable next step.

## Minimal safe automation target

The first safe autonomous loop is:

```text
Generate one bounded artifact
  -> classify it
  -> save it to a branch
  -> open a PR
  -> wait for review
```

Everything beyond this should be added only after measurable reliability is shown.

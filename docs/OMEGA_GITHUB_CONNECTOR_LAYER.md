# TFUGAG Omega GitHub Connector Layer

## Purpose

Transform GitHub from a file repository into an epistemic memory substrate for TFUGAG.

Git remains the persistence layer. Pull requests become review events. Commits become evolution events. Branches become exploration spaces. Merges become canon promotion decisions.

## Core Mapping

| GitHub Object | Omega Meaning |
|---|---|
| Repository | Epistemic memory space |
| Branch | Exploration trajectory |
| Commit | Evolution event |
| Pull Request | Review packet |
| Issue | Frontier, question, defect, or protocol candidate |
| Label | Governance state |
| Tag | Canonical milestone |
| Release | Stable atlas snapshot |

## Recommended Branch Model

```text
main                 -> stable canon
frontier/*           -> exploratory questions and gaps
bridge/*             -> bridge candidates
protocol/*           -> protocol candidates
quarantine/*         -> contradictions and OAK review
atlas/*              -> view and documentation updates
agent/*              -> generated review proposals
```

## Recommended Directory Model

```text
docs/claims/         -> canonical and candidate claims
docs/evidence/       -> evidence records and source summaries
docs/questions/      -> generated research questions
docs/protocols/      -> protocol candidates
docs/frontiers/      -> frontier packets
docs/atlas/          -> navigable atlas views
docs/evolution/      -> temporal mutation records
docs/governance/     -> rules, policies, validation packets
```

## Review Flow

```text
OmegaSignal
  -> OmegaFrontier
  -> OmegaQuestion
  -> OmegaResearchCandidate
  -> OmegaProtocolCandidate
  -> Pull Request
  -> Review
  -> Merge or Quarantine
  -> OmegaEvolutionEvent
```

## Connector Capabilities Needed

### 1. Semantic Search Adapter

Find related claims, evidence, protocols, and atlas views from a concept query.

### 2. Omega Neighborhood Adapter

Given a node identifier, retrieve nearby files, PRs, commits, issues, and review packets.

### 3. Evolution Diff Adapter

Compare two branches or tags and produce:

```text
new claims
changed claims
resolved contradictions
opened frontiers
closed frontiers
new protocols
archived nodes
```

### 4. Batch Proposal Adapter

Create many reviewable files in one branch while preserving a single PR-level audit trail.

### 5. Canon Promotion Adapter

Prepare promotion packets from PR metadata, tests, evidence, contradiction status, and governance review.

## Safety Rule

The connector may prepare, classify, and propose.

It must not silently mutate main.

```text
Allowed:
- create branch
- create review files
- open PR
- summarize risk
- attach evidence
- generate review packet

Forbidden:
- direct main mutation
- self-merge without review
- hiding failed checks
- promoting claims without evidence
```

## Long-Term Goal

GitHub becomes the versioned substrate of the TFUGAG OmegaGraph.

```text
Git = memory
Branch = exploration
Commit = mutation
PR = review
Merge = promotion
Tag = invariant
Release = atlas snapshot
```

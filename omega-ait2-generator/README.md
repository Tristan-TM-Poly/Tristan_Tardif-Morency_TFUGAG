# Omega-SAGE-AIT2 Generator

**Omega-SAGE-AIT2 Generator** is a minimal, testable research kernel for generating AITs: *Architectural / Augmented / Agentic Intelligences Transformatives* that combine mission design, HGFM mapping, CVCD scoring, OAK validation, residue tracking, and executable prototyping.

This package is intentionally conservative: it does not claim autonomous scientific discovery. It provides a reproducible scaffold for turning fertile theory into explicit specifications, tests, traces, and next actions.

## Core loop

```text
Goal
  -> AITSpec
  -> HGFM map
  -> CVCD+ score
  -> OAK report
  -> AIT runtime packet
  -> residue memory
  -> next generation
```

## Canonical equation

```text
AIT_{t+1} = EXP(OAK(CVCD(LOG(HGFM(TGNT(JKD(AIT_t)))))))
```

In code, this becomes a deterministic pipeline with auditable intermediate objects.

## Repository layout

```text
omega-ait2-generator/
  src/ait2/              Python package
  agents/                YAML genomes for canonical AITs
  docs/                  theory and operating contract
  tests/                 pytest verification tests
```

## Quick start

```bash
python -m ait2.cli "generate prime conjecture agents"
```

## OAK maturity levels

| Status | Meaning |
|---:|---|
| 0 | Brume: vague idea |
| 1 | Forme: minimally defined |
| 2 | Testable: has checks or experiments |
| 3 | Prototype: executable artifact |
| 4 | Robust: stress-tested |
| 5 | Canonical: stable and reusable |

## Design rule

> Every strong claim must become either a proof, test, prototype, counterexample search, or residue.

This keeps the Tristan TFUGA / HGFM ecosystem ambitious but grounded.

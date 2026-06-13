# Omega-SAGE-AIT2 Theory Contract

## Definition

`Omega-SAGE-AIT2` is a meta-generator that converts goals into specialized AIT packets:

```text
Goal -> AITSpec -> HGFM -> CVCD+ -> OAK -> AITPacket -> ResidueMemory
```

An AIT packet is not assumed true because it is generated. It is a candidate operational intelligence that must expose inputs, outputs, validators, traces, and residues.

## Tensor view

```text
AIT_i ∈ T_mission ⊗ T_knowledge ⊗ T_proof ⊗ T_action ⊗ T_yield ⊗ T_residue
```

This means an AIT is not merely a prompt. It is a structured factorization of mission, knowledge, validation, action, yield, and failure modes.

## HGFM view

The HGFM map stores concepts as nodes and relations as hyperedges. This first implementation is intentionally lightweight so it can be tested, extended, and replaced by richer graph engines later.

## CVCD+ score

CVCD+ estimates:

- coherence;
- value;
- compression;
- density;
- proofability;
- yield potential;
- residue/error pressure.

The score is a triage signal, not a proof.

## OAK validation

OAK turns every generated object into:

- strengths;
- weaknesses;
- tests;
- residues;
- next actions;
- maturity status.

## Negative memory

Failures are first-class artifacts. Every contradiction, vague assumption, failed proof, or missing test becomes future fuel.

## Anti-hallucination rule

No claim is promoted to canonical status without an auditable path through tests, proofs, benchmarks, or explicit limitations.

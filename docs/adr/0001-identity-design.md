# ADR-0001 — Separate source identifiers from mastered identities
Status: Accepted for demonstration (not production endorsed)

## Context
CRM and loyalty assign different identifiers to customers. Joining directly on source IDs is invalid. Email-only matching introduces false merge and reassignment risks.

## Decision
Export an explicit source-to-master crosswalk. In phase 1, exact normalized email grouping generates deterministic demo IDs solely for repeatability.

## Alternatives
1. Treat email as primary key — rejected for enterprise use: mutable/shared/reassigned.
2. Use name only — rejected: collisions and noisy spellings.
3. Use full probabilistic entity resolution now — deferred until labeled matching data, quality scoring and human review exist.

## Consequences
Simple, reproducible local prototype but not an enterprise-safe identity engine. Future work must use immutable surrogate IDs, crosswalk history, confidence thresholds, override/unmerge and audited stewardship.

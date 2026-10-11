# ADR-0002 — Transparent attribute survivorship
Status: Accepted for demonstration

## Context
Multiple source records may disagree on the display name.

## Decision
Prefer CRM name if present; otherwise use the latest updated source record. Keep `survivor_source` for visibility.

## Trade-offs
This is deterministic and testable but source priority is attribute-specific in real MDM. A production design requires verification status, field-by-field trust scores, effective dates, manual overrides, and history.

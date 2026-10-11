# Architecture requirements — hypothetical Customer 360 case study

## Business outcomes
- Unified customer view across independently keyed source systems.
- Trusted source-to-master lineage and explainable survivorship.
- Rejection visibility for malformed records.

## Functional requirements
- Import synthetic CSV source feeds.
- Validate required fields and email format.
- Resolve matching normalized emails to one master identity (phase 1 only).
- Track source identifiers and surviving attribute provenance.
- Produce quality metrics, customer master, and crosswalk exports.

## Non-functional targets — proposed, not validated
- Idempotent reruns with stable master IDs for unchanged normalized email.
- Deterministic, testable outputs; no production data.
- Future scalability to incremental Spark/Delta pipeline.
- Future governance: access policies, audit log, monitoring, unmerge workflow.

## Explicit limitations
- Email equality cannot establish identity in all cases: shared accounts and email reassignment exist.
- The phase 1 prototype does not satisfy enterprise privacy/compliance requirements.
- No performance or accuracy SLA is claimed.

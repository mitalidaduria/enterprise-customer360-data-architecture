# Interview story — adapted from independently reproducible demonstration

**Situation:** Multiple domains represent the same conceptual customer using different IDs and naming conventions.

**Task:** Define an architecture that creates a traceable customer representation without tying enterprise identity to one source system.

**Action:** Created canonical schemas and STTM; separated master ID and source crosswalk; implemented validation gates, normalized matching, survivorship, lineage exports, tests, and two architecture decision records.

**Result:** Phase-1 synthetic fixture demonstrates six input rows, five accepted rows, four master identities, and a machine-readable rejected-record report. These numbers describe *only the demo dataset* and make no statement about employer impact.

**What I would change for production:** immutable surrogate IDs, probabilistic match score calibration, steward queue and unmerge, reliable incremental ingestion, Delta Lake, security, lineage and monitoring.

**Challenge:** Why exact email matching when email is a flawed identifier? **Answer:** This is a deliberately constrained teaching baseline; the ADR and roadmap reject it as a production-safe matching approach. The architecture decouples crosswalk and master concepts so the matcher can be replaced.

# Phased portfolio roadmap

| Phase | Proof | Deliverables | Completion gate |
|---|---|---|---|
| 1 — local architecture | model and correctness | README, Mermaid diagrams, STTM, ADRs, code, tests, DQ report | clean local run and automated tests |
| 2 — enterprise modeling | deeper MDM | conceptual/logical/physical models, SCD2, match-review queue, steward override | test false merge, reassignment and unmerge scenarios |
| 3 — lakehouse | distributed engineering | synthetic 5-source generator, PySpark Bronze/Silver/Gold, Delta MERGE, incremental and replay tests | rerun idempotently and explain Spark plan |
| 4 — platform hardening | operations and governance | CI, quality checks, lineage, telemetry dashboard, permissions threat model | demonstrate failures, recovery, observable SLOs |
| 5 — AI enrichment | guarded applied AI | embedding-based candidate matching, review thresholds, evaluation report, optional grounded LLM summary | labeled eval set and precision/recall reporting |
| 6 — recruiter presentation | business and decision narrative | 2-minute walkthrough, public demo, decision matrix, cost model, results | independent reviewer can reproduce all claims |

Do not claim a phase is complete until code and evidence support it.

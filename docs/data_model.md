# Logical data model

**Grain:** `customer_master` has one row per phase-1 resolved normalized email. `source_crosswalk` has one row per accepted source customer record.

```mermaid
erDiagram
  CUSTOMER_MASTER ||--o{ SOURCE_CROSSWALK : links
  CUSTOMER_MASTER {
    string master_customer_id PK
    string full_name
    string email
    string survivor_source
    int linked_records
  }
  SOURCE_CROSSWALK {
    string master_customer_id FK
    string source_system
    string source_customer_id
  }
```

**Business key of crosswalk:** `(source_system, source_customer_id)`.

**Important caveat:** master ID uses SHA-256 of normalized email in this demo. This is deterministic for reruns, but is **not** suitable as a production enterprise ID because changing/reassigned emails would change or conflate identities. Production proposal: immutable generated surrogate IDs and an independent, auditable matching history.

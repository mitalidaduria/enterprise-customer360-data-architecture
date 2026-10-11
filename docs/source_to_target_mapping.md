# Source-to-target mapping (STTM)

| Source | Source field | Target | Rule |
|---|---|---|---|
| CRM, Loyalty | `source_customer_id` | crosswalk.source_customer_id | trim; reject missing |
| CRM, Loyalty | source name | master.full_name | trim; prefer CRM record, else latest updated |
| CRM, Loyalty | `email` | master.email | lower and trim; reject invalid structure |
| CRM, Loyalty | source system label | crosswalk.source_system | preserve source lineage |
| derived | normalized email | master.master_customer_id | deterministic demo hash, see limitations |
| derived | count of crosswalk rows | master.linked_records | count per resolved email |

## Quality gates
1. Structural: expected column names.
2. Record-level: nonempty ID and name, basic email structure.
3. Identity: normalized email grouping (conservative demo; not a validated production match engine).

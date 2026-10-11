"""Local-first, conservative Customer 360 reference pipeline; synthetic data only."""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = {"source_customer_id", "full_name", "email", "phone", "updated_at"}


def normalize_email(email: str) -> str:
    return email.strip().lower()


def load_sources(paths: dict[str, Path]) -> tuple[list[dict], list[dict]]:
    valid, rejected = [], []
    for source, path in paths.items():
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if not REQUIRED.issubset(set(reader.fieldnames or [])):
                raise ValueError(f"Missing required fields in {source}")
            for line, row in enumerate(reader, start=2):
                record = {key: (row.get(key) or "").strip() for key in REQUIRED}
                record["source_system"] = source
                record["source_row"] = line
                record["email_normalized"] = normalize_email(record["email"])
                if not record["source_customer_id"] or not record["full_name"]:
                    rejected.append({"source_system": source, "source_row": line, "reason": "missing required identity/name"})
                elif "@" not in record["email_normalized"] or "." not in record["email_normalized"].split("@")[-1]:
                    rejected.append({"source_system": source, "source_row": line, "reason": "invalid email"})
                else:
                    valid.append(record)
    return valid, rejected


def build_customers(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Match only unique emails across records; all repeated emails are grouped.

    This deliberately small demo assumes each normalized email maps to one identity;
    shared emails are an explicitly documented limitation.
    """
    groups: dict[str, list[dict]] = {}
    for row in records:
        groups.setdefault(row["email_normalized"], []).append(row)
    masters, xref = [], []
    for email in sorted(groups):
        rows = groups[email]
        master_id = "MC-" + hashlib.sha256(email.encode()).hexdigest()[:12].upper()
        # Demonstration rule: prefer CRM for display name; fall back to most recently updated.
        chosen = sorted(rows, key=lambda r: (r["source_system"] == "CRM", r["updated_at"]), reverse=True)[0]
        masters.append({"master_customer_id": master_id, "full_name": chosen["full_name"],
                        "email": email, "survivor_source": chosen["source_system"], "linked_records": len(rows)})
        for row in rows:
            xref.append({"master_customer_id": master_id, "source_system": row["source_system"],
                         "source_customer_id": row["source_customer_id"]})
    return masters, xref


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path = ROOT) -> dict:
    paths = {"CRM": root / "data/sample/crm.csv", "LOYALTY": root / "data/sample/loyalty.csv"}
    valid, rejected = load_sources(paths)
    masters, xref = build_customers(valid)
    out = root / "output"
    write_csv(out / "customer_master.csv", masters, ["master_customer_id", "full_name", "email", "survivor_source", "linked_records"])
    write_csv(out / "source_crosswalk.csv", xref, ["master_customer_id", "source_system", "source_customer_id"])
    report = {"input_rows": len(valid) + len(rejected), "accepted_rows": len(valid), "rejected_rows": len(rejected),
              "master_records": len(masters), "source_links": len(xref), "rejections": rejected,
              "source_counts": dict(Counter(r["source_system"] for r in valid))}
    (out / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

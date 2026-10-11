from customer360.pipeline import build_customers, load_sources, normalize_email, run
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_email_canonicalization():
    assert normalize_email(" Asha.Rao@EXAMPLE.TEST ") == "asha.rao@example.test"

def test_duplicate_source_records_map_to_one_master():
    rows = [
        {"email_normalized": "one@example.test", "source_system": "CRM", "updated_at": "2026-01-01", "full_name": "One" , "source_customer_id": "1"},
        {"email_normalized": "one@example.test", "source_system": "LOYALTY", "updated_at": "2026-02-01", "full_name": "One Alias", "source_customer_id": "2"},
    ]
    masters, xref = build_customers(rows)
    assert len(masters) == 1 and len(xref) == 2
    assert masters[0]["full_name"] == "One"

def test_invalid_email_rejected():
    valid, rejected = load_sources({"CRM": ROOT / "data/sample/crm.csv", "LOYALTY": ROOT / "data/sample/loyalty.csv"})
    assert len(valid) == 5
    assert len(rejected) == 1

def test_end_to_end(tmp_path):
    import shutil
    (tmp_path / "data/sample").mkdir(parents=True)
    for name in ("crm.csv", "loyalty.csv"):
        shutil.copy(ROOT / "data/sample" / name, tmp_path / "data/sample" / name)
    report = run(tmp_path)
    assert report["input_rows"] == 6
    assert report["master_records"] == 4
    assert (tmp_path / "output/customer_master.csv").exists()
    assert (tmp_path / "output/source_crosswalk.csv").exists()

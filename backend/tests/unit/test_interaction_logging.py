import os
import json

import sss.zero_system as zs


def test_interact_creates_log_file(tmp_path):
    log_file = tmp_path / "log.jsonl"
    system = zs.ZeroSystem(log_filename=str(log_file))
    system.interact("اختبار التسجيل")
    assert log_file.exists()
    with open(log_file, encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 1
    entry = json.loads(lines[-1])
    assert entry["message"] == "اختبار التسجيل"
    assert "response" in entry

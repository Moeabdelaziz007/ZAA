import os
import json
 codex/remove-conflict-markers-and-refactor-tests
import tempfile
import unittest

from sss.zero_system import ZeroSystem


class TestInteractionLogging(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.temp_dir.name, "log.jsonl")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_interact_creates_log_file(self):
        system = ZeroSystem(log_filename=self.log_file)
        system.interact("اختبار التسجيل")
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, encoding="utf-8") as f:
            lines = f.readlines()
        self.assertGreaterEqual(len(lines), 1)
        entry = json.loads(lines[-1])
        self.assertEqual(entry["message"], "اختبار التسجيل")
        self.assertIn("response", entry)


if __name__ == "__main__":
    unittest.main()
=======
import pytest
import sss.zero_system as zs

LOG_PATH = os.path.join(os.path.dirname(zs.__file__), "log.jsonl")
MOOD_PATH = os.path.join(os.path.dirname(zs.__file__), "mood.jsonl")

@pytest.fixture(autouse=True)
def cleanup_logs():
    for path in (LOG_PATH, MOOD_PATH):
        if os.path.exists(path):
            os.remove(path)
    yield
    for path in (LOG_PATH, MOOD_PATH):
        if os.path.exists(path):
            os.remove(path)

def test_interact_creates_log_file():
    system = zs.ZeroSystem()
    system.interact("اختبار التسجيل")
    assert os.path.exists(LOG_PATH)
    with open(LOG_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 1
    entry = json.loads(lines[-1])
    assert entry["message"] == "اختبار التسجيل"
    assert "response" in entry

def test_interact_logs_mood():
    system = zs.ZeroSystem()
    system.interact("مرحبا")
    assert os.path.exists(MOOD_PATH)
    with open(MOOD_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 1
    entry = json.loads(lines[-1])
    assert "mood" in entry
 main

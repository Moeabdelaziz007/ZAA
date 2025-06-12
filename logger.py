import json
import os
from datetime import datetime

class ZeroSystemLogger:
    """Minimal logger used for tests."""

    def __init__(self, filename="mood.jsonl"):
        self.filename = filename

    def log_mood(self, mood):
        path = self.filename if os.path.isabs(self.filename) else os.path.join(os.path.dirname(__file__), self.filename)
        entry = {"time": datetime.now().isoformat(), "mood": mood}
        with open(path, "a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

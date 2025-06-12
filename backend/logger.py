import json
import logging
import os
from datetime import datetime
from typing import Optional


class ZeroSystemLogger:
    """Simple logger for ZeroSystem events."""

    def __init__(self, log_file: str = "zero_system.log"):
        self.log_file = log_file
        self._logger = logging.getLogger("ZeroSystemLogger")
        if not self._logger.handlers:
            handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def log_event(
        self,
        message: str,
        skill: Optional[str] = None,
        mood: Optional[str] = None,
        voice_style: Optional[str] = None,
        response: Optional[str] = None,
    ) -> None:
        """Write a structured interaction event to the log file."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "skill": skill,
            "mood": mood,
            "voice_style": voice_style,
            "response": response,
        }
        self._logger.info(json.dumps(data, ensure_ascii=False))

    def log_mood(self, mood: str) -> None:
        """Append the mood value to ``mood.jsonl`` as a JSON line."""
        path = os.path.join(os.path.dirname(__file__), "mood.jsonl")
        entry = {"time": datetime.now().isoformat(), "mood": mood}
        with open(path, "a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")

import os
import json

import sss.zero_system as zs
import logger

LOG_PATH = os.path.join(os.path.dirname(zs.__file__), "log.jsonl")
MOOD_PATH = os.path.join(os.path.dirname(logger.__file__), "mood.jsonl")


def cleanup():
    for path in (LOG_PATH, MOOD_PATH):
        if os.path.exists(path):
            os.remove(path)


def test_mood_history_and_logging():
    cleanup()
    system = zs.ZeroSystem()
    system.interact("صوت لدي سؤال تقني حول البرمجة")
    system.interact("مرحبا")

    assert os.path.exists(LOG_PATH)
    with open(LOG_PATH, encoding="utf-8") as f:
        log_lines = f.readlines()
    assert len(log_lines) >= 2

    assert os.path.exists(MOOD_PATH)
    with open(MOOD_PATH, encoding="utf-8") as f:
        mood_lines = f.readlines()
    assert len(mood_lines) >= 2
    cleanup()

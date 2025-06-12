import json
import os

import sss.zero_system as zs

LOG_PATH = os.path.join(os.path.dirname(zs.__file__), "log.jsonl")
MOOD_PATH = os.path.join(os.path.dirname(zs.__file__), "mood.jsonl")
EVENT_LOG = os.path.join(os.getcwd(), "zero_system.log")


def cleanup():
    for path in (LOG_PATH, MOOD_PATH, EVENT_LOG):
        if os.path.exists(path):
            os.remove(path)


def test_mood_history_and_logging():
    cleanup()
    system = zs.ZeroSystem()
    # trigger mindful embodiment to change mood
    system.interact("صوت لدي سؤال تقني حول البرمجة")
    assert system.brother_ai.mood == "professional"
    # mood history should contain initial and new mood
    assert system.brother_ai.get_mood_history(2) == ["متحمس", "professional"]

    # interact with a message that doesn't change mood
    system.interact("مرحبا")
    # history length unchanged
    assert system.brother_ai.get_mood_history(2) == ["متحمس", "professional"]

    with open(EVENT_LOG, encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 2
    last_entry = json.loads(lines[-1].split(" - ", 1)[-1])
    assert last_entry["mood"] == system.brother_ai.mood
    cleanup()

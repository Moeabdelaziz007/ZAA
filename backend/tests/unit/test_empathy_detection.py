import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from zero_system import EmpathySensorSkill


def test_empathy_detection():
    skill = EmpathySensorSkill()
    assert skill.execute("أشعر بالقلق")["empathy"] == "قلق"
    assert skill.execute("أنا سعيد اليوم")["empathy"] == "سعادة"
    assert skill.execute("مرحباً")["empathy"] == "محايد"

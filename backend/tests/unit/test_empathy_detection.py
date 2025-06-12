from sss.zero_system import EmpathySensorSkill


def test_empathy_detection():
    skill = EmpathySensorSkill()
    assert skill.execute("أشعر بالقلق")["empathy"] == "قلق"
    assert skill.execute("أنا سعيد اليوم")["empathy"] == "سعادة"
    assert skill.execute("مرحباً")["empathy"] == "محايد"

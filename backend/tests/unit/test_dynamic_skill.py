from sss.zero_system import ZeroSystem


def test_dynamic_skill_registration():
    system = ZeroSystem()
    message = system.brother_ai.grow("test_skill")
    assert message == "تم تطوير مهارة جديدة: test_skill"
    assert "test_skill" in system.brother_ai.skills

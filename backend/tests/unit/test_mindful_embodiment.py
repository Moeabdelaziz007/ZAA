from sss.zero_system import MindfulEmbodimentSkill


def test_support_context():
    skill = MindfulEmbodimentSkill()
    result = skill.execute("انا احتاج دعم عاجل")
    assert result["mood"] == "caring"
    assert result["voice_style"] == "صوت دافئ ومتعاطف"

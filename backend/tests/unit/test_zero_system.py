import io
import contextlib
import logging
from sss.zero_system import ZeroSystem, is_sibling_request


def test_is_sibling_request_true():
    assert is_sibling_request("اريد اخ صغير يساعدني")


def test_is_sibling_request_false():
    assert not is_sibling_request("مرحبا كيف الحال؟")


def test_create_sibling_increments_count():
    system = ZeroSystem()
    skill = system.skills["sibling_genesis"]
    before = skill.siblings_created
    system.create_sibling()
    assert skill.siblings_created == before + 1


def test_interact_sibling(caplog):
    system = ZeroSystem()
    buf = io.StringIO()
    with caplog.at_level(logging.INFO), contextlib.redirect_stdout(buf):
        response = system.interact("أريد أخاً صغيراً")
    captured = buf.getvalue()
    assert "المستخدم: أريد أخاً صغيراً" in captured
    assert response["sibling_id"] == "أخ رقمي #1"
    assert "Triggering sibling_genesis skill" in "\n".join(caplog.messages)

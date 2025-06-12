import logging
from sss.zero_system import is_sibling_request, ZeroSystem

def test_is_sibling_request_true():
    assert is_sibling_request("اريد اخ صغير يساعدني")

def test_is_sibling_request_false():
    assert not is_sibling_request("اريد صديق جديد")

def test_interact_logs_and_output(caplog):
    system = ZeroSystem()
    message = "مرحبا"
    user = {"id": "u", "name": "Test"}
    with caplog.at_level(logging.INFO):
        response = system.interact(message, user)
    assert response["status"] == "success"
    assert "AI response" in caplog.text

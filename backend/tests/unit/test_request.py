  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
  import io
  import contextlib
  import logging

  from sss.zero_system import ZeroSystem, is_sibling_request
  =======
  import logging
  from sss.zero_system import is_sibling_request, ZeroSystem

  >>>>>>> main

  def test_is_sibling_request_true():
      assert is_sibling_request("اريد اخ صغير يساعدني")

  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
  def test_is_sibling_request_true():
      assert is_sibling_request("اريد اخ صغير يساعدني")


  def test_is_sibling_request_false():
      assert not is_sibling_request("اريد صديق جديد")


  =======

  def test_is_sibling_request_false():
      assert not is_sibling_request("اريد صديق جديد")


  >>>>>>> main
  def test_interact_logs_and_output(caplog):
      system = ZeroSystem()
      message = "مرحبا"
      user = {"id": "u", "name": "Test"}
  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
      buf = io.StringIO()
      with caplog.at_level(logging.INFO), contextlib.redirect_stdout(buf):
          response = system.interact(message, user)
      captured = buf.getvalue()
      assert "المستخدم: مرحبا" in captured
      assert "الذكاء:" in captured
      assert response["status"] == "success"
      log_text = "\n".join(caplog.messages)
      assert f"User message: {message}" in log_text
      assert any("AI response" in m for m in caplog.messages)
  =======
      with caplog.at_level(logging.INFO):
          response = system.interact(message, user)
      assert response["status"] == "success"
      assert "AI response" in caplog.text
  >>>>>>> main

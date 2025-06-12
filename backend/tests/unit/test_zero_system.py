from sss.zero_system import ZeroSystem, is_sibling_request


def test_is_sibling_request_true():
    assert is_sibling_request("اريد اخ صغير يساعدني")


def test_create_sibling_increments_count():
    system = ZeroSystem()
    before = system.skills["sibling_genesis"].siblings_created
    system.create_sibling()
    after = system.skills["sibling_genesis"].siblings_created
    assert after == before + 1

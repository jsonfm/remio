from remio.network import get_ipv4


def test_get_ipv4():
    """Test for get_ipv4 method."""
    ipv4 = get_ipv4()
    assert type(ipv4) == list, "IPv4 should be a list"
    assert "127.0.0.1" not in ipv4, "localhost should not be included in IPv4"

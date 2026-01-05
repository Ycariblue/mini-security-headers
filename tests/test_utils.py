from scanner.utils import normalize_url

def test_normalize_url_with_scheme():
    assert normalize_url("http://example.com") == "http://example.com"
    assert normalize_url("https://example.com") == "https://example.com"

def test_normalize_url_without_scheme():
    assert normalize_url("example.com") == "https://example.com"

def test_normalize_url_with_slashes():
    assert normalize_url("//example.com") == "https://example.com"

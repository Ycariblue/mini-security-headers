from scanner.headers_checks import check_headers

def test_check_headers_missing():
    headers = {}
    results = check_headers(headers)
    for res in results:
        assert res.present is False
        assert res.status == "missing"

def test_check_headers_ok():
    headers = {
        "Strict-Transport-Security": "max-age=31536000",
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer"
    }
    results = check_headers(headers)
    for res in results:
        assert res.present is True
        assert res.status == "ok"

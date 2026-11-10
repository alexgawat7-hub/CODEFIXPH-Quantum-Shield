import unittest
from unittest.mock import patch
from quantum_scanner import ScanError, _validate_target


class TargetValidationTests(unittest.TestCase):
    def test_adds_https_when_scheme_is_missing(self):
        with patch("quantum_scanner.socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))]):
            self.assertEqual(_validate_target("example.com"), "https://example.com")

    def test_rejects_localhost(self):
        with self.assertRaises(ScanError):
            _validate_target("http://localhost:5000")

    def test_rejects_private_ip(self):
        with self.assertRaises(ScanError):
            _validate_target("http://127.0.0.1")

    def test_rejects_non_http_scheme(self):
        with self.assertRaises(ScanError):
            _validate_target("ftp://example.com")

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ScanError):
            _validate_target("https://user:pass@example.com")

    def test_rejects_domain_resolving_to_private_ip(self):
        with patch("quantum_scanner.socket.getaddrinfo", return_value=[(2, 1, 6, "", ("10.0.0.5", 443))]):
            with self.assertRaises(ScanError):
                _validate_target("https://internal.example")


if __name__ == "__main__":
    unittest.main()

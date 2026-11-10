"""Safe, lightweight HTTP security posture checks for explicitly authorized public websites.

This is not a penetration tester. It makes one bounded GET request, does not follow
redirects, does not submit forms, and never attempts exploitation.
"""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import requests


class ScanError(ValueError):
    pass


def _validate_target(raw_url: str) -> str:
    if not isinstance(raw_url, str) or len(raw_url) > 2048:
        raise ScanError("Enter a valid URL (maximum 2,048 characters).")
    value = raw_url.strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ScanError("Only valid HTTP or HTTPS URLs are supported.")
    if parsed.username or parsed.password:
        raise ScanError("URLs containing usernames or passwords are not allowed.")
    host = parsed.hostname.rstrip(".").lower()
    if host in ("localhost",) or host.endswith((".localhost", ".local", ".internal", ".test")):
        raise ScanError("Private or local network targets are not allowed.")
    try:
        literal = ipaddress.ip_address(host)
        if not literal.is_global:
            raise ScanError("Private, reserved, and local IP addresses are not allowed.")
    except ValueError:
        try:
            addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)}
        except OSError:
            raise ScanError("The domain could not be resolved. Check the address and try again.")
        if not addresses:
            raise ScanError("The domain did not resolve to a public address.")
        for address in addresses:
            if not ipaddress.ip_address(address).is_global:
                raise ScanError("The domain resolves to a private or reserved network address.")
    # Remove fragments; retain query because it can be part of the public landing page.
    return value.split("#", 1)[0]


def scan_website(raw_url: str) -> dict:
    target = _validate_target(raw_url)
    parsed = urlparse(target)
    session = requests.Session()
    session.trust_env = False
    try:
        response = session.get(
            target,
            headers={"User-Agent": "CODEFIXPH-QuantumShield/1.0 (+authorized security posture check)"},
            timeout=(4, 8),
            allow_redirects=False,
            stream=True,
            verify=True,
        )
        status = response.status_code
        headers = {k.lower(): v for k, v in response.headers.items()}
        response.close()
    except requests.exceptions.SSLError:
        raise ScanError("TLS certificate validation failed. No insecure TLS fallback was attempted.")
    except requests.exceptions.Timeout:
        raise ScanError("The website took too long to respond (8-second read limit).")
    except requests.exceptions.RequestException:
        raise ScanError("Could not connect safely to the website.")

    findings = []
    def add(severity, title, detail, recommendation):
        findings.append({"severity": severity, "title": title, "detail": detail, "recommendation": recommendation})

    if parsed.scheme != "https":
        add("high", "HTTPS is not enabled", "The submitted address uses plain HTTP.", "Enable HTTPS with a valid certificate and redirect HTTP to HTTPS.")
    if "strict-transport-security" not in headers:
        add("medium", "HSTS header missing", "The response does not advertise HTTP Strict Transport Security.", "For HTTPS sites, configure Strict-Transport-Security with an appropriate max-age after confirming all subdomains support HTTPS.")
    if "content-security-policy" not in headers:
        add("medium", "Content Security Policy missing", "No Content-Security-Policy header was observed.", "Define a restrictive CSP based on the scripts, styles, images, and connections the site actually needs.")
    if "x-content-type-options" not in headers:
        add("low", "MIME-sniffing protection missing", "X-Content-Type-Options was not observed.", "Set X-Content-Type-Options: nosniff.")
    if "x-frame-options" not in headers and "frame-ancestors" not in headers.get("content-security-policy", "").lower():
        add("medium", "Clickjacking defense not detected", "Neither X-Frame-Options nor CSP frame-ancestors was observed.", "Set a suitable frame-ancestors CSP directive; use X-Frame-Options as a legacy fallback.")
    if "referrer-policy" not in headers:
        add("low", "Referrer-Policy missing", "The response does not define a Referrer-Policy.", "Choose a policy such as strict-origin-when-cross-origin based on your privacy requirements.")
    if "permissions-policy" not in headers:
        add("low", "Permissions-Policy missing", "The response does not define a Permissions-Policy.", "Disable browser features the site does not need, such as camera, microphone, and geolocation.")
    server = headers.get("server")
    if server:
        add("info", "Server header disclosed", "The response includes a Server header; it may reveal implementation details.", "Consider minimizing unnecessary version or platform details in response headers.")
    cookies = headers.get("set-cookie", "")
    if cookies:
        lower_cookie = cookies.lower()
        if parsed.scheme == "https" and "secure" not in lower_cookie:
            add("medium", "Cookie Secure attribute not observed", "At least one Set-Cookie response was observed without a Secure attribute.", "Set Secure on session and sensitive cookies served over HTTPS.")
        if "httponly" not in lower_cookie:
            add("medium", "Cookie HttpOnly attribute not observed", "At least one Set-Cookie response was observed without HttpOnly.", "Set HttpOnly on cookies that do not need JavaScript access.")
        if "samesite" not in lower_cookie:
            add("low", "Cookie SameSite attribute not observed", "At least one Set-Cookie response was observed without SameSite.", "Set an appropriate SameSite policy and add CSRF protection where needed.")
    if not findings:
        add("info", "No checked header gaps detected", "The limited checks did not identify the listed header issues.", "Continue with a full, authorized security review; this result is not proof that the site is secure.")

    weights = {"critical": 25, "high": 15, "medium": 8, "low": 3, "info": 0}
    penalty = sum(weights.get(item["severity"], 0) for item in findings)
    score = max(0, 100 - penalty)
    return {
        "product": "CODEFIXPH Quantum Shield",
        "scan_type": "passive_http_security_headers",
        "target": target,
        "http_status": status,
        "score": score,
        "rating": "Good" if score >= 85 else "Needs attention" if score >= 60 else "High risk",
        "findings": findings,
        "limitations": [
            "One bounded HTTP GET request only; redirects are not followed.",
            "Checks visible response headers and basic HTTPS usage only.",
            "Does not test application logic, authentication, authorization, source code, dependencies, or exploitability.",
            "A high score is not a security certification or guarantee of safety.",
            "Only scan websites you own or have explicit permission to assess."
        ]
    }

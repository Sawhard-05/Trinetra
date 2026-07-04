from urllib.parse import urlparse
import re

KEYWORDS = ["login", "verify", "update", "secure", "account", "bank", "password"]
SUSPICIOUS_TLDS = ["xyz", "top", "click", "online", "info", "live"]


def analyze_url(url):
    reasons = []
    explanation = ""

    url_lower = url.lower()
    parsed = urlparse(url)
    domain = parsed.netloc

    for k in KEYWORDS:
        if k in url_lower:
            reasons.append(f"Suspicious keyword detected: {k}")
            explanation = "The URL contains common phishing keywords used in fake login or verification pages."
            break

    if "@" in url_lower:
        reasons.append("URL contains '@' symbol")
        explanation = "The '@' symbol is often used to redirect users to malicious websites."

    if len(url) > 80:
        reasons.append("URL is unusually long")
        explanation = "Long URLs are commonly used to hide malicious content."

    if "-" in domain:
        reasons.append("Hyphen found in domain name")
        explanation = "Hyphenated domains are frequently used in phishing attacks."

    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", domain):
        reasons.append("IP address used instead of domain")
        explanation = "Legitimate websites usually do not use raw IP addresses."

    if domain:
        tld = domain.split(".")[-1]
        if tld in SUSPICIOUS_TLDS:
            reasons.append(f"Suspicious domain extension: .{tld}")
            explanation = "The domain extension used is commonly abused for phishing websites."

    if domain.count(".") > 2:
        reasons.append("Multiple subdomains detected")
        explanation = "Multiple subdomains are often used to disguise phishing URLs."

    score = len(reasons)

    if score == 0:
        confidence = "Low"
        explanation = "No common phishing indicators were detected."
    elif score <= 2:
        confidence = "Medium"
    else:
        confidence = "High"

    return {
        "url": url,
        "is_phishing": score > 0,
        "confidence": confidence,
        "reasons": reasons,
        "explanation": explanation
    }

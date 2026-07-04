import re

FREE_PROVIDERS = ["gmail.com", "yahoo.com", "outlook.com"]


def analyze_email(headers):
    reasons = []
    explanation = ""

    from_header = headers.get("From", "")
    reply_to = headers.get("Reply-To", "")
    subject = headers.get("Subject", "")

    # Extract actual email from From header if format is: Name <email@domain.com>
    display_match = re.search(r"\s*(.*?)\s*<\s*(.*?)\s*>", from_header)

    if display_match:
        name = display_match.group(1).strip().lower()
        from_email = display_match.group(2).strip().lower()
    else:
        name = ""
        from_email = from_header.strip().lower()

    reply_to_email = reply_to.strip().lower()

    # Compare actual email addresses, not full From header text
    if reply_to_email and reply_to_email != from_email:
        reasons.append("Reply-To address differs from From address")
        explanation = "The email redirects replies to a different address, which is a common spoofing technique."

    if display_match:
        if ("bank" in name or "paypal" in name) and not from_email.endswith(("bank.com", "paypal.com")):
            reasons.append("Display name does not match sender domain")
            explanation = "The sender name appears legitimate, but the email domain does not match the organization."

    if any(p in from_email for p in FREE_PROVIDERS) and ("bank" in subject.lower() or "verify" in subject.lower()):
        reasons.append("Free email provider used for official communication")
        explanation = "Official organizations typically do not send emails from free email providers."

    if any(k in subject.lower() for k in ["urgent", "verify", "suspended", "click"]):
        reasons.append("Urgent or threatening language in subject")
        explanation = "Urgent language is commonly used to pressure users in phishing emails."

    score = len(reasons)

    if score == 0:
        confidence = "Low"
        explanation = "No clear phishing indicators were found in the email."
    elif score <= 2:
        confidence = "Medium"
    else:
        confidence = "High"

    return {
        "suspicious": score > 0,
        "confidence": confidence,
        "reasons": reasons,
        "explanation": explanation
    }
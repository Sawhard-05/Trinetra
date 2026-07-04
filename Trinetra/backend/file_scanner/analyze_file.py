import os

DANGEROUS_EXTENSIONS = [".exe", ".bat", ".cmd", ".vbs", ".js", ".ps1", ".scr"]
MACRO_FILES = [".docm", ".xlsm", ".pptm"]
SUSPICIOUS_KEYWORDS = [b"powershell", b"cmd.exe", b"wget", b"curl", b"invoke-webrequest", b"base64"]

HEADER_SIGNATURES = {
    b"MZ": "exe",
    b"\x7fELF": "elf",
    b"%PDF": "pdf",
    b"PK\x03\x04": "zip"
}


def analyze_file(path, filename):
    reasons = []
    explanation = ""

    file_size = os.path.getsize(path)
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in DANGEROUS_EXTENSIONS:
        reasons.append("Executable or script file detected")
        explanation = "Executable or script files can directly run code and may pose security risks."

    if ext in MACRO_FILES:
        reasons.append("Macro-enabled document detected")
        explanation = "Macro-enabled documents can execute hidden scripts when opened."

    if "." in filename[:-len(ext)]:
        reasons.append("Double file extension detected")
        explanation = "Multiple file extensions are often used to disguise malicious files."

    if file_size < 1024:
        reasons.append("Unusually small file size")
        explanation = "The file size is unusually small for its type, which can indicate a hidden payload."

    try:
        with open(path, "rb") as f:
            header = f.read(8)
            content = f.read().lower()

        detected_type = None
        for sig, ftype in HEADER_SIGNATURES.items():
            if header.startswith(sig):
                detected_type = ftype
                break

        if detected_type:
            if (detected_type == "exe" and ext not in [".exe"]) or \
               (detected_type == "pdf" and ext not in [".pdf"]) or \
               (detected_type == "zip" and ext not in [".zip", ".docx", ".xlsx", ".pptx"]):
                reasons.append("File header does not match file extension")
                explanation = "The internal file structure does not match its extension, indicating possible disguise."

        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in content:
                reasons.append("Suspicious command-related content detected")
                explanation = "The file contains command-related instructions commonly used in malicious scripts."
                break

    except:
        reasons.append("File could not be safely analyzed")
        explanation = "The file could not be fully read, which may indicate corruption or unsafe structure."

    score = len(reasons)

    if score == 0:
        confidence = "Low"
        explanation = "No unsafe patterns were detected in the file."
    elif score <= 2:
        confidence = "Medium"
    else:
        confidence = "High"

    return {
        "filename": filename,
        "file_size_bytes": file_size,
        "is_safe": score == 0,
        "confidence": confidence,
        "reasons": reasons,
        "explanation": explanation
    }

# Trinetra – Cyber Threat Awareness System

## Project Overview

**Trinetra** is a Python and Flask-based Cyber Threat Awareness System that helps users identify potentially suspicious **URLs**, **emails**, and **files** using rule-based analysis. It provides confidence-based results along with clear explanations, making it easy for non-technical users to understand potential cyber threats. The project was developed as my **Bachelor of Computer Applications (BCA) Final Year Project**.

---

## How It Works

The application provides a simple web interface where users can choose to analyze a URL, an email, or a file.

### 1. URL Analysis
Checks for common phishing indicators such as:
- Suspicious keywords
- Long URLs
- Hyphenated domains
- IP-based URLs
- Multiple subdomains
- Suspicious domain extensions

### 2. Email Analysis
Analyzes email headers including:
- From Address
- Reply-To Address
- Subject Line

Detects:
- Reply-To mismatch
- Display-name spoofing
- Free email providers used as official senders
- Urgent or threatening subject lines

### 3. File Analysis
Performs safe static analysis without executing the file.

Checks for:
- Dangerous file extensions
- Double extensions
- Macro-enabled documents
- Suspicious command-related keywords
- File header mismatch
- Unusually small file size

The application then displays:
- ✅ Safe / Suspicious Status
- 📊 Confidence Level
- 📝 Detection Reasons
- 💬 Human-readable Explanation

---

## Project Files

| File/Folder | Description |
|-------------|-------------|
| `backend/app.py` | Main Flask application |
| `backend/phishing_scanner/` | URL analysis module |
| `backend/email_analyzer/` | Email analysis module |
| `backend/file_scanner/` | File analysis module |
| `backend/templates/` | HTML frontend |
| `backend/static/` | CSS, JavaScript, and images |
| `backend/uploads/` | Temporary uploaded files |
| `requirements.txt` | Required Python libraries |

---

## Requirements

- Python 3.x
- Flask

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Navigate to the backend folder

```bash
cd backend
```

### Step 3: Run the application

```bash
python app.py
```

### Step 4:

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Why I Built This

I built **Trinetra** as my **BCA Final Year Project** to create a simple and explainable cyber threat awareness system for everyday users.

Many cybersecurity tools are designed for professionals and often provide technical outputs that can be difficult for non-technical users to understand. Trinetra focuses on identifying suspicious URLs, emails, and files using lightweight rule-based detection and presenting the results in a clear, easy-to-understand format.

The project helped me strengthen my knowledge of **Python**, **Flask**, **backend development**, **REST APIs**, and **basic cybersecurity concepts** while building a practical application with real-world use cases.

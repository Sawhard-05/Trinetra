from flask import Flask, request, jsonify, render_template
import os

from phishing_scanner.phishing_check import analyze_url
from email_analyzer.analyze_email import analyze_email
from file_scanner.analyze_file import analyze_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan/url", methods=["POST"])
def scan_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL not provided"}), 400
    return jsonify(analyze_url(data["url"]))


@app.route("/scan/email", methods=["POST"])
def scan_email():
    data = request.get_json()
    if not data or "headers" not in data:
        return jsonify({"error": "Headers not provided"}), 400
    return jsonify(analyze_email(data["headers"]))


@app.route("/scan/file", methods=["POST"])
def scan_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    result = analyze_file(path, file.filename)

    try:
        os.remove(path)
    except:
        pass

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5001)


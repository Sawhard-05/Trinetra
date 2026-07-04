let scanHistory = [];
let lastScanData = null;
let lastScanType = "";

function showSection(id) {
    document.querySelectorAll(".section").forEach(s => s.classList.add("hidden"));
    document.getElementById(id).classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");
    document.getElementById("advice").classList.add("hidden");
    document.getElementById("downloadBtn").classList.add("hidden");
}

function addToHistory(type, confidence) {
    scanHistory.unshift({
        type: type,
        confidence: confidence,
        time: new Date().toLocaleTimeString()
    });

    if (scanHistory.length > 5) scanHistory.pop();

    const historyList = document.getElementById("history");
    historyList.innerHTML = "";

    scanHistory.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.type} Scan – ${item.confidence} (${item.time})`;
        historyList.appendChild(li);
    });
}

function showAdvice(confidence, type) {
    const advice = document.getElementById("advice");
    advice.classList.remove("hidden");

    let message = "";
    if (confidence === "High") {
        message = `Do NOT open, click, or reply to this ${type}. Delete it immediately.`;
    } else if (confidence === "Medium") {
        message = `Proceed with caution. Verify the source of this ${type} before interacting.`;
    } else {
        message = `No immediate threat detected. Stay alert for unusual behavior.`;
    }

    advice.innerHTML = `<strong>What should you do next?</strong><br><br>${message}`;
}

function showResult(data, type) {
    const result = document.getElementById("result");
    result.className = "result";
    result.classList.remove("hidden");

    let level = "safe";
    if (data.confidence === "Medium") level = "medium";
    if (data.confidence === "High") level = "high";
    result.classList.add(level);

    result.innerHTML = `
        <strong>Confidence:</strong> ${data.confidence}<br><br>
        <strong>Explanation:</strong><br>${data.explanation}<br><br>
        <strong>Reasons:</strong>
        <ul>${(data.reasons || []).map(r => `<li>${r}</li>`).join("")}</ul>
        <small>This analysis is based on known patterns and should not replace professional security tools.</small>
    `;

    lastScanData = data;
    lastScanType = type;

    document.getElementById("downloadBtn").classList.remove("hidden");

    addToHistory(type, data.confidence);
    showAdvice(data.confidence, type);
}

async function scanURL() {
    const url = document.getElementById("urlInput").value;

    const res = await fetch("/scan/url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    });

    showResult(await res.json(), "URL");
}

async function scanEmail() {
    const raw = document.getElementById("emailInput").value;
    const headers = {};

    raw.split("\n").forEach(line => {
        const p = line.split(":");
        if (p.length >= 2) headers[p[0].trim()] = p.slice(1).join(":").trim();
    });

    const res = await fetch("/scan/email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ headers })
    });

    showResult(await res.json(), "Email");
}

async function scanFile() {
    const file = document.getElementById("fileInput").files[0];
    const form = new FormData();
    form.append("file", file);

    const res = await fetch("/scan/file", {
        method: "POST",
        body: form
    });

    showResult(await res.json(), "File");
}

function downloadReport() {
    if (!lastScanData) return;

    const report = `
TRINETRA – Scan Report
----------------------

Scan Type: ${lastScanType}
Confidence: ${lastScanData.confidence}

Explanation:
${lastScanData.explanation}

Reasons:
${(lastScanData.reasons || []).map(r => "- " + r).join("\n")}

Recommendation:
${getRecommendation(lastScanData.confidence, lastScanType)}

Date & Time:
${new Date().toLocaleString()}

Disclaimer:
This analysis is based on known patterns and should not replace professional security tools.
`;

    const blob = new Blob([report], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `trinetra_${lastScanType.toLowerCase()}_report.txt`;
    link.click();
}

function getRecommendation(confidence, type) {
    if (confidence === "High") {
        return `Do NOT open, click, or reply to this ${type}. Delete it immediately.`;
    }
    if (confidence === "Medium") {
        return `Proceed with caution. Verify the source of this ${type} before interacting.`;
    }
    return `No immediate threat detected. Stay alert for unusual behavior.`;
}

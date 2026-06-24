from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/normalize", methods=["POST"])
def normalize():

    data = request.json

    normalized = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "unknown",
        "severity": "LOW",
        "event_type": "unknown"
    }

    # Falco normalization
    if "rule" in data:
        normalized["source"] = "falco"
        normalized["severity"] = data.get("priority", "LOW").upper()

        if "shell" in data["rule"].lower():
            normalized["event_type"] = "shell_spawn"

    # Prowler normalization
    elif "check" in data:
        normalized["source"] = "prowler"
        normalized["severity"] = data.get("severity", "LOW").upper()
        normalized["event_type"] = "cloud_posture"

    # Kubernetes event normalization
    elif "reason" in data:
        normalized["source"] = "kubernetes"
        normalized["severity"] = "MEDIUM"
        normalized["event_type"] = data["reason"]

    return jsonify(normalized)

app.run(host="0.0.0.0", port=8080)

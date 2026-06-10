
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/tools", methods=["GET"])
def tools():
    return jsonify({
        "tools": [
            "get_logs",
            "restart_deployment",
            "get_pods"
        ]
    })

@app.route("/tool/get_logs", methods=["POST"])
def get_logs():
    deployment = request.json["deployment"]

    result = subprocess.run(
        [
            "kubectl",
            "logs",
            f"deployment/{deployment}",
            "--tail=20"
        ],
        capture_output=True,
        text=True
    )

    return jsonify({
        "logs": result.stdout
    })

@app.route("/tool/get_pods", methods=["POST"])
def get_pods():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-o", "wide"],
        capture_output=True,
        text=True
    )

    return jsonify({
        "pods": result.stdout
    })

@app.route("/tool/restart_deployment", methods=["POST"])
def restart():
    deployment = request.json["deployment"]

    result = subprocess.run(
        [
            "kubectl",
            "rollout",
            "restart",
            f"deployment/{deployment}"
        ],
        capture_output=True,
        text=True
    )

    return jsonify({
        "result": result.stdout + result.stderr
    })

app.run(host="0.0.0.0", port=9000)

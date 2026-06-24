import json
from flask import Flask, request, jsonify

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "PROJECT_ID"
LOCATION = "us-central1"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)

model = GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():

    event = request.json

    prompt = f"""
    You are a Kubernetes security analyst.

    Analyze this event:

    {json.dumps(event, indent=2)}

    Provide:
    1. Summary
    2. Possible risk
    3. Recommended next step

    Keep response concise.
    """

    response = model.generate_content(prompt)

    return jsonify({
        "event": event,
        "summary": response.text
    })

app.run(host="0.0.0.0", port=8080)

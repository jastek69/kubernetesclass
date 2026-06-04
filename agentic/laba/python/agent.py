import os
from dotenv import load_dotenv  # Or load_dotenv
load_dotenv()  # This automatically reads your .env file
import subprocess
import time
from google import genai

PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ.get("LOCATION", "us-central1")
TARGET_DEPLOYMENT = os.environ.get("TARGET_DEPLOYMENT", "broken-app")
TARGET_NAMESPACE = os.environ.get("TARGET_NAMESPACE", "default")
MODEL = os.environ.get("MODEL", "gemini-2.0-flash")

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)

def get_logs():
    cmd = [
        "kubectl",
        "logs",
        f"deployment/{TARGET_DEPLOYMENT}",
        "-n",
        TARGET_NAMESPACE,
        "--tail=30",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout + result.stderr

def ask_vertex(logs):
    prompt = f"""
You are an SRE assistant.

Analyze these Kubernetes application logs.

Return:
1. likely_issue
2. severity: low, medium, high
3. recommended_action
4. should_restart: yes or no

Logs:
{logs}
"""

    print("Prompt:", prompt)

    response = client.models.generate_content(
            model=MODEL,
            contents=logs,
        )
    return response.text

def restart_deployment():
    cmd = [
        "kubectl",
        "rollout",
        "restart",
        f"deployment/{TARGET_DEPLOYMENT}",
        "-n",
        TARGET_NAMESPACE,
    ]
    subprocess.run(cmd)

while True:
    print("Collecting logs...")
    logs = get_logs()

    print("Asking Vertex AI...")
    diagnosis = ask_vertex(logs)

    print("=== Agent Diagnosis ===")
    print(diagnosis)

    if "should_restart: yes" in diagnosis.lower():
        print("Agent chose restart action.")
        restart_deployment()
    else:
        print("Agent chose no restart.")

    time.sleep(60)

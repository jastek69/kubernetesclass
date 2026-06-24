```python id="ad4g1b"
import base64
import json
from datetime import datetime

from kubernetes import client, config

from cryptography import x509
from cryptography.hazmat.backends import default_backend

import vertexai
from vertexai.generative_models import GenerativeModel

# ==========================================
# CONFIG
# ==========================================

PROJECT_ID = "PROJECT_ID"
LOCATION = "us-central1"

TARGET_NAMESPACE = "mcp-gateway"

# ==========================================
# VERTEX INIT
# ==========================================

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)

model = GenerativeModel(
    "claude-3-5-sonnet@20240620"
)

# ==========================================
# K8 INIT
# ==========================================

config.load_incluster_config()

v1 = client.CoreV1Api()

# ==========================================
# MAIN
# ==========================================

def analyze_cert(secret):

    cert_b64 = secret.data.get("tls.crt")

    if not cert_b64:
        return None

    cert_pem = base64.b64decode(cert_b64)

    cert = x509.load_pem_x509_certificate(
        cert_pem,
        default_backend()
    )

    now = datetime.utcnow()

    days_remaining = (
        cert.not_valid_after - now
    ).days

    issuer = cert.issuer.rfc4514_string()

    subject = cert.subject.rfc4514_string()

    algo = cert.signature_hash_algorithm.name

    findings = {
        "secret_name": secret.metadata.name,
        "issuer": issuer,
        "subject": subject,
        "days_remaining": days_remaining,
        "algorithm": algo
    }

    return findings


def summarize_with_claude(findings):

    prompt = f"""
    You are a Certificate Guardian AI agent.

    Analyze this certificate health data.

    Identify:
    1. expiration risk
    2. cryptographic concerns
    3. compliance concerns
    4. operational recommendations

    Certificate Data:
    {json.dumps(findings, indent=2)}

    Keep response concise.
    """

    response = model.generate_content(prompt)

    return response.text


# ==========================================
# RUN
# ==========================================

print("\n=== CERTIFICATE GUARDIAN ===\n")

secrets = v1.list_namespaced_secret(
    TARGET_NAMESPACE
)

for secret in secrets.items:

    if secret.type != "kubernetes.io/tls":
        continue

    findings = analyze_cert(secret)

    if not findings:
        continue

    print(
        f"\n--- Certificate: "
        f"{findings['secret_name']} ---\n"
    )

    print(json.dumps(findings, indent=2))

    summary = summarize_with_claude(findings)

    print("\n=== CLAUDE ANALYSIS ===\n")
    print(summary)
    print("\n=======================\n")
```

import json
from datetime import datetime

INPUT_FILE = "/opt/ai-soc/reports/risk_prioritized_findings.json"
OUTPUT_FILE = "/opt/ai-soc/reports/owasp_mapped_findings.json"

OWASP_MAP = {
    "policy_violation": {
        "category": "A01:2021 Broken Access Control",
        "reason": "Policy violations may indicate unauthorized access attempts or improper authorization boundaries."
    },
    "unauthorized_mcp_request": {
        "category": "A01:2021 Broken Access Control",
        "reason": "Unauthorized MCP requests suggest access control enforcement or client authorization issues."
    },
    "tls_failure": {
        "category": "A02:2021 Cryptographic Failures",
        "reason": "TLS failures may indicate certificate, trust chain, or encrypted transport problems."
    },
    "cert_expiring": {
        "category": "A02:2021 Cryptographic Failures",
        "reason": "Expiring certificates can weaken service trust and cause outages if not rotated."
    },
    "shell_spawn": {
        "category": "A05:2021 Security Misconfiguration",
        "reason": "Unexpected shell execution inside a container can indicate unsafe runtime configuration or compromise."
    },
    "critical_cve": {
        "category": "A06:2021 Vulnerable and Outdated Components",
        "reason": "Critical CVEs indicate vulnerable software components requiring prioritization."
    },
    "weak_secret_handling": {
        "category": "A07:2021 Identification and Authentication Failures",
        "reason": "Weak secret handling can compromise identity, authentication, or workload trust."
    },
    "log_injection": {
        "category": "A03:2021 Injection",
        "reason": "Injected content in logs or telemetry may influence downstream systems or AI agents."
    },
    "prompt_injection": {
        "category": "A03:2021 Injection",
        "reason": "Prompt injection is a form of malicious instruction injection against AI systems."
    },
    "ssrf_attempt": {
        "category": "A10:2021 Server-Side Request Forgery",
        "reason": "SSRF attempts may indicate attempts to reach internal metadata or control-plane services."
    },
    "404_spike": {
        "category": "A05:2021 Security Misconfiguration",
        "reason": "Repeated 404s may indicate endpoint probing, scanning, or exposed routing issues."
    },
    "403_spike": {
        "category": "A01:2021 Broken Access Control",
        "reason": "Repeated 403s may indicate access attempts blocked by authorization controls."
    }
}


def map_to_owasp(events):
    mappings = []

    for event in events:
        if event in OWASP_MAP:
            mappings.append({
                "event_type": event,
                "owasp_category": OWASP_MAP[event]["category"],
                "mapping_reason": OWASP_MAP[event]["reason"]
            })

    if not mappings:
        mappings.append({
            "event_type": "unknown",
            "owasp_category": "Unmapped",
            "mapping_reason": "No OWASP mapping was identified for the supplied telemetry events."
        })

    return mappings


with open(INPUT_FILE, "r") as f:
    findings = json.load(f)

results = []

for finding in findings:
    events = finding.get("telemetry_events", [])

    owasp_mappings = map_to_owasp(events)

    result = {
        "student_id": finding.get("student_id", "unknown"),
        "timestamp": datetime.utcnow().isoformat(),
        "risk_level": finding.get("risk_level"),
        "risk_score": finding.get("risk_score"),
        "finding_summary": finding.get("finding_summary"),
        "telemetry_events": events,
        "owasp_mappings": owasp_mappings,
        "analyst_note": (
            "This mapping is intended to help analysts classify the finding using "
            "common application security language. It is not a final compliance determination."
        )
    }

    results.append(result)

with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print("\n=== OWASP MAPPED FINDINGS ===\n")

for result in results:
    print(json.dumps(result, indent=2))

```python id="s4nvyx"
import json
from datetime import datetime

INPUT_FILE = \
"/opt/ai-soc/reports/risk_prioritized_findings.json"

OUTPUT_FILE = \
"/opt/ai-soc/reports/nist_mapped_findings.json"

# ==========================================
# NIST MAPPINGS
# ==========================================

NIST_MAP = {

    "tls_failure": {

        "function":
            "PR",

        "category":
            "PR.DS",

        "description":
            "Protective data security mechanisms failed during encrypted communications."
    },

    "cert_expiring": {

        "function":
            "PR",

        "category":
            "PR.DS",

        "description":
            "Cryptographic protections may become unreliable due to certificate expiration."
    },

    "unauthorized_mcp_request": {

        "function":
            "PR",

        "category":
            "PR.AC",

        "description":
            "Unauthorized requests indicate access control enforcement activity."
    },

    "policy_violation": {

        "function":
            "PR",

        "category":
            "PR.IP",

        "description":
            "Security policy enforcement mechanisms detected violations."
    },

    "shell_spawn": {

        "function":
            "DE",

        "category":
            "DE.CM",

        "description":
            "Unexpected runtime behavior detected in monitored systems."
    },

    "critical_cve": {

        "function":
            "ID",

        "category":
            "ID.RA",

        "description":
            "Critical vulnerabilities increase operational risk exposure."
    },

    "prompt_injection_attempt": {

        "function":
            "DE",

        "category":
            "DE.AE",

        "description":
            "AI prompt manipulation attempts indicate anomalous activity."
    },

    "unsafe_tool_invocation": {

        "function":
            "PR",

        "category":
            "PR.AC",

        "description":
            "Unsafe AI tool usage may bypass intended authorization boundaries."
    },

    "runtime_anomaly": {

        "function":
            "DE",

        "category":
            "DE.CM",

        "description":
            "Runtime monitoring identified abnormal system behavior."
    },

    "403_spike": {

        "function":
            "DE",

        "category":
            "DE.CM",

        "description":
            "Repeated denied access attempts may indicate probing activity."
    },

    "404_spike": {

        "function":
            "DE",

        "category":
            "DE.AE",

        "description":
            "Repeated endpoint failures may indicate reconnaissance activity."
    }
}

# ==========================================
# LOAD FINDINGS
# ==========================================

with open(INPUT_FILE, "r") as f:

    findings = json.load(f)

results = []

# ==========================================
# PROCESS
# ==========================================

for finding in findings:

    events = finding.get(
        "telemetry_events",
        []
    )

    nist_mappings = []

    for event in events:

        if event in NIST_MAP:

            mapping = {

                "event_type":
                    event,

                "nist_function":
                    NIST_MAP[event]["function"],

                "nist_category":
                    NIST_MAP[event]["category"],

                "description":
                    NIST_MAP[event]["description"]
            }

            nist_mappings.append(mapping)

    if not nist_mappings:

        nist_mappings.append({

            "event_type":
                "unknown",

            "nist_function":
                "UNMAPPED",

            "nist_category":
                "UNMAPPED",

            "description":
                "No NIST mapping identified."
        })

    result = {

        "student_id":
            finding.get("student_id"),

        "timestamp":
            str(datetime.utcnow()),

        "risk_level":
            finding.get("risk_level"),

        "risk_score":
            finding.get("risk_score"),

        "finding_summary":
            finding.get("finding_summary"),

        "telemetry_events":
            events,

        "nist_mappings":
            nist_mappings,

        "analyst_note":
            "Mappings align operational telemetry "
            "with NIST Cybersecurity Framework concepts."
    }

    results.append(result)

# ==========================================
# OUTPUT
# ==========================================

with open(OUTPUT_FILE, "w") as f:

    json.dump(results, f, indent=2)

print("\n=== NIST MAPPED FINDINGS ===\n")

for result in results:

    print(json.dumps(result, indent=2))
```

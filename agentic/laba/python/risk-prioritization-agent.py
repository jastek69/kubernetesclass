```python
import json
from datetime import datetime

INPUT_FILE = \
"/opt/ai-soc/correlated/correlated_findings.json"

OUTPUT_FILE = \
"/opt/ai-soc/reports/risk_prioritized_findings.json"

# ==========================================
# RISK LOGIC
# ==========================================

def determine_priority(score):

    if score >= 81:
        return "CRITICAL"

    elif score >= 51:
        return "HIGH"

    elif score >= 21:
        return "MEDIUM"

    return "LOW"


# ==========================================
# LOAD CORRELATED FINDINGS
# ==========================================

with open(INPUT_FILE, "r") as f:

    findings = json.load(f)

# ==========================================
# ANALYSIS
# ==========================================

results = []

for finding in findings:

    score = finding["risk_score"]

    level = determine_priority(score)

    events = finding["events"]

    # ======================================
    # CONTEXT GENERATION
    # ======================================

    summary = \
        "Multiple correlated telemetry events detected."

    why_it_matters = \
        "Correlated findings increase probability " \
        "of operational or security issues."

    likely_root_cause = \
        "Unknown. Additional investigation required."

    blast_radius = \
        "Potential impact limited to namespace scope."

    attack_surface = \
        "Internal Kubernetes telemetry."

    escalation = \
        "Level 1 analyst review recommended."

    # ======================================
    # ENRICHMENT
    # ======================================

    if "tls_failure" in events:

        attack_surface = \
            "Internet-facing mTLS gateway"

        likely_root_cause = \
            "Invalid client certificates, " \
            "trust mismatch, or unauthorized access attempts."

    if "shell_spawn" in events:

        blast_radius = \
            "Possible container compromise."

        escalation = \
            "Immediate analyst escalation recommended."

    if "critical_cve" in events:

        why_it_matters = \
            "Critical vulnerabilities may permit " \
            "remote compromise or privilege escalation."

    # ======================================
    # BUILD RESULT
    # ======================================

    enriched = {

        "student_id":
            finding["student_id"],

        "timestamp":
            str(datetime.utcnow()),

        "risk_level":
            level,

        "risk_score":
            score,

        "finding_summary":
            summary,

        "telemetry_events":
            events,

        "attack_surface":
            attack_surface,

        "blast_radius":
            blast_radius,

        "why_it_matters":
            why_it_matters,

        "likely_root_cause":
            likely_root_cause,

        "recommended_escalation":
            escalation
    }

    results.append(enriched)

# ==========================================
# OUTPUT
# ==========================================

with open(OUTPUT_FILE, "w") as f:

    json.dump(results, f, indent=2)

print("\n=== RISK PRIORITIZED FINDINGS ===\n")

for result in results:

    print(json.dumps(result, indent=2))
```

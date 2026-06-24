```python id="2mye4j"
import json
from datetime import datetime

INPUT_FILE = \
"/opt/ai-soc/reports/risk_prioritized_findings.json"

OUTPUT_FILE = \
"/opt/ai-soc/reports/ai_owasp_mapped_findings.json"

# ==========================================
# AI OWASP MAPPINGS
# ==========================================

AI_OWASP_MAP = {

    "prompt_injection_attempt": {

        "category":
            "LLM01: Prompt Injection",

        "reason":
            "Untrusted prompt content may manipulate AI behavior."
    },

    "unsafe_tool_invocation": {

        "category":
            "LLM08: Excessive Agency",

        "reason":
            "AI agents invoking tools without adequate restrictions."
    },

    "sensitive_data_exposure": {

        "category":
            "LLM06: Sensitive Information Disclosure",

        "reason":
            "AI responses exposing secrets or confidential information."
    },

    "hallucinated_action": {

        "category":
            "LLM09: Overreliance",

        "reason":
            "AI-generated actions may be inaccurate or unsafe."
    },

    "external_api_without_validation": {

        "category":
            "LLM07: Insecure Plugin Design",

        "reason":
            "External APIs used without sufficient trust validation."
    },

    "agent_chain_escalation": {

        "category":
            "LLM08: Excessive Agency",

        "reason":
            "Autonomous agent chains increasing operational risk."
    },

    "model_dos_attempt": {

        "category":
            "LLM04: Model Denial of Service",

        "reason":
            "High-volume prompts attempting to exhaust model resources."
    },

    "untrusted_mcp_connection": {

        "category":
            "LLM07: Insecure Plugin Design",

        "reason":
            "MCP connections without adequate trust enforcement."
    },

    "unsafe_output_forwarding": {

        "category":
            "LLM02: Insecure Output Handling",

        "reason":
            "AI-generated content forwarded into systems without validation."
    },

    "retrieval_data_poisoning": {

        "category":
            "LLM03: Training Data Poisoning",

        "reason":
            "Corrupted or malicious retrieval data influencing AI output."
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

    ai_mappings = []

    for event in events:

        if event in AI_OWASP_MAP:

            mapping = {

                "event_type":
                    event,

                "ai_owasp_category":
                    AI_OWASP_MAP[event]["category"],

                "mapping_reason":
                    AI_OWASP_MAP[event]["reason"]
            }

            ai_mappings.append(mapping)

    if not ai_mappings:

        ai_mappings.append({

            "event_type":
                "unknown",

            "ai_owasp_category":
                "Unmapped",

            "mapping_reason":
                "No AI OWASP mapping identified."
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

        "ai_owasp_mappings":
            ai_mappings,

        "analyst_note":
            "Mappings align telemetry findings "
            "with AI-specific OWASP risk categories."
    }

    results.append(result)

# ==========================================
# OUTPUT
# ==========================================

with open(OUTPUT_FILE, "w") as f:

    json.dump(results, f, indent=2)

print("\n=== AI OWASP MAPPED FINDINGS ===\n")

for result in results:

    print(json.dumps(result, indent=2))
```

    dgc/
    
    ├── app.py                    # FastAPI entry point
    ├── config.py
    ├── schemas/
    │   ├── event.py
    │   ├── decision.py
    │   ├── evidence.py
    │   └── policy.py
    │
    │-- evaluators/
    │   ├── latest_tag.py
    │
    ├── engines/
    │   ├── normalization_engine.py
    │   ├── policy_engine.py
    │   ├── risk_engine.py
    │   ├── compliance_engine.py
    │   ├── approval_engine.py
    │   ├── workflow_engine.py
    │   ├── decision_engine.py
    │   └── audit_engine.py
    │
    ├── policies/
    │   ├── kubernetes/
    │   ├── mcp/
    │   ├── cloud/
    │   ├── ai/
    │   ├── owasp/
    │   └── nist/
    │
    ├── knowledge/
    │   ├── remediation/
    │   ├── control_mappings/
    │   └── severity_matrix/
    │
    ├── evidence/
    │   ├── trivy/
    │   ├── kube_bench/
    │   ├── prowler/
    │   ├── falco/
    │   ├── certs/
    │   └── gateway/
    │
    ├── state/
    │   ├── active_findings.json
    │   ├── suppression_rules.json
    │   └── workflow_state.json
    │
    └── output/
        ├── decisions/
        ├── reports/
        └── audit/
    
        

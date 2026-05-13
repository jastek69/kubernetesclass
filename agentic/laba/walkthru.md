Vertex AI Single Agent on GKE


Mantra: “The AI is not Kubernetes. The AI is not magic. The AI is being used as a reasoning step inside a normal cloud-native system.”
Secret Point: “Your code is the agent. Vertex AI is the reasoning engine. Kubernetes is the environment.”

GKE Log Investigator Agent using Vertex AI

A) Lab Use Case
    Scenario
    
    A bad application is deployed to GKE.
    
    It sometimes fails because of a fake database connection error.
    
    The agent will:
    
        Read recent pod logs
        Send the logs to Vertex AI
        Ask Vertex AI to classify the issue
        Print a recommended action
        Optionally restart the broken deployment

B) Prerequisites

    Mutants should already have:
    
        GCP / Terraform
        Existing GCP project
        Existing GKE cluster built with Terraform
        Workload Identity Federation enabled on GKE
        Terraform state working
        kubectl connected to the cluster

    APIs Enabled
        Kubernetes Engine API
        Vertex AI API
        Cloud Logging API
        IAM API
        Student Skills
    
    You should already understand:
    
        kubectl get pods
        kubectl logs
        kubectl describe pod
        basic Deployment YAML
        basic Python
        Terraform apply workflow

C) Architecture

[ Broken App Pod ]
        |
        | kubectl logs / Kubernetes API
        v
[ Agent Pod ]
        |
        | sends logs to Vertex AI
        v
[ Vertex AI / Gemini ]
        |
        | returns diagnosis
        v
[ Agent Decision ]
        |
        | optional safe action
        v
[ Restart Deployment / Print Report ]


D) Terraform Additions

vertex-agent-iam.tf:  https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/terraform/vertex-agent-iam.tf

E) YAML Kubernetes Service Account

k8s-service-account.yaml: https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/k8s-service-account.yaml
Remember to replace the Project ID

F) Allow Kubernetes SA to Use Google SA
Remember to change the PROJECT_ID

        gcloud iam service-accounts add-iam-policy-binding \
          vertex-gke-agent@PROJECT_ID.iam.gserviceaccount.com \
          --role roles/iam.workloadIdentityUser \
          --member "serviceAccount:PROJECT_ID.svc.id.goog[default/vertex-agent-ksa]"

G) Broken App

broken-app.yaml: https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/broken-app.yaml

        Apply: kubectl apply -f broken-app.yaml

H) Agent Python Code
You need this: pip install google-genai

agent.py: https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/python/agent.py

I) Dockerfile

This Dockerfile:  https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/docker/dockerfile.txt

J) Build and Push Image

        gcloud builds submit \
          --tag gcr.io/PROJECT_ID/vertex-agent:lab1a

K) Agent Deployment

vertex-agent-deployment.yaml:  https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/vertex-agent-deployment.yaml

Apply: 

        kubectl apply -f k8s-service-account.yaml
        kubectl apply -f vertex-agent-deployment.yaml


L) RBAC for Agent

agent-rbac.yaml: https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/agent-rbac.yaml

        Apply: kubectl apply -f agent-rbac.yaml


M) Validation

        kubectl get pods
        kubectl logs deployment/broken-app
        kubectl logs deployment/vertex-agent

Expected result:

Collecting logs...
Asking Vertex AI...

        === Agent Diagnosis ===
        likely_issue: database connection failure
        severity: medium
        recommended_action: check database hostname, service, DNS, and network path
        should_restart: no


If the model says restart is appropriate, students may see:

        Agent chose restart action.
        deployment.apps/broken-app restarted

O) Success Criteria

Show this to pass:

    Broken app running
    Agent pod running
    Agent reads logs
    Agent calls Vertex AI
    Agent prints diagnosis
    Agent explains likely issue
    Agent either recommends action or performs safe restart

In Conclusion.....
SpeechOPS: “I built a GKE-based AI agent that inspected pod logs, used Vertex AI to classify failures, and made a controlled remediation decision.”
Or
“I understand that agentic AI is not just prompting. It requires tools, permissions, runtime, guardrails, and feedback loops.”





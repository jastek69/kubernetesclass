
Step 1 — Namespace YAML

mcp-gateway-namespace.yaml
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/mcp-gateway-namespace.yaml


Step 2 — Service Account

mcp-gateway-sa.yaml 
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/mcp-gateway-sa.yaml

kubectl apply -f mcp-gateway-sa.yaml



Step 3 — TLS Secret

Example Secret Creation

    kubectl create secret tls mcp-server-tls \
      --cert=server.crt \
      --key=server.key \
      -n mcp-gateway

  
Client CA Secret: This validates AI agent certificates.

    kubectl create secret generic mcp-client-ca \
      --from-file=ca.crt \
      -n mcp-gateway

  


Create NGINX ConfigMap

mcp-nginx-config.yaml
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/mcp-nginx-config.yaml

Step 5 — Gateway Deployment

mcp-gateway-deployment.yaml
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/mcp-gateway-deployment.yaml

At this point, you should have:

        secrets mounted securely
        non-root execution
        TLS isolation
        dedicated trust layer

Step 6 — Service YAML

mcp-gateway-service.yaml

https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/yaml/mcp-gateway-service.yaml

Remember 

kubectl apply -f mcp-nginx-config.yaml
kubectl apply -f mcp-gateway-deployment.yaml
kubectl apply -f mcp-gateway-service.yaml

Step 7 — Validate
Check Pods: kubectl get pods -n mcp-gateway
Check Service: kubectl get svc -n mcp-gateway




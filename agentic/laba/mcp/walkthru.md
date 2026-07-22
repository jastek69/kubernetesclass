




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

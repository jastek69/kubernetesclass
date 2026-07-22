
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

Step 8 — Validate mTLS

        curl https://EXTERNAL-IP

#detour

Oh no.... you need an External IP.... Oh Mi oh my!

How to find? 

Option 1 ---> If your gateway is exposed as a LoadBalancer, the external IP can be retrieved directly.

        kubectl get svc mcp-gateway \
            -n mcp-gateway \
            -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

If Google returns a hostname instead: (Because it happened to me)

        kubectl get svc mcp-gateway \
            -n mcp-gateway \
            -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
    

Or really easy way:

export MCP_IP=$(kubectl get svc mcp-gateway \
-n mcp-gateway \
-o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "MCP Gateway IP: $MCP_IP"

you should see something like MCP Gateway IP: 34.123.45.67

Then you can curl https://$MCP_IP
or 

        openssl s_client \
        -connect ${MCP_IP}:443

Or... you could run a bash script....  

my_external_ip.sh
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/bash/my_external_ip.sh

or
k8_wait.sh
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/bash/k8_wait.sh

or
what_is_my_ip.py
https://github.com/BalericaAI/kubernetesclass/blob/main/agentic/laba/python/what_is_my_ip.py

in fact guys... why not just make a folder structure like this?

        utilities/
        
            get_gateway_ip.sh
        
            wait_for_gateway.sh
        
            validate_gateway.sh
        
            validate_mtls.py
        
            validate_certs.py
        
            validate_mcp.py

    

#resume

Expected: 400 No required SSL certificate was sent

EXCELLENT 😄---> You da man

With client cert:

        curl \
        --cert client.crt \
        --key client.key \
        https://EXTERNAL-IP

Now: ---> request succeeds

What is happening? The gateway is cryptographically verifying machine identity.

“The AI agent is no longer trusted because of network location.
The AI agent is trusted because it proves identity cryptographically.”

That is Zero Trust.  

#!/bin/bash

echo "Looking for MCP Gateway..."

IP=$(kubectl get svc mcp-gateway \
-n mcp-gateway \
-o jsonpath='{.status.loadBalancer.ingress[0].ip}')

if [ -z "$IP" ]; then
    echo "LoadBalancer still provisioning..."
    exit 1
fi

echo ""
echo "===================================="
echo "MCP Gateway Ready"
echo "===================================="
echo "External IP: $IP"
echo ""

echo "Test with:"
echo ""

echo "openssl s_client -connect ${IP}:443"
echo ""

echo "curl https://${IP}"

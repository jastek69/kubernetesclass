echo "Waiting for LoadBalancer..."

while true
do

IP=$(kubectl get svc mcp-gateway \
-n mcp-gateway \
-o jsonpath='{.status.loadBalancer.ingress[0].ip}')

if [[ -n "$IP" ]]; then
    break
fi

sleep 5

done

echo "Gateway Ready: $IP"

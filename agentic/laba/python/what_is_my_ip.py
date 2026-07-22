from kubernetes import client, config
import time

config.load_kube_config()

v1 = client.CoreV1Api()

print("Waiting for External IP...")

while True:

    svc = v1.read_namespaced_service(
        "mcp-gateway",
        "mcp-gateway"
    )

    ingress = svc.status.load_balancer.ingress

    if ingress:

        if ingress[0].ip:
            print(f"Gateway IP: {ingress[0].ip}")
            break

        if ingress[0].hostname:
            print(f"Gateway Hostname: {ingress[0].hostname}")
            break

    time.sleep(5)

```python
import json
import subprocess

from kubernetes import client, config

# ==========================================
# CONFIG
# ==========================================

PROJECT_ID = "PROJECT_ID"

AGENTS = [
    {
        "name": "mcp-observer-agent",
        "namespace": "ai-agents"
    },
    {
        "name": "mcp-guardian-agent",
        "namespace": "ai-governance"
    }
]

# ==========================================
# LOAD K8 CONFIG
# ==========================================

config.load_kube_config()

apps_v1 = client.AppsV1Api()
core_v1 = client.CoreV1Api()

# ==========================================
# HELPERS
# ==========================================

def print_status(status, message):

    prefix = "[PASS]" if status else "[FAIL]"

    print(f"{prefix} {message}")


# ==========================================
# CHECK DEPLOYMENT
# ==========================================

def check_deployment(agent):

    try:

        deploy = apps_v1.read_namespaced_deployment(
            name=agent["name"],
            namespace=agent["namespace"]
        )

        print_status(
            True,
            f"{agent['name']} deployment found"
        )

        return deploy

    except Exception as e:

        print_status(
            False,
            f"{agent['name']} deployment missing"
        )

        return None


# ==========================================
# CHECK PODS
# ==========================================

def check_pods(agent):

    pods = core_v1.list_namespaced_pod(
        namespace=agent["namespace"]
    )

    found = False

    for pod in pods.items:

        if agent["name"] in pod.metadata.name:

            found = True

            phase = pod.status.phase

            if phase == "Running":

                print_status(
                    True,
                    f"{pod.metadata.name} running"
                )

            else:

                print_status(
                    False,
                    f"{pod.metadata.name} state={phase}"
                )

    if not found:

        print_status(
            False,
            f"No pods found for {agent['name']}"
        )


# ==========================================
# CHECK SERVICE ACCOUNT
# ==========================================

def check_service_account(agent):

    deploy = apps_v1.read_namespaced_deployment(
        name=agent["name"],
        namespace=agent["namespace"]
    )

    sa = deploy.spec.template.spec.service_account_name

    if sa and sa != "default":

        print_status(
            True,
            f"{agent['name']} uses service account {sa}"
        )

    else:

        print_status(
            False,
            f"{agent['name']} using default service account"
        )


# ==========================================
# CHECK POD LOGS
# ==========================================

def check_logs(agent):

    pods = core_v1.list_namespaced_pod(
        namespace=agent["namespace"]
    )

    for pod in pods.items:

        if agent["name"] in pod.metadata.name:

            try:

                logs = core_v1.read_namespaced_pod_log(
                    name=pod.metadata.name,
                    namespace=agent["namespace"],
                    tail_lines=5
                )

                if logs:

                    print_status(
                        True,
                        f"{agent['name']} logs detected"
                    )

                else:

                    print_status(
                        False,
                        f"{agent['name']} no logs found"
                    )

            except Exception:

                print_status(
                    False,
                    f"{agent['name']} unable to read logs"
                )


# ==========================================
# PUBSUB VALIDATION
# ==========================================

def check_pubsub():

    try:

        cmd = [
            "gcloud",
            "pubsub",
            "subscriptions",
            "list"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print_status(
                True,
                "Pub/Sub reachable"
            )

        else:

            print_status(
                False,
                "Pub/Sub unreachable"
            )

    except Exception:

        print_status(
            False,
            "Pub/Sub validation failed"
        )


# ==========================================
# VERTEX TEST
# ==========================================

def check_vertex():

    try:

        import vertexai
        from vertexai.generative_models import (
            GenerativeModel
        )

        vertexai.init(
            project=PROJECT_ID,
            location="us-central1"
        )

        model = GenerativeModel(
            "gemini-1.5-flash"
        )

        response = model.generate_content(
            "Respond with: Vertex operational"
        )

        if "Vertex operational" in response.text:

            print_status(
                True,
                "Vertex AI operational"
            )

        else:

            print_status(
                False,
                "Unexpected Vertex response"
            )

    except Exception as e:

        print_status(
            False,
            f"Vertex validation failed: {str(e)}"
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print("\n==============================")
    print(" AGENT OPERATIONAL READINESS ")
    print("==============================\n")

    for agent in AGENTS:

        print(
            f"\n--- Checking {agent['name']} ---\n"
        )

        check_deployment(agent)
        check_pods(agent)
        check_service_account(agent)
        check_logs(agent)

    print("\n--- Shared Services ---\n")

    check_pubsub()
    check_vertex()

    print("\n==============================")
    print(" VALIDATION COMPLETE ")
    print("==============================\n")
```

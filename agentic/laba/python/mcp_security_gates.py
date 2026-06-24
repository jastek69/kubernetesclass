```python
import json
from kubernetes import client, config

# ==========================================
# LOAD KUBERNETES CONFIG
# ==========================================

config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
networking_v1 = client.NetworkingV1Api()

# ==========================================
# SETTINGS
# ==========================================

TARGET_NAMESPACE = "mcp"

REQUIRED_SECURITY_CONTEXT = [
    "runAsNonRoot",
    "readOnlyRootFilesystem"
]

# ==========================================
# HELPERS
# ==========================================

def print_result(check, status, details):
    result = {
        "check": check,
        "status": status,
        "details": details
    }

    print(json.dumps(result))


# ==========================================
# CHECK 1
# Namespace Exists
# ==========================================

def check_namespace():

    namespaces = v1.list_namespace()

    found = False

    for ns in namespaces.items:
        if ns.metadata.name == TARGET_NAMESPACE:
            found = True

    if found:
        print_result(
            "namespace_exists",
            "PASS",
            f"{TARGET_NAMESPACE} namespace exists"
        )
    else:
        print_result(
            "namespace_exists",
            "FAIL",
            f"{TARGET_NAMESPACE} namespace missing"
        )


# ==========================================
# CHECK 2
# Default Service Account Usage
# ==========================================

def check_service_accounts():

    deployments = apps_v1.list_namespaced_deployment(
        TARGET_NAMESPACE
    )

    for deploy in deployments.items:

        sa = deploy.spec.template.spec.service_account_name

        if sa == "default" or sa is None:
            print_result(
                "service_account",
                "FAIL",
                f"{deploy.metadata.name} uses default service account"
            )
        else:
            print_result(
                "service_account",
                "PASS",
                f"{deploy.metadata.name} uses {sa}"
            )


# ==========================================
# CHECK 3
# Privileged Containers
# ==========================================

def check_privileged():

    deployments = apps_v1.list_namespaced_deployment(
        TARGET_NAMESPACE
    )

    for deploy in deployments.items:

        containers = deploy.spec.template.spec.containers

        for container in containers:

            sc = container.security_context

            if sc and sc.privileged:
                print_result(
                    "privileged_container",
                    "FAIL",
                    f"{container.name} is privileged"
                )
            else:
                print_result(
                    "privileged_container",
                    "PASS",
                    f"{container.name} not privileged"
                )


# ==========================================
# CHECK 4
# Security Context
# ==========================================

def check_security_context():

    deployments = apps_v1.list_namespaced_deployment(
        TARGET_NAMESPACE
    )

    for deploy in deployments.items:

        containers = deploy.spec.template.spec.containers

        for container in containers:

            sc = container.security_context

            if not sc:
                print_result(
                    "security_context",
                    "FAIL",
                    f"{container.name} missing securityContext"
                )
                continue

            missing = []

            if sc.run_as_non_root is not True:
                missing.append("runAsNonRoot")

            if sc.read_only_root_filesystem is not True:
                missing.append("readOnlyRootFilesystem")

            if missing:
                print_result(
                    "security_context",
                    "FAIL",
                    f"{container.name} missing: {missing}"
                )
            else:
                print_result(
                    "security_context",
                    "PASS",
                    f"{container.name} hardened"
                )


# ==========================================
# CHECK 5
# Resource Limits
# ==========================================

def check_resource_limits():

    deployments = apps_v1.list_namespaced_deployment(
        TARGET_NAMESPACE
    )

    for deploy in deployments.items:

        containers = deploy.spec.template.spec.containers

        for container in containers:

            resources = container.resources

            if (
                not resources
                or not resources.limits
            ):

                print_result(
                    "resource_limits",
                    "FAIL",
                    f"{container.name} missing limits"
                )

            else:

                print_result(
                    "resource_limits",
                    "PASS",
                    f"{container.name} has limits"
                )


# ==========================================
# CHECK 6
# Latest Image Tag
# ==========================================

def check_latest_tag():

    deployments = apps_v1.list_namespaced_deployment(
        TARGET_NAMESPACE
    )

    for deploy in deployments.items:

        containers = deploy.spec.template.spec.containers

        for container in containers:

            image = container.image

            if ":latest" in image:

                print_result(
                    "latest_tag",
                    "FAIL",
                    f"{container.name} uses latest tag"
                )

            else:

                print_result(
                    "latest_tag",
                    "PASS",
                    f"{container.name} pinned image tag"
                )


# ==========================================
# CHECK 7
# Network Policies
# ==========================================

def check_network_policies():

    policies = networking_v1.list_namespaced_network_policy(
        TARGET_NAMESPACE
    )

    if len(policies.items) == 0:

        print_result(
            "network_policy",
            "FAIL",
            "No network policies found"
        )

    else:

        print_result(
            "network_policy",
            "PASS",
            f"{len(policies.items)} policies present"
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print("\n=== MCP SECURITY GATES ===\n")

    check_namespace()
    check_service_accounts()
    check_privileged()
    check_security_context()
    check_resource_limits()
    check_latest_tag()
    check_network_policies()

    print("\n=== SECURITY REVIEW COMPLETE ===\n")
```

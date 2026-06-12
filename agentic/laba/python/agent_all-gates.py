#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys


GREEN = "✅"
YELLOW = "⚠️"
RED = "❌"


def run(cmd, json_output=False):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout.strip()
        error = result.stderr.strip()

        if json_output and output:
            return result.returncode, json.loads(output), error

        return result.returncode, output, error

    except Exception as e:
        return 1, "", str(e)


def print_gate(name):
    print("\n" + "=" * 70)
    print(f"GATE: {name}")
    print("=" * 70)


def pass_msg(msg):
    print(f"{GREEN} {msg}")


def warn_msg(msg):
    print(f"{YELLOW} {msg}")


def fail_msg(msg):
    print(f"{RED} {msg}")


def check_gcloud():
    print_gate("gcloud authentication")

    rc, account, err = run(["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"])

    if rc == 0 and account:
        pass_msg(f"Active gcloud account: {account}")
        return True

    fail_msg("No active gcloud account found.")
    print(err)
    return False


def check_project(project_id):
    print_gate("GCP project configuration")

    rc, active_project, err = run(["gcloud", "config", "get-value", "project"])

    if active_project == project_id:
        pass_msg(f"Active project is correct: {project_id}")
        return True

    warn_msg(f"Active project is '{active_project}', expected '{project_id}'")
    print(f"Fix with: gcloud config set project {project_id}")
    return False


def check_cloud_build(project_id):
    print_gate("Cloud Build recent status")

    rc, output, err = run([
        "gcloud", "builds", "list",
        "--project", project_id,
        "--limit", "3",
        "--format=value(id,status,images)"
    ])

    if rc != 0:
        fail_msg("Unable to query Cloud Build.")
        print(err)
        return False

    if not output:
        warn_msg("No recent Cloud Build jobs found.")
        return False

    print(output)

    if "SUCCESS" in output.splitlines()[0]:
        pass_msg("Most recent Cloud Build completed successfully.")
        return True

    fail_msg("Most recent Cloud Build did not succeed.")
    print("Inspect with:")
    print("gcloud builds log <BUILD_ID>")
    return False


def check_artifact_tag(image_uri):
    print_gate("Artifact Registry image tag")

    base_image = image_uri.split(":")[0]

    rc, output, err = run([
        "gcloud", "artifacts", "docker", "tags", "list",
        base_image
    ])

    if rc != 0:
        fail_msg("Could not list Artifact Registry tags.")
        print(err)
        return False

    print(output)

    tag = image_uri.split(":")[-1] if ":" in image_uri else "latest"

    if tag in output:
        pass_msg(f"Tag exists: {tag}")
        return True

    fail_msg(f"Tag not found: {tag}")
    return False


def check_cluster(cluster, zone):
    print_gate("GKE cluster access")

    rc, output, err = run([
        "gcloud", "container", "clusters", "describe", cluster,
        "--zone", zone,
        "--format=value(name)"
    ])

    if rc == 0 and output == cluster:
        pass_msg(f"Cluster exists and is reachable: {cluster}")
        return True

    fail_msg("Unable to describe GKE cluster.")
    print(err)
    return False


def check_node_sa_artifact_reader(project_id, cluster, zone):
    print_gate("Node service account Artifact Registry access")

    rc, node_sa, err = run([
        "gcloud", "container", "clusters", "describe", cluster,
        "--zone", zone,
        "--format=value(nodeConfig.serviceAccount)"
    ])

    if rc != 0 or not node_sa:
        fail_msg("Could not determine node service account.")
        print(err)
        return False

    pass_msg(f"Node service account: {node_sa}")

    rc, roles, err = run([
        "gcloud", "projects", "get-iam-policy", project_id,
        "--flatten=bindings[].members",
        f"--filter=bindings.members:serviceAccount:{node_sa}",
        "--format=value(bindings.role)"
    ])

    if "roles/artifactregistry.reader" in roles:
        pass_msg("Node service account has roles/artifactregistry.reader")
        return True

    fail_msg("Node service account is missing roles/artifactregistry.reader")
    print("Fix with:")
    print(f"gcloud projects add-iam-policy-binding {project_id} \\")
    print(f'  --member="serviceAccount:{node_sa}" \\')
    print('  --role="roles/artifactregistry.reader"')
    return False


def check_deployment(namespace, deployment, expected_image):
    print_gate("Kubernetes Deployment image")

    rc, data, err = run([
        "kubectl", "get", "deployment", deployment,
        "-n", namespace,
        "-o", "json"
    ], json_output=True)

    if rc != 0:
        fail_msg(f"Deployment not found: {deployment}")
        print(err)
        return False

    containers = data["spec"]["template"]["spec"].get("containers", [])
    images = [c.get("image") for c in containers]

    print("Deployment images:")
    for image in images:
        print(f"  {image}")

    if expected_image in images:
        pass_msg("Deployment is using the expected image.")
        return True

    warn_msg("Deployment image does not exactly match expected image.")
    print(f"Expected: {expected_image}")
    return False


def check_ksa_annotation(namespace, ksa, expected_gsa):
    print_gate("Kubernetes Service Account annotation")

    rc, data, err = run([
        "kubectl", "get", "sa", ksa,
        "-n", namespace,
        "-o", "json"
    ], json_output=True)

    if rc != 0:
        fail_msg(f"Kubernetes service account not found: {ksa}")
        print(err)
        return False

    annotations = data.get("metadata", {}).get("annotations", {})
    actual = annotations.get("iam.gke.io/gcp-service-account")

    print(f"Expected GSA: {expected_gsa}")
    print(f"Actual annotation: {actual}")

    if actual == expected_gsa:
        pass_msg("KSA annotation is correct.")
        return True

    fail_msg("KSA annotation is incorrect or malformed.")
    print("Fix with:")
    print(f"kubectl annotate serviceaccount {ksa} \\")
    print(f"  --namespace {namespace} \\")
    print(f"  iam.gke.io/gcp-service-account={expected_gsa} \\")
    print("  --overwrite")
    return False


def check_workload_identity_binding(project_id, namespace, ksa, gsa):
    print_gate("Workload Identity IAM binding")

    expected_member = f"serviceAccount:{project_id}.svc.id.goog[{namespace}/{ksa}]"

    rc, policy, err = run([
        "gcloud", "iam", "service-accounts", "get-iam-policy", gsa,
        "--format=json"
    ], json_output=True)

    if rc != 0:
        fail_msg("Could not read GSA IAM policy.")
        print(err)
        return False

    for binding in policy.get("bindings", []):
        if binding.get("role") == "roles/iam.workloadIdentityUser":
            if expected_member in binding.get("members", []):
                pass_msg("Workload Identity binding is correct.")
                return True

    fail_msg("Workload Identity binding missing.")
    print("Expected member:")
    print(expected_member)
    print("Fix with:")
    print(f"gcloud iam service-accounts add-iam-policy-binding {gsa} \\")
    print('  --role="roles/iam.workloadIdentityUser" \\')
    print(f'  --member="{expected_member}"')
    return False


def check_pods(namespace, app_label):
    print_gate("Pod status")

    rc, data, err = run([
        "kubectl", "get", "pods",
        "-n", namespace,
        "-l", f"app={app_label}",
        "-o", "json"
    ], json_output=True)

    if rc != 0:
        fail_msg("Could not get pods.")
        print(err)
        return False

    pods = data.get("items", [])

    if not pods:
        fail_msg(f"No pods found with label app={app_label}")
        return False

    all_running = True

    for pod in pods:
        name = pod["metadata"]["name"]
        phase = pod["status"].get("phase")
        print(f"{name}: {phase}")

        container_statuses = pod["status"].get("containerStatuses", [])
        for status in container_statuses:
            state = status.get("state", {})
            if "waiting" in state:
                reason = state["waiting"].get("reason")
                warn_msg(f"{name} waiting: {reason}")
                all_running = False
            if "terminated" in state:
                reason = state["terminated"].get("reason")
                fail_msg(f"{name} terminated: {reason}")
                all_running = False

        if phase != "Running":
            all_running = False

    if all_running:
        pass_msg("All matching pods are Running.")
        return True

    warn_msg("One or more pods are not fully Running.")
    return False


def check_logs(namespace, deployment):
    print_gate("Recent application logs")

    rc, output, err = run([
        "kubectl", "logs",
        f"deployment/{deployment}",
        "-n", namespace,
        "--tail=50"
    ])

    if rc != 0:
        fail_msg("Could not read deployment logs.")
        print(err)
        return False

    print(output)

    known_errors = [
        "ModuleNotFoundError",
        "ImagePullBackOff",
        "ErrImagePull",
        "Forbidden",
        "PermissionDenied",
        "Unauthorized",
        "Annotated service account must be in format",
    ]

    for error in known_errors:
        if error in output:
            fail_msg(f"Detected known error in logs: {error}")
            return False

    pass_msg("No known fatal errors found in recent logs.")
    return True


def main():
    parser = argparse.ArgumentParser(description="SEIR Vertex Agent all-gates troubleshooting script")

    parser.add_argument("--project-id", default="seir-1-490120")
    parser.add_argument("--region", default="us-central1")
    parser.add_argument("--zone", default="us-central1-a")
    parser.add_argument("--cluster", default="primary")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--deployment", default="vertex-agent")
    parser.add_argument("--app-label", default="vertex-agent")
    parser.add_argument("--ksa", default="vertex-agent-ksa")
    parser.add_argument("--gsa", default="vertex-gke-agent@seir-1-490120.iam.gserviceaccount.com")
    parser.add_argument(
        "--image",
        default="us-central1-docker.pkg.dev/seir-1-490120/vertex-agent/lab1a:lab1a-latest"
    )

    args = parser.parse_args()

    results = []

    results.append(check_gcloud())
    results.append(check_project(args.project_id))
    results.append(check_cloud_build(args.project_id))
    results.append(check_artifact_tag(args.image))
    results.append(check_cluster(args.cluster, args.zone))
    results.append(check_node_sa_artifact_reader(args.project_id, args.cluster, args.zone))
    results.append(check_deployment(args.namespace, args.deployment, args.image))
    results.append(check_ksa_annotation(args.namespace, args.ksa, args.gsa))
    results.append(check_workload_identity_binding(args.project_id, args.namespace, args.ksa, args.gsa))
    results.append(check_pods(args.namespace, args.app_label))
    results.append(check_logs(args.namespace, args.deployment))

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r)
    total = len(results)

    print(f"Passed {passed}/{total} gates.")

    if passed == total:
        pass_msg("All gates passed. Vertex Agent infrastructure looks healthy.")
        sys.exit(0)

    fail_msg("One or more gates failed. Review the failed section above.")
    sys.exit(1)


if __name__ == "__main__":
    main()

from kubernetes import client, config
import re

# Initialize Kubernetes client
config.load_kube_config()
v1 = client.CoreV1Api()


def check_kubernetes_logs(pod_name, namespace):
    logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)

    issues = {
        "error": [],
        "warning": [],
        "info": [],  # Collect information that might indicate near-future problems
    }

    patterns = {
        "error": re.compile(r"error|exception|fatal", re.IGNORECASE),
        "warning": re.compile(r"warning|deprecated|slow", re.IGNORECASE),
        "info": re.compile(r"retrying|reconnecting|allocated", re.IGNORECASE),
    }

    for line in logs.split("\n"):
        for level, pattern in patterns.items():
            if pattern.search(line):
                issues[level].append(line)

    return issues


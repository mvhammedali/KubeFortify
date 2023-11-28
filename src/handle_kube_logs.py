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

def check_pod_health(namespace):
    # check if the pods are working properly
    pods = v1.list_namespaced_pod(namespace)
    first_pod = pods.items[0]
    pod_name = first_pod.metadata.name
    pod_status = v1.read_namespaced_pod(name=pod_name, namespace=namespace).status

    for line in logs.split("\n"):
        for level, pattern in patterns.items():
            if pattern.search(line):
                issues[level].append(line)
    for container in pod_status.container_statuses:
        print(f"Container Name: {container.name}")
        print(f"Restart count: {container.restart_count}")
        if container.restart_count > 3:
            return("Unhealthy pods detected:", [pod_name])

        else:
            return("Healthy pods!")
from kubernetes import client, config

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Kubernetes client
config.load_kube_config()
v1 = client.CoreV1Api()

def fetch_pod_logs(namespace):
    # fetch logs in pod
    pods = v1.list_namespaced_pod(namespace)
    if pods.items:
        first_pod = pods.items[0]
        pod_name = first_pod.metadata.name 
        log = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        return log
    else:
        print("No pods found in the namespace.")

def check_pod_errors():
    log_error = fetch_pod_logs(namespace=os.getenv('NAMESPACE'))    
    if log_error:
        # If an error is found, extract the last 700 characters from the log
        print("Error found in logs:")
        return log_error
    else:
        return None

def check_pod_health(namespace):
    # check if the pods are working properly
    pods = v1.list_namespaced_pod(namespace)
    first_pod = pods.items[0]
    pod_name = first_pod.metadata.name
    pod_status = v1.read_namespaced_pod(name=pod_name, namespace=namespace).status

    for container in pod_status.container_statuses:
        print(f"Container Name: {container.name}")
        print(f"Restart count: {container.restart_count}")
        if container.restart_count > 3:
            return("Unhealthy pods detected:", [pod_name])

        else:
            return("Healthy pods!")
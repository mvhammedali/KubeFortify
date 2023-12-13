from kubernetes import client, config
from src.mailer import send_email, get_solution
from src.handle_kube_logs import check_kubernetes_logs
import re

config.load_kube_config()
v1 = client.CoreV1Api()


def stop_all_pods(namespace="default"):
    pods = v1.list_namespaced_pod(namespace)
    for pod in pods.items:
        try:
            print(f"Deleting pod {pod.metadata.name}")
            v1.delete_namespaced_pod(pod.metadata.name, namespace)
        except client.exceptions.ApiException as e:
            print(f"Failed to delete pod {pod.metadata.name}: {str(e)}")


def resilience_test(url, namespace="default"):
    print("Stopping all pods in the namespace.")
    stop_all_pods(namespace)

    print("Waiting for the system to stabilize...")
    import time

    time.sleep(60)  # Wait a minute to allow for pod recreation and system stabilization

    errors = check_kubernetes_logs(namespace)
    if errors:
        error_message = (
            "Errors detected in Kubernetes logs during resilience testing:\n"
        )
        error_message += "\n".join(f"Pod: {pod}, Error: {log}" for pod, log in errors)
        detailed_solutions = [get_solution(log) for _, log in errors]
        full_message = error_message + "\n\n" + "\n".join(detailed_solutions)
        send_email("Resilience Test Failure", full_message)
    else:
        send_email(
            "Resilience Test Success",
            "All pods were stopped and then recovered successfully.",
        )

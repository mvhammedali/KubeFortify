from kubernetes import client, config
from mailer import send_email, get_solution
from handle_kube_logs import fetch_pod_logs
import time
import os
from dotenv import load_dotenv

config.load_kube_config()
v1 = client.CoreV1Api()
load_dotenv()


def stop_all_pods(namespace="default"):
    pods = v1.list_namespaced_pod(namespace)
    for pod in pods.items:
        try:
            print(f"Deleting pod {pod.metadata.name}")
            v1.delete_namespaced_pod(pod.metadata.name, namespace)
        except client.exceptions.ApiException as e:
            print(f"Failed to delete pod {pod.metadata.name}: {str(e)}")


def resilience_test(namespace):
    print("Stopping all pods in the namespace.")
    stop_all_pods(namespace)

    print("Waiting for the system to stabilize...")

    time.sleep(30)  # Wait a minute to allow for pod recreation and system stabilization

    errors = fetch_pod_logs(namespace)
    if errors:
        mes = "Errors detected in Kubernetes logs during resilience testing❗❗❗:\n"
        error_message = mes + "\n" + errors
        # print(error_message)
        detailed_solutions = get_solution(error_message)
        full_message = error_message + "\n\n" + "\n" + detailed_solutions
        send_email("Resilience Test Failure", full_message)
    else:
        send_email(
            "Resilience Test Success",
            "All pods were stopped and then recovered successfully.",
        )


if __name__ == "__main__":
    resilience_test(os.getenv("NAMESPACE"))

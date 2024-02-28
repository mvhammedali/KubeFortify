from kubernetes import client, config
from mailer import send_email, get_solution
import requests
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

config.load_kube_config()
v1 = client.CoreV1Api()


def send_requests(url, amount):
    # config.load_kube_config()  # Use load_incluster_config() if running inside a Kubernetes cluster

    # Create a CoreV1Api client instance to interact with Kubernetes API
    v1 = client.CoreV1Api()

    with requests.Session() as session:
        for _ in range(amount):
            try:
                response = session.get(url)
                print(response.status_code)

                if response.status_code != 200:
                    # Assuming you're working within a specific namespace; otherwise adjust this
                    namespace = os.getenv("NAMESPACE")
                    # List all pods in the specified namespace
                    pods = v1.list_namespaced_pod(namespace)

                    if pods.items:
                        # Get the first pod (make sure it's running if needed by checking status)
                        first_pod = pods.items[0]
                        # Get the logs of the first pod
                        logs = v1.read_namespaced_pod_log(name=first_pod.metadata.name, namespace=namespace)
                        print("Logs from the first pod:", first_pod.metadata.name)
                        print(logs)
                    else:
                        print("No pods found in the namespace.")

            except requests.exceptions.ConnectionError as e:
                print("Failed to connect to the site. Stopping the test.")
                break  # Stops the loop if the site is unreachable

            except Exception as e:
                print("An error occurred:", e)
                break


url = os.getenv("LOAD_URL")  # put the url here
amount = 1000  # Number of requests to send


def main(url, namespace):
    print("Starting load test...")

    send_requests(url, amount)
    pods = v1.list_namespaced_pod(namespace)
    first_pod = pods.items[0]
    pod_name = first_pod.metadata.name
    pod_status = v1.read_namespaced_pod(name=pod_name, namespace=namespace).status.container_statuses

    print("Checking Kubernetes logs for errors...")
    errors = pod_status
    print (errors)
    if errors:
        error_message = "Errors detected in Kubernetes logs during load testing:\n"
        
        solution = get_solution(errors)
           
        full_message = error_message + "\n\n" + errors +"\n"+solution
        print(full_message)
        send_email("Load Test Failure", full_message)
        print("Email with error details and solutions sent.")
    else:
        print("No errors detected. System is stable.")
        send_email(
            "Load Test Success", "The load test completed successfully with no errors."
        )


if __name__ == "__main__":
    main(os.getenv("LOAD_URL"), os.getenv("NAMESPACE"))

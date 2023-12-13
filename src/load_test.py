from kubernetes import client, config
from src.mailer import send_email, get_solution
from src.handle_kube_logs import check_kubernetes_logs
import requests

config.load_kube_config()
v1 = client.CoreV1Api()


def send_request(url):
    try:
        response = requests.get(url)
        print(f"Response Code: {response.status_code}, URL: {url}")
    except Exception as e:
        print(f"Error contacting {url}: {str(e)}")


def load_test(url, num_requests=100):
    for _ in range(num_requests):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Request failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


def main(url, namespace="default"):
    print("Starting load test...")
    load_test(url)

    print("Checking Kubernetes logs for errors...")
    errors = check_kubernetes_logs(namespace)
    if errors:
        error_message = "Errors detected in Kubernetes logs during load testing:\n"
        solutions = []
        for pod, log in errors:
            solution = get_solution(log)
            solutions.append(f"Pod: {pod}, Error: {log}, Solution: {solution}")

        full_message = error_message + "\n\n" + "\n\n".join(solutions)
        print(full_message)
        send_email("Load Test Failure", full_message)
        print("Email with error details and solutions sent.")
    else:
        print("No errors detected. System is stable.")
        send_email(
            "Load Test Success", "The load test completed successfully with no errors."
        )


if __name__ == "__main__":
    main("http://your-application-url", "your-namespace")

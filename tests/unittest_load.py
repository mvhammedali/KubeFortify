import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.load_test import send_requests, main 

class TestKubeFortify(unittest.TestCase):
    def setUp(self):
        # Patch the load_dotenv to do nothing
        patch('dotenv.load_dotenv', MagicMock(return_value=True)).start()

        # Mock os.getenv to return predefined values
        self.patcher = patch.dict(os.environ, {'NAMESPACE': 'test-namespace', 'LOAD_URL': 'http://test-url.com'})
        self.patcher.start()

        # Mock Kubernetes client
        self.mock_client = patch('kubernetes.client.CoreV1Api').start()

        # Mock requests
        self.mock_requests = patch('requests.Session').start()

    def tearDown(self):
        patch.stopall()
        self.patcher.stop()

    def test_send_requests_success(self):
        # Configure the mock session to simulate successful HTTP calls
        session_instance = self.mock_requests.return_value.__enter__.return_value
        session_instance.get.return_value.status_code = 200

        # Call the function
        send_requests('http://test-url.com', 1)

        # Assert the successful request was made
        self.assertTrue(session_instance.get.called)
        print("Test for successful requests passed.")

    def test_send_requests_failure_and_recovery(self):
        # Configure mocks
        session_instance = self.mock_requests.return_value.__enter__.return_value
        session_instance.get.return_value.status_code = 500  # Simulate failure
        self.mock_client.return_value.list_namespaced_pod.return_value.items = [MagicMock()]

        # Call the function
        send_requests('http://test-url.com', 1)

        # Check if Kubernetes API was called to fetch pods
        self.assertTrue(self.mock_client.return_value.list_namespaced_pod.called)
        print("Test for handling request failure and attempting recovery passed.")

    def test_main_function_email_sending(self):
        # Assume all other functions work as expected, focus on email sending logic
        with patch('your_script.send_email') as mock_send_email, \
             patch('your_script.get_solution', return_value="Mocked Solution"), \
             patch('your_script.send_requests') as mock_send_requests:
            main('http://test-url.com', 'test-namespace')
            mock_send_email.assert_called_once()
            print("Test for main function's email sending passed.")

# Run tests
if __name__ == '__main__':
    unittest.main()

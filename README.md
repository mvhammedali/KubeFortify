# KubeFortify

KubeFortify is a tool designed to ensure the resilience and performance of applications deployed on Kubernetes. It integrates load testing, resilience testing, and automated recovery processes into a single framework, leveraging AI to analyze issues and recommend solutions. KubeFortify aims to enhance system reliability and operational efficiency.
KubeFortify is tailored for organizations that rely on Kubernetes for application deployment and require an easy-to-use tool to maintain service quality and uptime. Its integrated approach to testing and recovery makes it a relevant tool in the toolkit of DevOps teams and site reliability engineers.

## Key Features
1. **Load Testing**: Simulates high traffic and usage scenarios to evaluate the performance limits and scalability of Kubernetes-managed applications.
2. **Resilience Testing**: Introduces faults into the system to assess the robustness and fault tolerance of the deployment, ensuring that the application can handle and recover from unexpected conditions.
3. **Automated Recovery**: Monitors the deployment status post-failure and automatically attempts recovery actions if the system does not return to the desired state, ensuring minimal downtime.
4. **AI-Driven Issue Resolution**: Utilizes OpenAI’s GPT to generate insights and practical solutions when problems are detected, enhancing the decision-making process during incident management.
5. **Email Notifications**:  Send detailed alerts on the issue that occurred during the test and the solution gotten from GPT.
   
## How to use
1. If you already have Python installed you can now install the requirements.
```bash
make install
```
2. After installations, create the environment variables in `.env` file in the `src` directory and populate with the appropriate details as you see in `.env_example`.
3. Now you can run the tests.
    Here are the `make` commands available (`make help`):
    ```bash
    Make targets:
    =============
    clean                Clean up .pyc files and __pycache__ directories
    install              Install Python dependencies needed for the tests
    load-test            Run the load testing script
    resilience-test      Run the resilience testing script
    ```

A failed test will look something like this:
![2024-04-25_23-32](https://github.com/mvhammedali/KubeFortify/assets/101676470/1cec9052-c757-43f6-b0d4-175fe70de034)

# DockerApp

A simple Flask weather application demonstrating **Kubernetes deployment with minikube**. This project showcases how to containerize a web application and deploy it to a local Kubernetes cluster with proper scaling, health checks, and service exposure.

## Purpose

This project is designed to demonstrate Kubernetes deployment and steps to:

- Containerize a Flask web application
- Deploy applications to Kubernetes using manifests
- Configure services for external access
- Implement health checks and resource management
- Scale applications with multiple replicas
- Use minikube for local Kubernetes development

## The Weather App

The application provides weather forecasts using the U.S. National Weather Service API:

- **City-based Search**: Enter any U.S. city name
- **Current Weather**: Real-time temperature and conditions
- **Hourly Forecast**: 24-hour detailed predictions
- **7-Day Forecast**: Weekly outlook with high/low temperatures
- **Temperature Conversion**: Both Fahrenheit and Celsius

## Tech Stack

- **Application**: Python Flask web framework
- **Containerization**: Docker
- **Orchestration**: Kubernetes (minikube)
- **APIs**: National Weather Service + OpenStreetMap Nominatim

## Kubernetes Deployment

### Prerequisites

- **minikube** - Local Kubernetes cluster
- **kubectl** - Kubernetes command-line tool
- **Docker** - Container runtime
  - **macOS/Windows**: Docker Desktop
  - **Linux**: Docker Engine

### Installation

**macOS:**

```bash
brew install minikube
```

**Windows:**

```powershell
# Using Chocolatey
choco install minikube

# Or using winget
winget install Kubernetes.minikube

# Or download directly from: https://minikube.sigs.k8s.io/docs/start/
```

**Linux:**

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Deployment Steps

1. **Clone and navigate to the project**

   ```bash
   git clone <repository-url>
   cd DockerApp
   ```

2. **Start minikube cluster**

   ```bash
   minikube start
   ```

3. **Configure Docker to use minikube's Docker daemon**

   **macOS/Linux:**

   ```bash
   eval $(minikube docker-env)
   ```

   **Windows (PowerShell):**

   ```powershell
   minikube docker-env | Invoke-Expression
   ```

   **Windows (Command Prompt):**

   ```cmd
   @FOR /f "tokens=*" %i IN ('minikube docker-env') DO @%i
   ```

4. **Build the Docker image inside minikube**

   ```bash
   docker build -t weather-app:latest .
   ```

5. **Deploy the application to Kubernetes**

   ```bash
   kubectl apply -f k8s-deployment.yaml
   kubectl apply -f k8s-service.yaml
   ```

6. **Get the service URL and access the app**

   ```bash
   minikube service weather-app-service --url
   ```

   Open the returned URL in your browser.

   **Note**: On Windows, you may need to use the minikube IP instead of localhost. The command above will provide the correct URL for your platform.

### Verify Deployment

```bash
# Check pods are running
kubectl get pods

# Check service status
kubectl get services

# View application logs
kubectl logs deployment/weather-app
```

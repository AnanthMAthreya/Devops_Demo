# Devops_Demo

Project to demonstrate basic DevOps concepts: a small Flask app, unit tests with pytest, a Dockerfile, a Helm chart, and a GitHub Actions CI/CD pipeline that builds and pushes a Docker image.

## Summary

This repository contains:
- app.py — a minimal Flask application with a root endpoint (`/`) and a health endpoint (`/healthz`).
- test_app.py — pytest unit tests for the app.
- Dockerfile — container image definition.
- requirements.txt — runtime (and dev) dependencies.
- flask-chart/ — Helm chart for deploying the app to Kubernetes.
- .github/workflows/build.yml — GitHub Actions CI that runs tests, builds and pushes the Docker image.

## Prerequisites

Install the following on your machine (Windows examples):

- Docker Desktop (with Docker CLI)
- Helm (v3+)
- kubectl
- kind or minikube (one of these to run a local cluster)
- Git
- (optional) Python 3.10+ and a virtual environment for local testing

## How the pipeline works

Pushing to the `main` branch triggers the GitHub Actions workflow `.github/workflows/build.yml`. The workflow:
1. Checks out the repo.
2. Sets up Python and installs dependencies.
3. Runs unit tests with pytest.
4. Logs in to Docker Hub using repo secrets.
5. Builds the Docker image and pushes it to Docker Hub (tagged with commit SHA).

Make sure you set these GitHub repository secrets:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Quick local test (without Kubernetes)

1. Create and activate a venv (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -U pip
   python -m pip install -r requirements.txt
   python -m pytest -q
   ```

2. Run the app locally:
   ```powershell
   python app.py
   # or
   python -m flask run --host=0.0.0.0 --port=5000
   ```

3. Test:
   ```powershell
   curl.exe -i http://localhost:5000/
   curl.exe -i http://localhost:5000/healthz
   ```

## Build and push Docker image (locally)

1. Build:
   ```powershell
   docker build -t your-dockerhub-username/devops_demo:latest .
   ```

2. Push:
   ```powershell
   docker login --username your-dockerhub-username
   docker push your-dockerhub-username/devops_demo:latest
   ```

## Deploy to a local cluster (kind) — full steps

1. Create a kind cluster:
   ```powershell
   kind create cluster --name devops-demo
   kubectl cluster-info --context kind-devops-demo
   ```

2. Install/upgrade Helm release (replace `your-dockerhub-username` and `tag` as needed):
   ```powershell
   helm install flask-release ./flask-chart
   ```
   
## Verify deployment & access the app

1. Check pods and services:
   ```powershell
   kubectl get pods
   kubectl get svc
   ```

2. Find your service name (example):
   ```powershell
   kubectl get svc -o wide
   ```

3. Port-forward to access the service locally:
   ```powershell
   # Replace <service-name> with the name shown by kubectl get svc
   kubectl port-forward svc/<service-name> 5000:5000
   ```

4. From another terminal run:
   ```powershell
   curl.exe -i http://localhost:5000/
   curl.exe -i http://localhost:5000/healthz
   ```

Expected:
- `/` returns 200 and includes the greeting.
- `/healthz` returns HTTP 200 (empty body or "OK" depending on configuration).

## Helm notes

- Edit `flask-chart/values.yaml` to set `image.repository` and `image.tag` to your image.
- `service.type` is set to `ClusterIP` in the chart. Use port-forwarding or expose via an Ingress if needed.
- Add liveness/readiness probes in `values.yaml`:
  ```yaml
  livenessProbe:
    httpGet:
      path: /healthz
      port: 5000
    initialDelaySeconds: 5
    periodSeconds: 10

  readinessProbe:
    httpGet:
      path: /healthz
      port: 5000
    initialDelaySeconds: 5
    periodSeconds: 10
  ```

## CI troubleshooting

- If tests fail in Actions, check the pytest output in the workflow logs.
- Ensure `requirements.txt` contains the test deps (or use a separate `requirements-dev.txt` and install it in the workflow).
- Make sure Docker Hub secrets are configured in the repository settings.

## Clean up

Remove the kind cluster:
```powershell
kind delete cluster --name devops-demo
```

Uninstall Helm release:
```powershell
helm uninstall flask-release
```

Remove local image (optional):
```powershell
docker rmi your-dockerhub-username/devops_demo:latest
```

---

This README provides the commands needed to set up a local cluster, deploy the Helm chart, run tests, and verify the app. Adjust repository names, image tags, and release names as appropriate for your environment.

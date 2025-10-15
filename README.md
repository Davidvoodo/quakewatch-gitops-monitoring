# 🌍 QuakeWatch GitOps Monitoring

## 📖 Overview
**QuakeWatch** is a lightweight Flask-based application designed to demonstrate full GitOps-based deployment and observability using **ArgoCD**, **Prometheus**, and **Grafana**.

This project showcases a complete modern DevOps lifecycle:
- Continuous deployment using **ArgoCD**
- Metrics exposure via **Prometheus instrumentation**
- Centralized monitoring using **Grafana**
- Service discovery using **ServiceMonitor**

---

## 🧱 Project Structure
quakewatch-gitops-monitoring/
├── app/ # Flask application (exposes /, /healthz, /metrics)
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
├── helm/
│ ├── quakewatch/ # Helm chart for deploying QuakeWatch
│ │ ├── Chart.yaml
│ │ ├── values.yaml
│ │ └── templates/
│ │ ├── deployment.yaml
│ │ ├── service.yaml
│ │ ├── ingress.yaml
│ │ └── servicemonitor.yaml
│ └── monitoring/ # (Managed via kube-prometheus-stack)
├── argocd/
│ └── apps/ # ArgoCD Application YAMLs
│ ├── 00-root-app.yaml
│ ├── 01-monitoring.yaml
│ └── 02-quakewatch.yaml
└── README.md



---

## 🚀 Deployment Flow (GitOps Pipeline)
1. **ArgoCD Root App** deploys both:
   - `monitoring` stack (Prometheus + Grafana + Alertmanager)
   - `quakewatch` app (Flask + ServiceMonitor)

2. **Prometheus** discovers and scrapes the app metrics using `ServiceMonitor`.

3. **Grafana** visualizes real-time metrics from Prometheus via a custom dashboard.

4. **Helm Charts** manage the deployment configurations for both apps.

---

## 🧩 Components

### 🔹 1. QuakeWatch Application
A simple Flask web app exposing Prometheus metrics:
```python
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    
    Exposed endpoints:

| Endpoint   | Description                 |
| ---------- | --------------------------- |
| `/`        | Basic status check          |
| `/healthz` | Liveness probe              |
| `/metrics` | Prometheus metrics endpoint |

Metrics example:
quakewatch_requests_total{endpoint="/"} 42
python_gc_collections_total{generation="0"} 103



🔹 2. ServiceMonitor (Integration with Prometheus)

servicemonitor.yaml ensures that Prometheus automatically discovers the app metrics.

spec:
  endpoints:
  - path: /metrics
    port: http
    interval: 30s
  selector:
    matchLabels:
      app.kubernetes.io/name: quakewatch

🔹 3. Monitoring Stack (Prometheus & Grafana)

Deployed via Helm chart:
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

After installation:

Prometheus UI → http://localhost:9090

Grafana UI → http://localhost:3000

(default user: admin, password retrieved from the secret monitoring-grafana)

To access Grafana locally:
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80

🔹 4. Grafana Dashboard

A custom dashboard (quakewatch-dashboard.json) visualizes:

Request rate per endpoint
rate(quakewatch_requests_total[1m]) by (endpoint)

Total requests per endpoint
quakewatch_requests_total

Steps to import:

In Grafana → “+ Create” → “Import”

Upload or paste the quakewatch-dashboard.json

Select your Prometheus data source

Click Import

📊 Validation Checklist
| Check                         | Command                                    | Expected Result                |
| ----------------------------- | ------------------------------------------ | ------------------------------ |
| **Pods running**              | `kubectl -n quakewatch get pods`           | 2 running pods                 |
| **ServiceMonitor active**     | `kubectl -n quakewatch get servicemonitor` | quakewatch (age > few minutes) |
| **Prometheus target up**      | `http://localhost:9090/targets`            | State = UP                     |
| **Grafana Dashboard visible** | Grafana UI                                 | Displays metrics charts        |


⚙️ Port Forwards Summary
| Component      | Command                                                                                  | Local URL                                      |
| -------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------- |
| Prometheus     | `kubectl -n monitoring port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090` | [http://localhost:9090](http://localhost:9090) |
| Grafana        | `kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80`                      | [http://localhost:3000](http://localhost:3000) |
| QuakeWatch App | `kubectl -n quakewatch port-forward svc/quakewatch 8081:80`                              | [http://localhost:8081](http://localhost:8081) |




👤 Maintainer

David Mizrahi
📧 davidvoodo@gmail.com

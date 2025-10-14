# QuakeWatch – Phase 4: GitOps & Monitoring

This repository demonstrates a complete end-to-end setup for **GitOps** and **Monitoring** using:

- **Argo CD** for Continuous Deployment (GitOps)
- **QuakeWatch** Flask app with Prometheus metrics endpoint
- **Helm** for application packaging
- **Prometheus + Grafana** monitoring stack (kube-prometheus-stack)
- **Docker** for containerization

---

## 0) Prerequisites
- A running Kubernetes (k3s/k8s) cluster accessible via `kubectl`
- Helm installed locally
- Docker Hub account for image pushing
- GitHub account and repo named `quakewatch-gitops-monitoring`

---

## 1) Build & Push Docker Image
From the `app/` folder:
```bash
docker build -t docker.io/david0mizrahi/quakewatch:1.0.0 .
docker push docker.io/david0mizrahi/quakewatch:1.0.0

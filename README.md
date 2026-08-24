# Learning Kubernetes — From Local to AWS EKS

Hands-on Kubernetes learning journey, from core concepts to cloud deployment.

> Status: work in progress — just getting started on Phase 1 (Core Concepts).

---

## What it does

Documents a step-by-step path through Kubernetes — Pods, Deployments, Services, and Namespaces on a local k3d cluster, then storage, health checks and autoscaling, then security fundamentals (RBAC, NetworkPolicy, Pod Security Standards), then Helm + monitoring — before moving to a real AWS EKS cluster provisioned with Terraform and deployed through a GitHub Actions CI/CD pipeline.

---

## Why I'm building it

6 years of SRE/Cloud Engineering background, but I'm returning to work after a 5-year break — this rebuilds the Kubernetes mental model from the ground up, phase by phase, instead of relying on rusty muscle memory. The roadmap deliberately mirrors what a real SRE/Cloud Engineer role needs in production: RBAC, NetworkPolicy, autoscaling, backup/restore, IaC — not just toy manifests.

---

## Stack

| Layer | Tool |
|---|---|
| Local cluster | k3d (k3s running inside Docker) |
| Container runtime | Docker Desktop |
| Local container registry | k3d registry (`k3d registry create`) |
| Cloud cluster | AWS EKS |
| Cloud registry | AWS ECR (public repo — 50 GB/month free) |
| App | Python (FastAPI) |
| Ingress / Traffic routing | Gateway API |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |

---

## Folder Structure

not available yet

---

## Installation

**Prerequisites:**

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — required as the container runtime for k3d
- [k3d](https://k3d.io/) — `choco install k3d` or download from the releases page
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/) — required from Phase 4 onwards

---

## How to Run

not available yet

---

## Roadmap

Detailed execution roadmap is in [ROADMAP.md](ROADMAP.md).

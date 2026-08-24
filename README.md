# Learning Kubernetes — From Local to AWS EKS

Hands-on Kubernetes learning journey, from core concepts to cloud deployment.

> Status: work in progress — Phase 1 (Core Concepts). Pod, Deployment, ReplicaSet, Rolling Update/Rollback, Service (+ CoreDNS), and Namespace done, currently on ConfigMap & Secret. See [ROADMAP.md](ROADMAP.md) for full progress.

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

Flat for now — manifests land at the root as each concept is learned, no subfolders yet.

```
learn-kubernetes-from-scratch/
├── pod-nginx.yaml          # first Pod manifest (Labels & Selectors)
├── deployment-nginx.yaml   # Deployment + ReplicaSet (Rolling Update & Rollback)
├── service-nginx.yaml      # ClusterIP Service (Service + CoreDNS)
├── .gitignore
├── README.md
└── ROADMAP.md
```

---

## Installation

**Prerequisites:**

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — required as the container runtime for k3d
- [k3d](https://k3d.io/) — `choco install k3d` or download from the releases page
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/) — required from Phase 4 onwards

---


## Troubleshooting

### `kubectl` times out connecting to `host.docker.internal` (Windows)

After `k3d cluster create`, `kubectl cluster-info` / `kubectl get nodes` hangs and fails with a `dial tcp ... connectex: ... failed to respond` error targeting `host.docker.internal:<port>`.

**Cause:** k3d writes the kubeconfig server address as `host.docker.internal`, which is meant to be resolved *from inside a container* back to the host machine. On Windows this hostname doesn't reliably resolve when `kubectl` runs directly on the host itself (outside a container).

**Confirm the cluster is actually fine** — find the mapped port for the `*-serverlb` container:

```
docker ps
```

Look for a line like `0.0.0.0:<PORT>->6443/tcp   k3d-<cluster-name>-serverlb`, then hit it directly:

```
curl.exe -k https://localhost:<PORT>/version
```

A `401 Unauthorized` JSON response is a good sign — the API server is alive and reachable, the client cert just wasn't sent. That confirms the problem is only the `host.docker.internal` address.

**Fix** — point the kubeconfig at `localhost` instead:

```
kubectl config set-cluster k3d-<cluster-name> --server=https://localhost:<PORT>
```

This patches only the `server` field for that cluster entry in the kubeconfig. Likely needs to be repeated after every `k3d cluster create`, since k3d writes `host.docker.internal` again by default.

---

## Roadmap

Detailed execution roadmap is in [ROADMAP.md](ROADMAP.md).

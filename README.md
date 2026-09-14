# Learning Kubernetes — From Local to AWS EKS

Hands-on Kubernetes learning journey, from core concepts to cloud deployment.

> Status: Phase 1 in progress.

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

```
learn-kubernetes-from-scratch/
├── manifests/                        # raw Kubernetes YAML manifests, numbered in the order they're applied
│   ├── 01-pod.yaml                    # reference only — superseded by the Deployment below, not applied to the cluster
│   ├── 02-deployment.yaml
│   ├── 03-service-clusterip.yaml
│   ├── 04-service-nodeport.yaml
│   └── 05-service-loadbalancer.yaml
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

### `kubectl` fails with "connection refused" after `k3d cluster create`

**Symptom:**

```
E0914 ... couldn't get current server API group list: Get "https://host.docker.internal:PORT/api?timeout=32s":
dial tcp <LAN IP>:PORT: connectex: No connection could be made because the target machine actively refused it.
```

`k3d cluster list` and `docker ps -a` both show the cluster's containers as running/healthy — this is not a cluster startup failure.

**Cause:** on this machine, `host.docker.internal` resolves to the real WiFi LAN IP (not a reachable loopback address), even though the k3d proxy container correctly maps the API port on `127.0.0.1`. Confirmed with:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port <PORT>              # succeeds
Test-NetConnection -ComputerName host.docker.internal -Port <PORT>   # fails
```

**Fix:** point kubeconfig at `127.0.0.1` instead of `host.docker.internal`. Needed every time the cluster is recreated, since k3d writes `host.docker.internal` into kubeconfig by default.

```powershell
kubectl config view --minify   # find the PORT and cluster name (e.g. k3d-dev-cluster)
kubectl config set-cluster k3d-<cluster-name> --server=https://127.0.0.1:<PORT>
```

### `Service` of type `LoadBalancer` stuck at `EXTERNAL-IP: <pending>`

**Symptom:** `kubectl get svc` shows `<pending>` indefinitely, and `kubectl get pods -A` shows a `svclb-<service-name>-xxxxx` Pod stuck `Pending` in `kube-system`.

**Cause:** k3d's built-in ServiceLB (Klipper LB) implements `LoadBalancer` by binding the Service's port directly as a `hostPort` on the Node. On a single-node cluster, every `LoadBalancer` Service competes for the same Node's ports — including k3s's default Traefik ingress controller, which claims ports `80`/`443` out of the box. `kubectl describe pod` on the stuck `svclb-*` Pod shows `FailedScheduling: ... node(s) didn't have free ports for the requested pod ports`.

Unlike a real cloud provider (e.g. AWS ELB), where each `LoadBalancer` Service gets its own dedicated external IP, k3d's ServiceLB reuses the single Node IP for all of them — so port collisions here are a local-dev limitation, not something that occurs in production.

**Fix (this project disables Traefik entirely, since traffic routing here goes through Gateway API instead):**

```powershell
k3d cluster delete dev-cluster
k3d cluster create dev-cluster --k3s-arg "--disable=traefik@server:0"
```

(Remember to re-apply the `host.docker.internal` fix above afterwards — it resets on every cluster recreation.)

If you need Traefik disabled but can't recreate the cluster, or hit the same conflict between two of your own `LoadBalancer` Services, use distinct ports per Service instead.

---

## Roadmap

Detailed execution roadmap is in [ROADMAP.md](ROADMAP.md).

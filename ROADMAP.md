# Roadmap — Learning Kubernetes

My execution plan for this project, broken into phases. I'll check items off as I go.

## Phase 1 — Kubernetes Local: Core Concepts `[LOCAL]`
> Understand core Kubernetes with hands-on practice

- [x] Install k3d and create a local cluster
- [x] Verify: `kubectl cluster-info` & `kubectl get nodes`
- [x] Pod, Node, Cluster — difference from plain Docker containers
- [x] First YAML manifest: deploy a simple Pod
- [x] Labels & Selectors — the glue that connects Deployment → Pod → Service
- [x] Deployment & ReplicaSet
- [x] Rolling Update & Rollback — `kubectl rollout status`, `kubectl rollout undo`
- [x] Service — ClusterIP, NodePort, LoadBalancer
- [x] Namespace — isolate dev/staging environments
- [ ] ConfigMap & Secret
- [ ] kubectl debugging — `logs`, `describe`, `exec`, `get events`

## Phase 2 — Kubernetes Local: Intermediate `[LOCAL]`
> Storage, health checks, autoscaling, observability

- [ ] Persistent Volume & PVC
- [ ] Startup, liveness & readiness probe
- [ ] Resource requests & limits
- [ ] Gateway API — GatewayClass, Gateway, HTTPRoute
- [ ] Metrics Server & `kubectl top`
- [ ] Horizontal Pod Autoscaler (HPA)
- [ ] Taints & Tolerations, Node Affinity/Anti-Affinity — control which node a Pod can (or can't) land on
- [ ] PodDisruptionBudget — keep the app up during voluntary disruption (node drain, cluster upgrade)
- [ ] Job & CronJob — batch tasks, scheduled cleanup (the Kubernetes equivalent of Linux cron)
- [ ] DaemonSet — run one Pod per node (how logging/monitoring agents are deployed)
- [ ] StatefulSet — PostgreSQL with automatic PVC

## Phase 3 — Kubernetes Security Fundamentals `[LOCAL]`
> RBAC, network isolation, and policy enforcement — security foundations that apply regardless of cloud provider

- [ ] RBAC — Role, RoleBinding, ClusterRole, ClusterRoleBinding
- [ ] ServiceAccount — least privilege, bound (expiring) tokens instead of long-lived legacy tokens
- [ ] Swap k3d's CNI to Calico — Flannel (k3d default) does not enforce NetworkPolicy
- [ ] NetworkPolicy — default-deny, then explicit allow rules between namespaces
- [ ] Pod Security Standards — `pod-security.kubernetes.io` Namespace labels, `restricted` profile (the official replacement for the removed PodSecurityPolicy)
- [ ] (Bonus) Kyverno or OPA Gatekeeper — enforce the Conventions section in README.md (no `:latest`, resource limits required) automatically via admission policy instead of by hand

## Phase 4 — Monitoring & Helm `[LOCAL]`
> Monitor the cluster and package manifests with Helm

- [ ] Helm: install, upgrade
- [ ] Build a custom Helm chart — FastAPI Todo API
- [ ] Deploy app via `helm install` to the dev namespace
- [ ] Multi-environment: `values-dev.yaml` (1 replica, HPA off) + `values-prod.yaml` (3 replicas, HPA on)
- [ ] Deploy Prometheus + Grafana via Helm (`kube-prometheus-stack`)
- [ ] Scrape FastAPI metrics — expose `/metrics` + ServiceMonitor
- [ ] Build a simple Grafana dashboard

## Phase 5 — AWS EKS `[CLOUD — PAID]`
> Deploy a production-grade cluster in the cloud

- [ ] EKS vs self-managed Kubernetes — what AWS manages vs what you manage
- [ ] Create EKS cluster with `eksctl` — node type `t3.small`
- [ ] IAM roles & service accounts — EKS Pod Identity (new approach) or IRSA (legacy)
- [ ] AWS Load Balancer Controller
- [ ] ECR — build, push & pull images (use public repo to avoid costs)
- [ ] EBS CSI Driver — persistent storage (default StorageClass: GP3)
- [ ] Cluster Autoscaler — scale nodes based on pending Pods (learn the concept first)
- [ ] Karpenter — migrate from Cluster Autoscaler
- [ ] Secrets Manager + External Secrets Operator
- [ ] Upgrade the cluster's Kubernetes minor version — practice via `eksctl`/EKS console, understand node group rolling upgrade and the version rollback window
- [ ] Velero — backup PV snapshots + cluster state to S3, then practice a restore

## Phase 6 — GitOps & CI/CD `[CLOUD]`
> Automate deployments like a real company

- [ ] GitHub Actions — auto build & push to ECR on git push
- [ ] CD pipeline to EKS via GitHub Actions
- [ ] Multi-environment pipeline (dev/staging/prod)
- [ ] (Bonus) ArgoCD — GitOps: cluster auto-syncs from Git

## Phase 7 — Infrastructure as Code (Terraform) `[CLOUD]`
> All infrastructure reproducible from code

- [ ] Terraform basics — resource, variable, output, state
- [ ] VPC with Terraform
- [ ] EKS cluster with Terraform
- [ ] Terraform modules
- [ ] Remote state in S3 + DynamoDB locking
- [ ] Full stack: VPC + EKS + RDS via Terraform


## Conventions

- Never use `:latest` image tag — always use a specific version (`:v1.0.0`)
- Never commit real Secret values — use `secret.yaml.example` as a template
- **Always delete the k3d cluster when not in use** — `k3d cluster delete dev-cluster` to free resources
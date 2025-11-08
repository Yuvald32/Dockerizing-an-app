# Helm Chart for Smart-Link Application

## Overview
This Helm chart deploys the Smart-Link Flask application to Kubernetes with configurable values for scalability and environment management.

## What Has Been Implemented
- ✅ Helm Chart structure (Chart.yaml, values.yaml)
- ✅ Kubernetes Deployment manifest with health probes
- ✅ Kubernetes Service (NodePort type)
- ✅ Kubernetes Ingress (optional, disabled by default)
- ✅ Configurable environment variables
- ✅ Readiness and Liveness probes
- ✅ Helper templates for consistent naming

## Chart Structure
helm-chart/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration values
├── .helmignore         # Files to ignore
└── templates/
├── _helpers.tpl    # Template helpers
├── deployment.yaml # Kubernetes Deployment
├── service.yaml    # Kubernetes Service
└── ingress.yaml    # Kubernetes Ingress (optional)

## How to Deploy

### Prerequisites
- Kubernetes cluster (Minikube, EKS, GKE, etc.)
- Helm 3.x installed
- kubectl configured

### Deployment Steps

#### Option 1: Deploy to Minikube
```bash
# 1. Start Minikube
minikube start

# 2. Navigate to helm-chart directory
cd helm-chart/

# 3. Lint the chart
helm lint .

# 4. Install/upgrade the release
helm upgrade --install smartlink . --namespace default

# 5. Verify deployment
kubectl get pods,svc
kubectl rollout status deployment/smartlink

# 6. Access the application
minikube service smartlink --url
```

#### Option 2: Deploy to Cloud Kubernetes
```bash
# 1. Ensure kubectl is configured for your cluster
kubectl config current-context

# 2. Install the chart
helm upgrade --install smartlink ./helm-chart \
  --namespace production \
  --create-namespace

# 3. Verify
kubectl get all -n production
```

### Customizing Values
```bash
# Deploy with custom values
helm upgrade --install smartlink ./helm-chart \
  --set image.tag=v0.2 \
  --set service.type=LoadBalancer \
  --set ingress.enabled=true
```

## Configuration Options

### Key Values in `values.yaml`

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Docker image repository | `shods/smartlink` |
| `image.tag` | Image tag | `v0.1` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Service type (NodePort/LoadBalancer/ClusterIP) | `NodePort` |
| `service.port` | Service port | `5001` |
| `containerPort` | Container port | `5001` |
| `ingress.enabled` | Enable ingress | `false` |
| `probes.initialDelaySeconds` | Probe initial delay | `5` |
| `env` | Environment variables | `TZ: Asia/Jerusalem` |

## Scaling Options

### Manual Scaling
```bash
# Scale replicas (requires updating deployment.yaml to use replicaCount)
kubectl scale deployment smartlink --replicas=3
```

### Future: Horizontal Pod Autoscaler
```yaml
# Add to values.yaml for HPA support
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## Health Checks
The chart includes:
- **Readiness Probe**: `/healthz` endpoint (initialDelay: 5s, period: 10s)
- **Liveness Probe**: `/healthz` endpoint (initialDelay: 5s, period: 10s)

## Testing the Deployment
```bash
# Check pod status
kubectl get pods -l app=smartlink

# Check service
kubectl get svc smartlink

# Port-forward for local testing
kubectl port-forward svc/smartlink 5001:5001

# Access at: http://localhost:5001

# View logs
kubectl logs -l app=smartlink --tail=50 -f
```

## Blockers
None. Chart deploys successfully on Minikube and cloud providers.

## Uninstalling
```bash
helm uninstall smartlink
```

## Notes
- Service type is `NodePort` for easy local development
- Change to `LoadBalancer` for cloud deployments with external IPs
- Ingress is disabled by default; enable for production with proper domain
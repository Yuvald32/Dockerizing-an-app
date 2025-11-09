# Terraform Configuration for Smart-Link Application

## Overview
This Terraform configuration deploys the Smart-Link application to a Kubernetes cluster using the Kubernetes provider. It provisions a namespace, deployment, and service.

## Implementation Note

This Terraform configuration deploys the application to Kubernetes rather than directly to EC2. This approach demonstrates:

1. **Modern cloud-native deployment** - Using Kubernetes for container orchestration
2. **Infrastructure as Code** - Provisioning K8s resources declaratively
3. **Consistency** - Same deployment method as Helm charts

### Alternative EC2 Approach (Not Implemented)

For direct EC2 deployment, the configuration would include:
```hcl
# EC2 Instance
resource "aws_instance" "app_server" {
  ami           = "ami-xxxxx"
  instance_type = "t2.micro"
  ...
}

# VPC and Networking
resource "aws_vpc" "main" { ... }
resource "aws_security_group" "app_sg" { ... }
```

**Reasoning for Kubernetes deployment:**
- Demonstrates container orchestration skills
- Aligns with Helm chart deployment method
- More scalable and production-ready approach
- Approved by instructor as valid alternative

## What Has Been Implemented
- ✅ Kubernetes namespace creation (`shods-app`)
- ✅ Kubernetes Deployment with Smart-Link container
- ✅ Kubernetes Service (NodePort type)
- ✅ Health probes (liveness and readiness)
- ✅ Environment variable configuration
- ✅ Output values for namespace and service name

## Infrastructure Components

### Resources Created
1. **Namespace**: `shods-app` - Isolated environment for the application
2. **Deployment**: `smartlink` - Manages pod lifecycle (1 replica)
3. **Service**: `smartlink-svc` - Exposes the application (NodePort)

## Prerequisites
- Terraform >= 1.3.0
- Kubernetes cluster running (Minikube, EKS, etc.)
- kubectl configured with valid kubeconfig
- Access to `~/.kube/config` file

## Project Structure
terraform/
├── main.tf              # Main Terraform configuration
└── .terraform.lock.hcl  # Provider version lock file

## How to Deploy

### Step 1: Initialize Terraform
```bash
cd terraform/

# Initialize providers and modules
terraform init
```

### Step 2: Review Plan
```bash
# See what will be created
terraform plan
```

### Step 3: Apply Configuration
```bash
# Deploy infrastructure
terraform apply

# Type 'yes' when prompted
```

### Step 4: Verify Deployment
```bash
# Check resources
kubectl get all -n shods-app

# Get service URL (Minikube)
minikube service smartlink-svc -n shods-app --url

# Port-forward for testing
kubectl port-forward -n shods-app svc/smartlink-svc 5001:5001
```

## Configuration Details

### Provider Configuration
```hcl
provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"  # Change for different clusters
}
```

**For different clusters:**
```bash
# List available contexts
kubectl config get-contexts

# Update main.tf with your context name
# For EKS: config_context = "arn:aws:eks:..."
# For GKE: config_context = "gke_project_zone_cluster"
```

### Deployment Specifications
- **Image**: `shods/smartlink:v0.1`
- **Replicas**: 1
- **Container Port**: 5001
- **Environment Variables**: `TZ=Asia/Jerusalem`
- **Probes**: 
  - Liveness: `/healthz` (5s initial delay, 10s period)
  - Readiness: `/healthz` (5s initial delay, 10s period)

### Service Specifications
- **Type**: NodePort (automatically assigned port 30000-32767)
- **Port**: 5001
- **Target Port**: 5001

## Outputs
```bash
# View outputs after apply
terraform output

# Outputs:
# - namespace: shods-app
# - service_name: smartlink-svc
```

## Modifying Configuration

### Change Number of Replicas
```hcl
# In main.tf, modify:
spec {
  replicas = 3  # Change from 1 to 3
}
```

### Change Service Type
```hcl
# In main.tf, modify:
spec {
  type = "LoadBalancer"  # Change from NodePort
}
```

### Update Image Version
```hcl
# In main.tf, modify:
container {
  image = "shods/smartlink:v0.2"  # Update version
}
```

Then re-apply:
```bash
terraform apply
```

## Testing the Infrastructure
```bash
# 1. Check Terraform state
terraform show

# 2. Verify Kubernetes resources
kubectl get namespace shods-app
kubectl get deployment -n shods-app
kubectl get service -n shods-app
kubectl get pods -n shods-app

# 3. Test application
curl $(minikube service smartlink-svc -n shods-app --url)

# 4. Check logs
kubectl logs -n shods-app -l app=smartlink
```

## Destroying Infrastructure
```bash
# Remove all Terraform-managed resources
terraform destroy

# Type 'yes' when prompted
```

## Blockers
None. Current configuration successfully deploys to Minikube.

## Alternative: Terraform for AWS Infrastructure

If deploying to AWS EC2 instead of Kubernetes, the configuration would include:
```hcl
# Future AWS resources
resource "aws_instance" "app_server" { ... }
resource "aws_security_group" "app_sg" { ... }
resource "aws_vpc" "main" { ... }
```

Currently focused on Kubernetes deployment as per project requirements.

## Notes
- Terraform state is stored locally (`.tfstate` file)
- For production, use remote state (S3 backend)
- Provider version is locked in `.terraform.lock.hcl`
- Change `config_context` based on your Kubernetes clusterx

# AWS Mini Dashboard – Dockerizing, Debugging & Kubernetes Deployment

This project is part of the DevOps course exam.  
It demonstrates how to:  
1. **Dockerize a Python Flask + boto3 application**  
2. Run and debug it on an **EC2 instance**  
3. Package and deploy it to **Kubernetes using Helm** for easier management and scalability.

---

## 📌 Project Overview
The application:
- Runs a **Flask web app** exposing port **5001**.
- Uses **boto3** to fetch data from AWS:
  - EC2 Instances
  - VPCs
  - Load Balancers (ALB/NLB)
  - AMIs (owned by self)
- Uses **IAM Role** with read-only permissions (on EC2) or **Kubernetes Secret** (in Minikube/Helm).

---

## 🐞 Section 3 – Dockerizing the Application
- Created a `Dockerfile` and `requirements.txt`.
- Built and ran the container on EC2.
- Application started, but crashed with a **NameError (`vpcs` not defined)**.

**Evidence:**
- Browser error screenshot: `evidence/section3-error-browser.png`
- Supporting files:
  - `evidence/docker-ps.txt`
  - `evidence/docker-images.txt`
  - `evidence/curl-status.txt`

---

## 🔧 Section 4 – Debugging & Fixing the Bug
- Fixed the bug in `app.py`:
  - Added calls to `describe_vpcs`, `describe_load_balancers`, `describe_images`.
  - Used safe `.get()` access to avoid crashes on missing fields.
- Rebuilt the Docker image and redeployed on EC2.
- Application now correctly lists **Instances, VPCs, Load Balancers, and AMIs**.

**Evidence:**
- Screenshot of fixed dashboard: `evidence/section4-dashboard-fixed.png`

---

## ☸️ Section 5 – Deploying to Kubernetes with Helm
- Created a **Helm Chart** (`flask-aws-monitor/`) with:
  - `Chart.yaml`, `values.yaml`
  - Templates: `deployment.yaml`, `service.yaml`, `ingress.yaml`, `_helpers.tpl`
- Configured:
  - Deployment with Docker image from Docker Hub
  - Service exposing port 5001
  - Optional Ingress resource
  - Kubernetes Secret for AWS credentials
  - Bonus: `ingress.enabled=true/false` toggle → Service type switches between **ClusterIP** and **LoadBalancer**
- Deployed to **Minikube** and verified with `helm upgrade --install` and `kubectl get pods,svc`.
- Accessed the app via `minikube service … --url`.

**Evidence:**
- Screenshots under `evidence/`:
  - Helm lint & install outputs
  - `kubectl get pods,svc`
  - Application dashboard running in browser
  - Bonus toggle (ClusterIP ↔ LoadBalancer)

---

## 📂 Repository Structure
├── app.py                     # Flask + boto3 app
├── Dockerfile                 # Docker build definition
├── requirements.txt           # Python dependencies
├── flask-aws-monitor/         # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── _helpers.tpl
├── evidence/                  # Evidence for Sections 3–5
│   ├── section3-error-browser.png
│   ├── section4-dashboard-fixed.png
│   ├── helm-install.png
│   ├── kubectl-get-pods.png
│   └── dashboard-minikube.png
└── README.md

---

## 🚀 How to Run

### Option A – Run with Docker on EC2
# 1. Connect to your EC2 instance via SSH

# 2. Clone the repository
git clone https://github.com/Yuvald32/Dockerizing-an-app.git
cd Dockerizing-an-app

# 3. Build the Docker image
docker build -t aws-dashboard:latest .

# 4. Run the container
docker run -d --name aws-dash -p 5001:5001 \
  -e AWS_DEFAULT_REGION=us-east-1 \
  aws-dashboard:latest

# 5. Open in browser:
# http://<EC2_PUBLIC_IP>:5001

### Option B – Run with Helm on Minikube (Demo mode, no real AWS data)
# 1. Start Minikube
minikube start

# 2. Navigate into the Helm chart
cd flask-aws-monitor

# 3. Lint and deploy
helm lint .
helm upgrade --install flask-monitor .

# 4. Verify resources
kubectl get pods,svc

# 5. Access in browser
minikube service flask-monitor-flask-aws-monitor --url

### Option B2 – Run with Helm on Minikube (Real AWS data)
# 1. Export AWS credentials as environment variables
export AWS_ACCESS_KEY_ID="<YOUR_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<YOUR_SECRET_ACCESS_KEY>"
export AWS_REGION="us-east-1"

# 2. Create or update a Kubernetes Secret from these variables
kubectl create secret generic flask-monitor-flask-aws-monitor-aws \
  --from-literal=AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  --from-literal=AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  --from-literal=AWS_REGION="$AWS_REGION" \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. Deploy the Helm chart
cd flask-aws-monitor
helm lint .
helm upgrade --install flask-monitor .

# 4. Verify deployment
kubectl rollout status deploy/flask-monitor-flask-aws-monitor
kubectl get pods,svc

# 5. Access in browser
minikube service flask-monitor-flask-aws-monitor --url

✅ Result
	•	Section 3: Bug reproduced.
	•	Section 4: Bug fixed; app works on EC2 (Docker).
	•	Section 5: App packaged as Helm chart and deployed on Kubernetes (Minikube).
	•	Bonus toggle implemented (Service type).
	•	Evidence included in evidence/.

⸻

👨‍💻 Author

Yuval Davidson
DevOps Course – John Bryce, 2025

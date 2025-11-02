# SHODS Smart-Link App

This project combines my two worlds — **music production** and **DevOps engineering**.

I’m **SHODS**, a music producer and sound designer who studied at **Rimon School of Music**,  
and this app is a bridge between my **final music project** at Rimon (producing Dana Maram’s debut EP)  
and my **final DevOps project** at John Bryce.

The web app is a **Flask-based Smart-Link** for the song **“מה אם?” by Dana Maram**,  
which I produced as part of the Rimon collaborations between songwriting and production students.  
It serves as a central landing page that showcases the song across platforms (Spotify, Apple Music, YouTube)  
with embedded players and a simple, elegant design.

The project is **fully containerized with Docker**, and prepared for deployment using **Helm** and **Terraform**  
to demonstrate modern CI/CD and cloud-native practices — bringing together creativity and infrastructure.

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

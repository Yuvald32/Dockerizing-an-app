# 🎵 SHODS Smart-Link App
### End-to-End DevOps Project | John Bryce Final Exam

<div align="center">

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white)

**A modern, cloud-native Smart-Link application combining music production and DevOps engineering**

[Live Demo](#) · [Report Bug](https://github.com/Yuvald32/Smart-Link-App/issues) · [Request Feature](https://github.com/Yuvald32/Smart-Link-App/issues)

</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Infrastructure Provisioning](#infrastructure-provisioning)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Features](#-features)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 About The Project

This project bridges two worlds: **music production** and **DevOps engineering**. 

As **SHODS**, a music producer and sound designer who studied at Rimon School of Music, this application serves as both:
- 🎼 A **Smart-Link landing page** for Dana Maram's debut song "מה אם?" (What If?)
- 🔧 A **comprehensive DevOps showcase** demonstrating containerization, orchestration, and CI/CD practices

The web app provides a centralized hub for the song across streaming platforms (Spotify, Apple Music, YouTube) while demonstrating modern cloud-native architecture and deployment methodologies.

### 🎓 Academic Context
- **Course:** End-to-End DevOps - John Bryce College
- **Year:** 2025
- **Instructor Approved:** Custom Flask application (alternative to AWS monitoring dashboard)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Request                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   Ingress      │
                    │  (Optional)    │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   Service      │
                    │  (NodePort)    │
                    └────────┬───────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌────────────────┐      ┌────────────────┐
        │   Pod 1        │      │   Pod 2        │
        │  (Flask App)   │      │  (Flask App)   │
        └────────────────┘      └────────────────┘
```

### Deployment Flow

```
Developer Push → GitHub → Jenkins Pipeline → Docker Build → 
Docker Hub → Helm Chart → Kubernetes Cluster → Production
```

---

## 🛠️ Tech Stack

### Application Layer
- **Backend:** Flask 3.0.0 (Python 3.13)
- **WSGI Server:** Gunicorn 22.0.0
- **Configuration:** PyYAML 6.0.2
- **Cloud SDK:** boto3 1.34.153

### Infrastructure & DevOps
- **Containerization:** Docker (multi-stage build)
- **Orchestration:** Kubernetes + Helm 3.x
- **IaC:** Terraform ~> 2.32
- **CI/CD:** Jenkins (Declarative Pipeline)
- **Registry:** Docker Hub

### Security & Quality
- **Linting:** flake8, hadolint, shellcheck
- **Security Scanning:** bandit, trivy
- **Health Checks:** Kubernetes liveness & readiness probes

---

## 📁 Project Structure

```
Smart-Link-App/
│
├── 📱 app/                        # Flask Application
│   ├── app.py                     # Main application logic
│   ├── requirements.txt           # Python dependencies
│   ├── links.yaml                 # Configuration file
│   ├── static/                    # CSS assets
│   ├── templates/                 # HTML templates
│   └── README.md                  # App documentation
│
├── 🐳 Dockerfile                  # Multi-stage Docker build
│
├── 🔄 ci-cd/                      # CI/CD Pipeline
│   ├── Jenkinsfile               # Jenkins declarative pipeline
│   └── README.md                 # Pipeline documentation
│
├── ⎈ helm-chart/                 # Kubernetes Helm Chart
│   ├── Chart.yaml                # Chart metadata
│   ├── values.yaml               # Configurable values
│   ├── templates/                # K8s manifests
│   │   ├── deployment.yaml       # Pod deployment
│   │   ├── service.yaml          # Service definition
│   │   ├── ingress.yaml          # Ingress rules (optional)
│   │   └── _helpers.tpl          # Template helpers
│   └── README.md                 # Helm documentation
│
├── 🏗️ terraform/                 # Infrastructure as Code
│   ├── main.tf                   # Terraform configuration
│   ├── .terraform.lock.hcl       # Provider lock file
│   └── README.md                 # Terraform documentation
│
├── 📜 .gitignore                 # Git ignore rules
├── 🐋 .dockerignore              # Docker ignore rules
└── 📖 README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop** or **Docker Engine** 20.10+
- **kubectl** 1.20+
- **Helm** 3.0+
- **Minikube** (for local K8s) or access to a K8s cluster
- **Terraform** 1.3.0+ (optional)
- **Python** 3.13+ (for local development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yuvald32/Smart-Link-App.git
   cd Smart-Link-App
   ```

2. **Set up Python environment**
   ```bash
   cd app/
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the app**
   ```
   Open browser: http://localhost:5001
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t smartlink:latest .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name smartlink \
     -p 5001:5001 \
     -e TZ=Asia/Jerusalem \
     smartlink:latest
   ```

3. **Verify health check**
   ```bash
   curl http://localhost:5001/healthz
   # Expected: {"status":"ok"}
   ```

4. **View logs**
   ```bash
   docker logs -f smartlink
   ```

5. **Stop and remove**
   ```bash
   docker stop smartlink
   docker rm smartlink
   ```

### Kubernetes Deployment

#### Using Helm (Recommended)

1. **Start Minikube**
   ```bash
   minikube start
   ```

2. **Deploy with Helm**
   ```bash
   cd helm-chart/
   helm lint .
   helm upgrade --install smartlink . --namespace default
   ```

3. **Verify deployment**
   ```bash
   kubectl get pods,svc
   kubectl rollout status deployment/smartlink
   ```

4. **Access the application**
   ```bash
   minikube service smartlink --url
   ```

5. **View logs**
   ```bash
   kubectl logs -l app=smartlink --tail=50 -f
   ```

#### Customizing Deployment

```bash
# Change service type to LoadBalancer
helm upgrade --install smartlink ./helm-chart \
  --set service.type=LoadBalancer

# Use different image tag
helm upgrade --install smartlink ./helm-chart \
  --set image.tag=v0.2

# Enable ingress
helm upgrade --install smartlink ./helm-chart \
  --set ingress.enabled=true
```

### Infrastructure Provisioning

#### Using Terraform

1. **Navigate to Terraform directory**
   ```bash
   cd terraform/
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Review the plan**
   ```bash
   terraform plan
   ```

4. **Apply configuration**
   ```bash
   terraform apply
   # Type 'yes' when prompted
   ```

5. **Verify resources**
   ```bash
   kubectl get all -n shods-app
   ```

6. **View outputs**
   ```bash
   terraform output
   ```

7. **Destroy infrastructure** (when done)
   ```bash
   terraform destroy
   ```

---

## 🔄 CI/CD Pipeline

The Jenkins pipeline automates the entire build, test, and deployment process:

### Pipeline Stages

1. **Checkout** - Clone repository from GitHub
2. **Parallel Checks** - Run simultaneously:
   - **Linting** (flake8, shellcheck, hadolint)
   - **Security Scanning** (bandit, trivy)
3. **Docker Build** - Build and tag images
4. **Security Scan** - Scan Docker image for vulnerabilities
5. **Push to Registry** - Upload to Docker Hub

### Pipeline Features

- ✅ Parallel execution for faster builds
- ✅ Mock mode for development without tools
- ✅ Credential management via Jenkins
- ✅ Build number tagging
- ✅ Automated security scanning
- ✅ Fail-fast on HIGH/CRITICAL vulnerabilities

### Running the Pipeline

```groovy
// In Jenkins UI
Parameters:
  - USE_MOCK: true (for mock mode)
           or false (for real scanning)

Credentials Required:
  - dockerhub (Username with password)
```

---

## ✨ Features

### Application Features
- 🎵 **Multi-platform Links** - Spotify, Apple Music, YouTube
- 🎬 **Embedded Players** - Spotify & YouTube iframes
- 🌐 **RTL Support** - Hebrew language support
- 📱 **Responsive Design** - Works on all devices
- ⚡ **Health Checks** - `/healthz` endpoint for monitoring
- 🔧 **YAML Configuration** - Easy content management

### DevOps Features
- 🐳 **Multi-stage Docker Build** - Optimized image size
- 🔒 **Non-root User** - Security best practices
- ⎈ **Kubernetes Ready** - Full Helm chart support
- 🏗️ **Infrastructure as Code** - Terraform provisioning
- 🔄 **CI/CD Pipeline** - Automated Jenkins workflow
- 🛡️ **Security Scanning** - Bandit + Trivy integration
- 📊 **Health Monitoring** - Liveness & readiness probes
- 🏷️ **Version Tagging** - Semantic versioning (v0.1, v0.2, etc.)

---

## 🗺️ Roadmap

- [x] Flask application development
- [x] Docker containerization
- [x] Jenkins CI/CD pipeline
- [x] Helm chart creation
- [x] Terraform infrastructure
- [x] Comprehensive documentation
- [ ] AWS EC2 deployment (alternative to K8s)
- [ ] Monitoring with Prometheus & Grafana
- [ ] Logging with ELK Stack
- [ ] GitOps with ArgoCD
- [ ] Multi-environment support (dev/staging/prod)
- [ ] Horizontal Pod Autoscaling
- [ ] SSL/TLS with cert-manager

---

## 🤝 Contributing

Contributions are what make the open source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

**Yuval Davidson (SHODS)**
- GitHub: [@Yuvald32](https://github.com/Yuvald32)
- Project Link: [https://github.com/Yuvald32/Smart-Link-App](https://github.com/Yuvald32/Smart-Link-App)

---

## 🙏 Acknowledgments

- **John Bryce College** - DevOps training and mentorship
- **Rimon School of Music** - Music production education
- **Dana Maram** - Artist collaboration
- **Docker** - Containerization platform
- **Kubernetes** - Container orchestration
- **HashiCorp** - Terraform infrastructure tooling
- **Jenkins** - Automation server
- **GitHub** - Version control and collaboration

---

<div align="center">

### 🌟 Star this repo if you found it helpful!

**Built with ❤️ by SHODS | Bridging Music & DevOps**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=Yuvald32.Smart-Link-App)
![GitHub last commit](https://img.shields.io/github/last-commit/Yuvald32/Smart-Link-App)
![GitHub repo size](https://img.shields.io/github/repo-size/Yuvald32/Smart-Link-App)

</div>

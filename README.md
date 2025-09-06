# AWS Mini Dashboard – Dockerizing & Debugging

This project is part of the DevOps course exam.  
It demonstrates how to **Dockerize a Python Flask + boto3 application**, run it on an **EC2 instance**, and fix a bug preventing the application from displaying AWS resources.

---

## 📌 Project Overview
The application:
- Runs a **Flask web app** exposing port **5001**.
- Uses **boto3** to fetch data from AWS:
  - EC2 Instances
  - VPCs
  - Load Balancers (ALB/NLB)
  - AMIs (owned by self)
- Uses **IAM Role** with read-only permissions (no static keys).

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

## 📂 Repository Structure
```
.
├── app.py               # Flask + boto3 app
├── Dockerfile           # Docker build definition
├── requirements.txt     # Python dependencies
├── evidence/            # Evidence for Section 3 & 4
│   ├── section3-error-browser.png
│   ├── section4-dashboard-fixed.png
│   ├── docker-ps.txt
│   ├── docker-images.txt
│   ├── curl-status.txt
│   └── ...
└── README.md
```

---

## 🚀 How to Run

### Prerequisites
- AWS EC2 instance (Amazon Linux 2023 / Ubuntu 22.04)
- IAM Role attached with:
  - `AmazonEC2ReadOnlyAccess`
  - `ElasticLoadBalancingReadOnly`

### Steps
```bash
# 1. Clone repo
git clone https://github.com/Yuvald32/Dockerizing-an-app.git
cd Dockerizing-an-app

# 2. Build docker image
docker build -t aws-dashboard:latest .

# 3. Run container
docker run -d --name aws-dash -p 5001:5001   -e AWS_DEFAULT_REGION=us-east-1   aws-dashboard:latest

# 4. Open in browser
http://<EC2_PUBLIC_IP>:5001
```

---

## ✅ Result
- **Section 3**: Verified the bug existed.  
- **Section 4**: Bug fixed, application runs successfully in Docker on EC2, listing AWS resources.  
- Evidence included in `evidence/`.

---

## 👨‍💻 Author
Yuval Davidson  
DevOps Course – John Bryce, 2025

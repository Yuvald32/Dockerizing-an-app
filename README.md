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

## 🧱 Run Locally
```bash
cd app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# Open http://localhost:5001
```

## 🐳 Run in Docker
```bash
docker build -t shods/smartlink:dev .
docker run -p 5001:5001 shods/smartlink:dev
# http://localhost:5001
```

## ⚙️ Health Check

The app exposes /healthz for Kubernetes readiness/liveness probes.

## 🧩 Helm & Terraform (Next Steps)
	•	Helm: update values.yaml → image.repository: shods/smartlink, image.tag: v0.1, containerPort: 5001
	•	Terraform: create main.tf with Kubernetes provider and a deployment manifest for this app.

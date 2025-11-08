# CI/CD Pipeline Configuration

## Overview
This directory contains the Jenkins pipeline configuration for automated building, testing, and deployment of the Smart-Link application.

## What Has Been Implemented
- ✅ Multi-stage Jenkins pipeline
- ✅ Parallel execution of linting and security scans
- ✅ Docker image build and push to Docker Hub
- ✅ Mock mode for development/testing without tools installed
- ✅ Credential management for Docker Hub
- ✅ Build number tagging for images
- ✅ Error handling and pipeline notifications

## Pipeline Structure

### Stages Overview
1. **Checkout** - Clone repository
2. **Parallel Checks** - Run linting and security scans simultaneously
   - Linting (flake8, shellcheck, hadolint)
   - Security Scan (bandit, trivy)
3. **Docker Build & Login** - Build and tag images
4. **Security Scan (Image)** - Scan built Docker image for vulnerabilities
5. **Push to Docker Hub** - Upload images to registry

## How to Use

### Prerequisites
- Jenkins server with Docker installed
- Docker Hub credentials configured in Jenkins
  - Credential ID: `dockerhub`
  - Type: Username with password
- Git repository access

### Setting Up Jenkins Credentials

1. Go to Jenkins → Manage Jenkins → Credentials
2. Add new credentials:
   - **Kind**: Username with password
   - **ID**: `dockerhub`
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password/token

### Running the Pipeline

#### Option 1: With Mock Tools (Faster, No Tools Required)
```groovy
// In Jenkins, set parameter:
USE_MOCK = true
```

#### Option 2: With Real Tools (Full Security Scanning)
```groovy
// In Jenkins, set parameter:
USE_MOCK = false
```

### Triggering Builds

#### Via Jenkins UI
1. Navigate to the pipeline job
2. Click "Build with Parameters"
3. Select `USE_MOCK` option
4. Click "Build"

#### Via Git Hook (Future)
```bash
# Configure webhook in GitHub
# Jenkins will auto-trigger on push to main/dev
```

## Pipeline Configuration

### Environment Variables
```groovy
environment {
  DOCKERHUB = credentials('dockerhub')  // Jenkins credential
  IMAGE = "${DOCKERHUB_USR}/smart-link-app"
  IMAGE_TAG = "${env.BUILD_NUMBER}"
  IMAGE_FULL = "${IMAGE}:${IMAGE_TAG}"
  IMAGE_LATEST = "${IMAGE}:latest"
}
```

### Build Parameters
- `USE_MOCK` (boolean): Run mock linting/security instead of real tools
  - Default: `true`
  - Set to `false` for production builds with full scanning

## Parallel Execution

The pipeline runs linting and security scans in parallel for faster execution:
┌─────────────┐     ┌──────────────────┐
│  Linting    │────▶│  Docker Build    │
└─────────────┘     └──────────────────┘
║                      │
┌─────────────┐              ▼
│ Security    │     ┌──────────────────┐
│   Scan      │────▶│  Push to Hub     │
└─────────────┘     └──────────────────┘

## Tools Used

### Linting Tools
- **flake8**: Python code linting
- **shellcheck**: Shell script analysis
- **hadolint**: Dockerfile linting

### Security Tools
- **bandit**: Python security vulnerability scanner
- **trivy**: Container image vulnerability scanner
  - Checks for LOW, MEDIUM, HIGH, and CRITICAL vulnerabilities
  - Fails pipeline on HIGH/CRITICAL issues

## Testing the Pipeline

### Manual Test
```bash
# 1. Push code to repository
git add .
git commit -m "test: CI/CD pipeline"
git push origin main

# 2. Trigger Jenkins build
# 3. Monitor console output
# 4. Verify image on Docker Hub
```

### Expected Output
✅ Checkout: SUCCESS
✅ Linting: SUCCESS (or MOCK)
✅ Security Scan: SUCCESS (or MOCK)
✅ Docker Build & Login: SUCCESS
✅ Security Scan (Image): SUCCESS (if not mock)
✅ Push to Docker Hub: SUCCESS
Image: <username>/smart-link-app:42
<username>/smart-link-app:latest

## Docker Hub Integration

### Image Tagging Strategy
- **Build number tag**: `shods/smart-link-app:42`
- **Latest tag**: `shods/smart-link-app:latest`

Both tags are pushed to Docker Hub on successful build.

### Pulling Images
```bash
# Pull latest
docker pull shods/smart-link-app:latest

# Pull specific build
docker pull shods/smart-link-app:42
```

## Error Handling

### Post-Build Actions
```groovy
post {
  always {
    sh 'docker logout || true'  // Always logout
  }
  success {
    echo "Done. Image: ${IMAGE_FULL}"
  }
  failure {
    echo 'Pipeline failed. Check above logs.'
  }
}
```

## Blockers
None. Pipeline executes successfully in both MOCK and real modes.

## Troubleshooting

### Issue: Docker login fails
```bash
# Solution: Verify credentials in Jenkins
# Ensure DOCKERHUB_USR and DOCKERHUB_PSW are accessible
```

### Issue: Trivy not found
```bash
# Solution: Use MOCK mode or install trivy
# Pipeline auto-installs if missing (requires sudo)
```

### Issue: Permission denied
```bash
# Solution: Ensure Jenkins user has Docker permissions
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

## Notes
- Mock mode is useful for development without installing all tools
- Real mode provides comprehensive security scanning
- Pipeline uses timestamps for better log readability
- All docker logout commands are safe-failed (|| true)
pipeline {
  agent any

  options {
    timestamps()
  }

  parameters {
    booleanParam(name: 'USE_MOCK', defaultValue: true, description: 'Run mock lint & security instead of real tools')
  }

  environment {
    // אלו שני ה-Credentials שכבר יצרת ב-Jenkins מסוג Username/Password
    DOCKERHUB_USERNAME = credentials('dockerhub-username')
    DOCKERHUB_PASSWORD = credentials('dockerhub-password')

    // שם התמונה ייגזר אוטומטית מה-username כדי שלא ניפול על טייפואים
    IMAGE = "${DOCKERHUB_USERNAME}/smart-link-app"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    IMAGE_FULL = "${IMAGE}:${IMAGE_TAG}"
    IMAGE_LATEST = "${IMAGE}:latest"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Parallel Checks') {
      parallel {
        stage('Linting') {
          steps {
            script {
              if (params.USE_MOCK) {
                sh '''
                  echo "MOCK Linting..."
                  echo "flake8 ."; echo "shellcheck **/*.sh"; echo "hadolint Dockerfile"
                '''
              } else {
                sh '''
                  python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
                  pip3 install flake8 bandit >/dev/null 2>&1 || true
                  # Dockerfile lint (hadolint) - נתקין בינארי קל
                  if ! command -v hadolint >/dev/null 2>&1; then
                    curl -sL https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 -o /usr/local/bin/hadolint
                    chmod +x /usr/local/bin/hadolint
                  fi
                  flake8 .
                  # אם יש סקריפטים
                  if ls *.sh >/dev/null 2>&1; then shellcheck *.sh; fi
                  hadolint Dockerfile
                '''
              }
            }
          }
        }

        stage('Security Scan') {
          steps {
            script {
              if (params.USE_MOCK) {
                sh '''
                  echo "MOCK Security scanning..."
                  echo "bandit -r ."; echo "trivy image ${IMAGE_FULL}"
                '''
              } else {
                sh '''
                  # Bandit לקוד פייתון
                  python3 -m pip install bandit >/dev/null 2>&1 || true
                  bandit -q -r .
                  # Trivy לסריקת התמונה (נריץ על ה-Workspace אם מותקן; אחרת נתקין בצורה מהירה)
                  if ! command -v trivy >/dev/null 2>&1; then
                    sudo rpm -q trivy || sudo rpm -Uvh --quiet https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.55.0_Linux-64bit.rpm || true
                  fi
                  echo "Trivy will scan after build stage on the built image"
                '''
              }
            }
          }
        }
      }
    }

    stage('Docker Build') {
      steps {
        sh '''
          echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
          docker build -t "${IMAGE_FULL}" -t "${IMAGE_LATEST}" .
        '''
      }
    }

    stage('Security Scan (Image)') {
      when { expression { return !params.USE_MOCK } }
      steps {
        sh '''
          trivy image --exit-code 0 --severity LOW,MEDIUM "${IMAGE_FULL}"
          trivy image --exit-code 1 --severity HIGH,CRITICAL "${IMAGE_FULL}" || {
            echo "High/Critical vulnerabilities found"; exit 1;
          }
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        sh '''
          docker push "${IMAGE_FULL}"
          docker push "${IMAGE_LATEST}"
        '''
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
    success {
      echo "Pipeline completed successfully. Pushed: ${IMAGE_FULL} and ${IMAGE_LATEST}"
    }
    failure {
      echo 'Pipeline failed. Check above logs.'
    }
  }
}
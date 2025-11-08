pipeline {
  agent any

  options { timestamps() }

  parameters {
    booleanParam(
      name: 'USE_MOCK',
      defaultValue: true,
      description: 'Run mock lint & security instead of real tools'
    )
  }

  environment {
    IMAGE_NAME = 'smart-link-app'          // שם התמונה בלי המשתמש
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sh '''
          echo "Commit: $(git rev-parse --short HEAD)"
        '''
      }
    }

    stage('Parallel Checks') {
      parallel {
        stage('Linting') {
          steps {
            script {
              if (params.USE_MOCK) {
                sh '''
                  echo "[MOCK] flake8 ."
                  echo "[MOCK] shellcheck **/*.sh"
                  echo "[MOCK] hadolint Dockerfile"
                '''
              } else {
                sh '''
                  python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
                  pip3 install -q flake8 bandit || true
                  if ! command -v hadolint >/dev/null 2>&1; then
                    curl -sL https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 -o /usr/local/bin/hadolint
                    chmod +x /usr/local/bin/hadolint
                  fi
                  flake8 .
                  if ls *.sh >/dev/null 2>&1; then shellcheck *.sh; fi
                  hadolint Dockerfile
                '''
              }
            }
          }
        }

        stage('Security Scan (Code)') {
          steps {
            script {
              if (params.USE_MOCK) {
                sh '''
                  echo "[MOCK] bandit -r ."
                  echo "[MOCK] trivy image shods/${IMAGE_NAME}:${BUILD_NUMBER}"
                '''
              } else {
                sh '''
                  python3 -m pip install -q bandit || true
                  bandit -q -r .
                  if ! command -v trivy >/dev/null 2>&1; then
                    sudo rpm -Uvh --quiet https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.55.0_Linux-64bit.rpm || true
                  fi
                  echo "Trivy will scan after build"
                '''
              }
            }
          }
        }
      }
    }

    stage('Docker Build & Login') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                          usernameVariable: 'DOCKERHUB_USERNAME',
                                          passwordVariable: 'DOCKERHUB_PASSWORD')]) {
          sh '''
            echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
            IMAGE="${DOCKERHUB_USERNAME}/${IMAGE_NAME}"
            IMAGE_FULL="${IMAGE}:${BUILD_NUMBER}"
            docker build -t "${IMAGE_FULL}" -t "${IMAGE}:latest" .
            # נשמור לקובץ כדי להשתמש בשלבים הבאים
            printf "IMAGE=%s\nIMAGE_FULL=%s\n" "$IMAGE" "$IMAGE_FULL" > image.env
          '''
        }
      }
    }

    stage('Security Scan (Image)') {
      when { expression { return !params.USE_MOCK } }
      steps {
        sh '''
          . image.env
          trivy image --exit-code 0 --severity LOW,MEDIUM "${IMAGE_FULL}"
          trivy image --exit-code 1 --severity HIGH,CRITICAL "${IMAGE_FULL}" || {
            echo "High/Critical vulnerabilities found"; exit 1;
          }
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                          usernameVariable: 'DOCKERHUB_USERNAME',
                                          passwordVariable: 'DOCKERHUB_PASSWORD')]) {
          sh '''
            . image.env
            echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
            docker push "${IMAGE_FULL}"
            docker push "${IMAGE}:latest"
          '''
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
      script {
        sh '[ -f image.env ] && cat image.env || true'
      }
    }
    success {
      sh '. image.env; echo "Done. Image: ${IMAGE_FULL} and ${IMAGE}:latest"'
    }
    failure {
      echo 'Pipeline failed. Check above logs.'
    }
  }
}
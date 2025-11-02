terraform {
  required_version = ">= 1.3.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.32"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

resource "kubernetes_namespace" "smartlink" {
  metadata {
    name = "shods-app"
  }
}

resource "kubernetes_deployment" "smartlink" {
  metadata {
    name      = "smartlink"
    namespace = kubernetes_namespace.smartlink.metadata[0].name
    labels = {
      app = "smartlink"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "smartlink"
      }
    }

    template {
      metadata {
        labels = {
          app = "smartlink"
        }
      }

      spec {
        container {
          name  = "smartlink"
          image = "shods/smartlink:v0.1"

          port {
            name           = "http"
            container_port = 5001
          }

          env {
            name  = "TZ"
            value = "Asia/Jerusalem"
          }

          liveness_probe {
            http_get {
              path = "/healthz"
              port = "http"
            }
            initial_delay_seconds = 5
            period_seconds        = 10
            timeout_seconds       = 2
            failure_threshold     = 3
          }

          readiness_probe {
            http_get {
              path = "/healthz"
              port = "http"
            }
            initial_delay_seconds = 5
            period_seconds        = 10
            timeout_seconds       = 2
            failure_threshold     = 3
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "smartlink" {
  metadata {
    name      = "smartlink-svc"
    namespace = kubernetes_namespace.smartlink.metadata[0].name
    labels = {
      app = "smartlink"
    }
  }

  spec {
    selector = {
      app = "smartlink"
    }
    type = "NodePort"

    port {
      name        = "http"
      port        = 5001
      target_port = "http"
      # node_port - נשאיר לקלאסטר להקצות אוטומטית
    }
  }
}

output "namespace" {
  value = kubernetes_namespace.smartlink.metadata[0].name
}

output "service_name" {
  value = kubernetes_service.smartlink.metadata[0].name
}
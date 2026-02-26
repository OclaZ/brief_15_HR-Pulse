terraform {
  required_providers {
    # Le provider Azure existant
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    # NOUVEAU : Le provider Docker pour l'orchestration locale
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "docker" {
  # Utilise le socket par défaut de Docker Desktop sur ta machine
}

# ==========================================
# ☁️ 1. INFRASTRUCTURE CLOUD (Azure SQL)
# ==========================================

data "azurerm_mssql_server" "formateur_server" {
  name                = "sql-server-hr-pulse-2026"
  resource_group_name = "RG-HR-PULSE-MGMT-YENNAYA"
}

resource "azurerm_mssql_database" "db_student" {
  name      = "db-hamza"
  server_id = data.azurerm_mssql_server.formateur_server.id

  sku_name     = "GP_S_Gen5_1"
  min_capacity = 0.5
  max_size_gb  = 2
  auto_pause_delay_in_minutes = 60
}

# ==========================================
# 🐳 2. ORCHESTRATION LOCALE (Conteneurs)
# ==========================================

# Création d'un réseau pour que le Front et le Back communiquent
resource "docker_network" "hr_pulse_net" {
  name = "hr_pulse_network"
}

# --- BACKEND ---
resource "docker_image" "backend_image" {
  name = "hr-pulse-backend:latest"
  build {
    # CORRECTION : On remonte d'un dossier pour trouver le vrai dossier backend
    context    = "${path.cwd}/../backend"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "backend_container" {
  name  = "hr_pulse_backend"
  image = docker_image.backend_image.image_id

  ports {
    internal = 8000
    external = 8000
  }

  networks_advanced {
    name = docker_network.hr_pulse_net.name
  }

  # L'injection dynamique du .env (On suppose que le .env est dans le dossier infra)
  volumes {
    host_path      = "${path.cwd}/.env"
    container_path = "/app/.env"
    read_only      = true
  }
}

# --- FRONTEND ---
resource "docker_image" "frontend_image" {
  name = "hr-pulse-frontend:latest"
  build {
    # CORRECTION : On remonte d'un dossier pour trouver le vrai dossier frontend
    context    = "${path.cwd}/../frontend"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "frontend_container" {
  name  = "hr_pulse_frontend"
  image = docker_image.frontend_image.image_id

  ports {
    internal = 3000
    external = 3000
  }

  env = [
    "NEXT_PUBLIC_API_URL=http://localhost:8000"
  ]

  networks_advanced {
    name = docker_network.hr_pulse_net.name
  }
  
  # Le Frontend attend que le Backend soit prêt
  depends_on = [docker_container.backend_container]
}
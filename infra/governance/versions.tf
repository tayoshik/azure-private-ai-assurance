# D16 isolated, review-only candidate; DO NOT activate without separate G07, POL-01.
terraform {
  required_version = ">= 1.9.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 4.66.0"
    }
  }
  # Independent governance state. NEVER point bootstrap at its own state.
  backend "azurerm" {}
}

provider "azurerm" {
  features {}
  subscription_id     = var.subscription_id
  storage_use_azuread = true
}

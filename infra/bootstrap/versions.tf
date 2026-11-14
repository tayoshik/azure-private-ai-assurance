terraform {
  required_version = ">= 1.9.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 4.66.0" # Provisional; exact approval required at G03.
    }
  }
  # Intentionally NO azurerm backend here. Bootstrap state is separately
  # safeguarded on the approved CI runner until private state access is proven.
}

provider "azurerm" {
  features {}
  subscription_id     = var.subscription_id
  storage_use_azuread = true
}

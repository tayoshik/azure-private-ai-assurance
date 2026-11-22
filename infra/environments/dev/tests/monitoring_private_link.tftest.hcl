# Synthetic mock: never initializes a backend or requests Azure authentication.
mock_provider "azurerm" {}

variables {
  name                                      = "synthetic-monitor"
  resource_group_name                       = "synthetic"
  location                                  = "eastus"
  tags                                      = {}
  monitoring_and_private_ingestion_approved = true
  subscription_id                           = "00000000-0000-0000-0000-000000000000"
  workload_vnet_id                          = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/virtualNetworks/workload"
}

run "disabled_preserves_workspace_and_creates_no_private_link" {
  command = plan

  module {
    source = "../../modules/monitoring"
  }

  assert {
    condition = (
      length(azurerm_monitor_private_link_scope.monitor) == 0 &&
      length(azurerm_monitor_private_link_scoped_service.workspace) == 0 &&
      length(azurerm_private_endpoint.monitor) == 0 &&
      length(azurerm_private_dns_zone.monitor) == 0
    )
    error_message = "Disabled mode must retain the workspace without creating Monitor Private Link resources."
  }

  assert {
    condition     = !azurerm_log_analytics_workspace.audit.internet_ingestion_enabled && !azurerm_log_analytics_workspace.audit.internet_query_enabled
    error_message = "The workspace must block public ingestion and query in every topology."
  }
}

run "dev_owns_scope_pe_and_five_links" {
  command = plan
  module {
    source = "../../modules/monitoring"
  }
  variables {
    private_link = {
      mode              = "dev"
      topology_approved = true
      dev_isolated_dns  = true
      dev_subnet_cidr   = "10.0.7.0/27"
      dev_client_cidrs  = ["10.0.6.0/24"]
    }
  }
  assert {
    condition = (
      azurerm_monitor_private_link_scope.monitor[0].query_access_mode == "PrivateOnly" &&
      azurerm_monitor_private_link_scope.monitor[0].ingestion_access_mode == "PrivateOnly" &&
      length(azurerm_monitor_private_link_scoped_service.workspace) == 1 &&
      azurerm_private_endpoint.monitor[0].private_service_connection[0].is_manual_connection &&
      contains(azurerm_private_endpoint.monitor[0].private_service_connection[0].subresource_names, "azuremonitor") &&
      length(azurerm_subnet.monitor) == 1 &&
      length(azurerm_subnet_network_security_group_association.monitor) == 1 &&
      length(azurerm_private_dns_zone.monitor) == 5 &&
      length(azurerm_private_dns_zone_virtual_network_link.monitor) == 5
    )
    error_message = "Dev owns the AMPLS, workspace association, approval-pending PE and five DNS zones and links."
  }
}

run "hub_owns_dns_pe_and_scope" {
  command = plan
  module {
    source = "../../modules/monitoring"
  }
  variables {
    private_link = {
      mode              = "hub"
      topology_approved = true
      hub_scope_id      = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Insights/privateLinkScopes/central-monitor"
      hub_endpoint_id   = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/privateEndpoints/existing-monitor"
      hub_zone_ids = {
        "privatelink.monitor.azure.com"             = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/privateDnsZones/privatelink.monitor.azure.com"
        "privatelink.oms.opinsights.azure.com"      = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/privateDnsZones/privatelink.oms.opinsights.azure.com"
        "privatelink.ods.opinsights.azure.com"      = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/privateDnsZones/privatelink.ods.opinsights.azure.com"
        "privatelink.agentsvc.azure-automation.net" = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/privateDnsZones/privatelink.agentsvc.azure-automation.net"
        "privatelink.blob.core.windows.net"         = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/synthetic/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net"
      }
    }
  }
  assert {
    condition = (
      length(azurerm_monitor_private_link_scope.monitor) == 0 &&
      length(azurerm_private_endpoint.monitor) == 0 &&
      length(azurerm_subnet.monitor) == 0 &&
      length(azurerm_private_dns_zone.monitor) == 0 &&
      length(azurerm_private_dns_zone_virtual_network_link.monitor) == 0 &&
      azurerm_monitor_private_link_scoped_service.workspace[0].scope_name == "central-monitor"
    )
    error_message = "Hub mode may create the workspace association only."
  }
}

run "reject_dev_without_isolated_dns" {
  command = plan
  module {
    source = "../../modules/monitoring"
  }
  variables {
    private_link = {
      mode              = "dev"
      topology_approved = true
      dev_subnet_cidr   = "10.0.7.0/27"
      dev_client_cidrs  = ["10.0.6.0/24"]
    }
  }
  expect_failures = [var.private_link]
}

run "reject_incomplete_hub" {
  command = plan
  module {
    source = "../../modules/monitoring"
  }
  variables {
    private_link = {
      mode              = "hub"
      topology_approved = true
    }
  }
  expect_failures = [var.private_link]
}

run "reject_undersized_endpoint_subnet" {
  command = plan
  module {
    source = "../../modules/monitoring"
  }
  variables {
    private_link = {
      mode              = "dev"
      topology_approved = true
      dev_isolated_dns  = true
      dev_subnet_cidr   = "10.0.7.0/28"
      dev_client_cidrs  = ["10.0.6.0/24"]
    }
  }
  expect_failures = [var.private_link]
}

# N04 — Azure NSGs are per-subnet, not an application authorization boundary.
# This is an explicit *restricted* design profile, not a safe deployment by itself.
# A reviewed egress dependency manifest (identity, DNS, CRL, monitoring, etc.),
# a private AppGW Network Isolation feature check and signed IPAM are required.
# Azure-native platform communication and effective routes must be reviewed.

resource "azurerm_network_security_group" "app_gateway" {
  name                = "nsg-${var.name}-appgw"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_network_security_rule" "gateway_client_https" {
  name                        = "AllowApprovedClients443"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefixes     = var.approved_client_cidrs
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

# Private-only WAF_v2 + Network Isolation: health from AzureLoadBalancer,
# not the legacy GatewayManager service tag. Verify the selected gateway mode.
resource "azurerm_network_security_rule" "gateway_platform_probe" {
  name                        = "AllowAzureLoadBalancerInbound"
  priority                    = 110
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "AzureLoadBalancer"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

resource "azurerm_network_security_rule" "gateway_deny_other_inbound" {
  name                        = "DenyUnapprovedInbound"
  priority                    = 4090
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

# Application Gateway talks to Web PE, and, if configured, Key Vault PE placed
# in the data-PE subnet. Treat these as subnets not as service identity proof.
resource "azurerm_network_security_rule" "gateway_to_web_pe" {
  name                        = "AllowWebPrivateEndpoint443"
  priority                    = 100
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = var.subnet_cidrs.web_private_endpoint
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

resource "azurerm_network_security_rule" "gateway_to_data_pe" {
  name                        = "AllowApprovedVaultPrivateEndpoint443"
  priority                    = 110
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = var.subnet_cidrs.data_private_endpoint
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

resource "azurerm_network_security_rule" "gateway_dns_udp" {
  count                        = length(var.approved_dns_resolver_ips) > 0 ? 1 : 0
  name                         = "AllowApprovedDnsUdp"
  priority                     = 120
  direction                    = "Outbound"
  access                       = "Allow"
  protocol                     = "Udp"
  source_port_range            = "*"
  destination_port_range       = "53"
  source_address_prefix        = "*"
  destination_address_prefixes = var.approved_dns_resolver_ips
  resource_group_name          = var.resource_group_name
  network_security_group_name  = azurerm_network_security_group.app_gateway.name
}

resource "azurerm_network_security_rule" "gateway_dns_tcp" {
  count                        = length(var.approved_dns_resolver_ips) > 0 ? 1 : 0
  name                         = "AllowApprovedDnsTcp"
  priority                     = 130
  direction                    = "Outbound"
  access                       = "Allow"
  protocol                     = "Tcp"
  source_port_range            = "*"
  destination_port_range       = "53"
  source_address_prefix        = "*"
  destination_address_prefixes = var.approved_dns_resolver_ips
  resource_group_name          = var.resource_group_name
  network_security_group_name  = azurerm_network_security_group.app_gateway.name
}

resource "azurerm_network_security_rule" "gateway_approved_egress" {
  for_each                    = var.gateway_extra_egress_rules
  name                        = "Allow-${each.key}"
  priority                    = each.value.priority
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = tostring(each.value.destination_port)
  source_address_prefix       = "*"
  destination_address_prefix  = each.value.destination_cidr
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

resource "azurerm_network_security_rule" "gateway_deny_other_outbound" {
  name                        = "DenyUnapprovedOutbound"
  priority                    = 4090
  direction                   = "Outbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_gateway.name
}

# Gate the potentially disruptive NSG association behind environment review.
# A false gate leaves 'terraform plan' as a deliberate failure, not green.
resource "azurerm_subnet_network_security_group_association" "app_gateway" {
  subnet_id                 = azurerm_subnet.app_gateway.id
  network_security_group_id = azurerm_network_security_group.app_gateway.id

  lifecycle {
    precondition {
      condition     = var.network_policy_approved && var.gateway_network_isolation_approved && var.gateway_egress_profile_approved
      error_message = "G03/G07: approve the private gateway feature, IPAM, complete egress dependencies and network control policy before planning this association."
    }
  }
}

# App Service VNet Integration subnet: outbound policy only. The inbound
# App Service request path is the separate Web PE subnet (below).
resource "azurerm_network_security_group" "app_outbound" {
  name                = "nsg-${var.name}-app-outbound"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_network_security_rule" "app_to_data_pe" {
  name                        = "AllowApprovedDataPrivateEndpoint443"
  priority                    = 100
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = var.subnet_cidrs.data_private_endpoint
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_outbound.name
}

resource "azurerm_network_security_rule" "app_dns_udp" {
  count                        = length(var.approved_dns_resolver_ips) > 0 ? 1 : 0
  name                         = "AllowApprovedDnsUdp"
  priority                     = 120
  direction                    = "Outbound"
  access                       = "Allow"
  protocol                     = "Udp"
  source_port_range            = "*"
  destination_port_range       = "53"
  source_address_prefix        = "*"
  destination_address_prefixes = var.approved_dns_resolver_ips
  resource_group_name          = var.resource_group_name
  network_security_group_name  = azurerm_network_security_group.app_outbound.name
}

resource "azurerm_network_security_rule" "app_dns_tcp" {
  count                        = length(var.approved_dns_resolver_ips) > 0 ? 1 : 0
  name                         = "AllowApprovedDnsTcp"
  priority                     = 130
  direction                    = "Outbound"
  access                       = "Allow"
  protocol                     = "Tcp"
  source_port_range            = "*"
  destination_port_range       = "53"
  source_address_prefix        = "*"
  destination_address_prefixes = var.approved_dns_resolver_ips
  resource_group_name          = var.resource_group_name
  network_security_group_name  = azurerm_network_security_group.app_outbound.name
}

resource "azurerm_network_security_rule" "app_approved_egress" {
  for_each                    = var.app_extra_egress_rules
  name                        = "Allow-${each.key}"
  priority                    = each.value.priority
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = tostring(each.value.destination_port)
  source_address_prefix       = "*"
  destination_address_prefix  = each.value.destination_cidr
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_outbound.name
}

resource "azurerm_network_security_rule" "app_deny_other_outbound" {
  name                        = "DenyUnapprovedOutbound"
  priority                    = 4090
  direction                   = "Outbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.app_outbound.name
}

resource "azurerm_subnet_network_security_group_association" "app_outbound" {
  subnet_id                 = azurerm_subnet.app_outbound.id
  network_security_group_id = azurerm_network_security_group.app_outbound.id

  lifecycle {
    precondition {
      condition     = var.network_policy_approved && var.app_egress_profile_approved
      error_message = "G07/W03: approve the complete App Service identity/monitoring/CRL/runtime egress list and VNet route-all behavior before plan."
    }
  }
}

# The inbound Web PE has a different NSG from the App outbound integration.
resource "azurerm_network_security_group" "web_pe" {
  name                = "nsg-${var.name}-web-pe"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_network_security_rule" "web_pe_from_gateway" {
  name                        = "AllowGateway443"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = var.subnet_cidrs.app_gateway
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.web_pe.name
}

resource "azurerm_network_security_rule" "web_pe_from_tests" {
  count                       = length(var.approved_test_runner_cidrs) > 0 ? 1 : 0
  name                        = "AllowApprovedPrivateTests443"
  priority                    = 120
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefixes     = var.approved_test_runner_cidrs
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.web_pe.name
}

resource "azurerm_network_security_rule" "web_pe_deny_other_inbound" {
  name                        = "DenyUnapprovedInbound"
  priority                    = 4090
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.web_pe.name
}

resource "azurerm_subnet_network_security_group_association" "web_pe" {
  subnet_id                 = azurerm_subnet.web_private_endpoint.id
  network_security_group_id = azurerm_network_security_group.web_pe.id

  lifecycle {
    precondition {
      condition     = var.network_policy_approved
      error_message = "G07: PE network policies, CIDR assignments and target subresource must be approved."
    }
  }
}

# AI/data/Key Vault Private Endpoints; allow approved App outbound and gateway.
resource "azurerm_network_security_group" "data_pe" {
  name                = "nsg-${var.name}-data-pe"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_network_security_rule" "data_pe_from_app" {
  name                        = "AllowAppIntegration443"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = var.subnet_cidrs.app_outbound
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.data_pe.name
}

resource "azurerm_network_security_rule" "data_pe_from_gateway" {
  name                        = "AllowGatewayToKeyVault443"
  priority                    = 110
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = var.subnet_cidrs.app_gateway
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.data_pe.name
}

resource "azurerm_network_security_rule" "data_pe_deny_other_inbound" {
  name                        = "DenyUnapprovedInbound"
  priority                    = 4090
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.data_pe.name
}

resource "azurerm_subnet_network_security_group_association" "data_pe" {
  subnet_id                 = azurerm_subnet.data_private_endpoint.id
  network_security_group_id = azurerm_network_security_group.data_pe.id

  lifecycle {
    precondition {
      condition     = var.network_policy_approved
      error_message = "G07: data PE NSG and private endpoint network policies must be approved."
    }
  }
}

# An optional default route to a pre-approved firewall. NEVER route the
# gateway subnet this way without a separate Azure feature/architecture review.
resource "azurerm_route_table" "app_outbound" {
  count                         = var.enable_app_forced_tunnel ? 1 : 0
  name                          = "rt-${var.name}-app-outbound"
  location                      = var.location
  resource_group_name           = var.resource_group_name
  bgp_route_propagation_enabled = false
  tags                          = var.tags

  route {
    name                   = "DefaultToApprovedFirewall"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = var.approved_firewall_next_hop_ip
  }

  lifecycle {
    precondition {
      condition     = var.network_policy_approved && var.app_egress_profile_approved && var.approved_firewall_next_hop_ip != null
      error_message = "An approved firewall private IP and signed dependencies are mandatory for the App Service default route."
    }
  }
}

resource "azurerm_subnet_route_table_association" "app_outbound" {
  count          = var.enable_app_forced_tunnel ? 1 : 0
  subnet_id      = azurerm_subnet.app_outbound.id
  route_table_id = azurerm_route_table.app_outbound[0].id
}

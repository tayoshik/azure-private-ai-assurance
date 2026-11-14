output "workload_resource_group_id" {
  value = module.foundation.id
}
output "vnet_id" {
  value = module.network.vnet_id
}
output "app_gateway_subnet_id" {
  value = module.network.app_gateway_subnet_id
}
output "app_outbound_subnet_id" {
  value = module.network.app_outbound_subnet_id
}
output "web_private_endpoint_subnet_id" {
  value = module.network.web_private_endpoint_subnet_id
}
output "data_private_endpoint_subnet_id" {
  value = module.network.data_private_endpoint_subnet_id
}
output "private_dns_zone_ids" {
  value = module.private_dns.zone_ids
}

output "network_security_group_ids" {
  value = module.network.network_security_group_ids
}
output "app_outbound_route_table_id" {
  value = module.network.app_outbound_route_table_id
}


output "app_managed_identity_id" { value = module.identity.app_identity_id }
output "app_managed_identity_client_id" { value = module.identity.app_client_id }
output "gateway_managed_identity_id" { value = module.identity.gateway_identity_id }
output "key_vault_id" { value = module.key_vault.id }
output "key_vault_uri" { value = module.key_vault.vault_uri }
output "key_vault_private_endpoint_id" { value = module.key_vault_private_endpoint.key_vault_private_endpoint_id }

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


output "openai_account_id" { value = module.azure_openai.account_id }
output "openai_endpoint" { value = module.azure_openai.endpoint }
output "openai_deployment_name" { value = module.azure_openai.deployment_name }
output "search_service_id" { value = module.ai_search.id }
output "search_hostname" { value = module.ai_search.hostname }
output "cosmos_account_id" { value = module.cosmos_db.account_id }
output "cosmos_endpoint" { value = module.cosmos_db.account_endpoint }
output "ai_data_private_endpoint_ips" {
  value = {
    openai = module.ai_data_private_endpoints.openai_private_ip
    search = module.ai_data_private_endpoints.search_private_ip
    cosmos = module.ai_data_private_endpoints.cosmos_private_ip
  }
}
output "data_role_assignment_ids" {
  value = {
    openai = module.ai_data_rbac.openai_user_assignment_id
    search = module.ai_data_rbac.search_reader_assignment_id
    cosmos = module.ai_data_rbac.cosmos_sql_assignment_id
  }
}

output "app_service_plan_id" { value = module.app_service.service_plan_id }
output "app_web_app_id" { value = module.app_service.web_app_id }
output "app_web_default_hostname" { value = module.app_service.default_hostname }
output "app_web_private_endpoint_id" { value = module.webapp_private_endpoint.private_endpoint_id }
output "app_web_private_endpoint_ip" { value = module.webapp_private_endpoint.private_ip }

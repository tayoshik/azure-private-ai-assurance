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

# W05: nonsecret app contract ONLY. Verify actual application source before use.
# No shared keys, tokens, connection strings, passwords or secret contents.
locals {
  app_settings = {
    AZURE_OPENAI_ENDPOINT       = var.openai_endpoint
    AZURE_OPENAI_DEPLOYMENT     = var.openai_deployment_name
    AZURE_SEARCH_ENDPOINT      = "https://${var.search_hostname}"
    COSMOS_DB_ENDPOINT         = var.cosmos_endpoint
    COSMOS_DATABASE_NAME       = var.cosmos_database_name
    COSMOS_CONTAINER_NAME      = var.cosmos_container_name
    AZURE_CLIENT_ID            = var.app_identity_client_id
    WEBSITE_HEALTHCHECK_MAXPINGFAILURES = "3"
  }
}

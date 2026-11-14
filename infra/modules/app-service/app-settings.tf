# W05 - All values are non-secret endpoint identifiers and public configuration.
# Tokens, database connection strings, API keys and secret material MUST NOT be
# embedded in app_settings: doing so would expose them to Terraform state.
# These environment variable names are a candidate application contract;
# the real application source is not yet available and must be reviewed.
locals {
  app_settings = {
    AZURE_OPENAI_ENDPOINT               = var.openai_endpoint
    AZURE_OPENAI_DEPLOYMENT             = var.openai_deployment_name
    AZURE_SEARCH_ENDPOINT               = "https://${var.search_hostname}"
    COSMOS_DB_ENDPOINT                  = var.cosmos_endpoint
    COSMOS_DATABASE_NAME                = var.cosmos_database_name
    COSMOS_CONTAINER_NAME               = var.cosmos_container_name
    AZURE_CLIENT_ID                     = var.app_identity_client_id
    WEBSITE_HEALTHCHECK_MAXPINGFAILURES = "3"
  }
}

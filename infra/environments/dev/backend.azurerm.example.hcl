# EXAMPLE: no secrets. Use only AFTER bootstrap connectivity gate B05.
# Values must be injected from approved protected CI variables.
resource_group_name  = "rg-REPLACE-bootstrap"
storage_account_name = "stREPLACE"
container_name       = "tfstate"
key                  = "dev.tfstate"
use_azuread_auth     = true
use_oidc             = true

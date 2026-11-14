# GW01: fail-safe policy starts in Detection mode. Prevention requires a
# separately attested false-positive/negative test and rule-change approval.
resource "azurerm_web_application_firewall_policy" "private_web" {
  name                = "waf-${var.name}"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags

  policy_settings {
    enabled            = true
    mode               = var.waf_mode
    request_body_check = true
  }

  managed_rules {
    managed_rule_set {
      type    = "Microsoft_DefaultRuleSet"
      version = var.waf_drs_version
    }
  }

  lifecycle {
    precondition {
      condition     = var.waf_policy_approved
      error_message = "GW01/G07: WAF policy and exception review approval is required."
    }
    precondition {
      condition     = var.waf_mode == "Detection" || var.waf_prevention_approved
      error_message = "Prevention requires a separate signed WAF-mode approval and evidence."
    }
  }
}

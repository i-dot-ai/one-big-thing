resource "aws_wafv2_web_acl" "obt-waf" {
  name        = "WAF-for-OBT-Cloudfront-${var.env}"
  description = "Cloudfront rate based statement for ${var.env}"
  scope       = "CLOUDFRONT"
  provider    = aws.useast1


  default_action {
    allow {}
  }

#  rule {
#    name        = "example-rule"
#    priority    = 1
#    action {
#      allow {}
#    }
#    statement {
#      rate_based_statement {
#        limit              = 10000
#        aggregate_key_type = "IP"
#
#        scope_down_statement {
#          geo_match_statement {
#            country_codes = ["US", "NL"]
#          }
#        }
#      }
#    }
#
#    visibility_config {
#      cloudwatch_metrics_enabled = true
#      metric_name                = "obt-${var.env}-web-acl-metric-rule-1"
#      sampled_requests_enabled   = true
#    }
#  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "obt-${var.env}-web-acl-metric"
    sampled_requests_enabled   = true
  }
}
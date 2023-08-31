#resource "aws_cloudfront_distribution" "cloudfront_distribution" {
#  comment = "Cloudfront distribution for OBT ${var.env}"
#  origin {
#    domain_name = aws_alb.this.dns_name
#    origin_id   = "obt_alb_origin_id"
#
#    custom_origin_config {
#      http_port              = 80
#      https_port             = 443
#      origin_protocol_policy = "match-viewer"
#      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
#    }
#  }
#
#  enabled             = true
#  is_ipv6_enabled     = true
#
#  default_cache_behavior {
#    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
#    origin_request_policy_id = "216adef6-5c7f-47e4-b989-5492eafa07d3"
#    allowed_methods  = ["GET", "HEAD", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"]
#    cached_methods   = ["GET", "HEAD"]
#    target_origin_id = "obt_alb_origin_id"
#
##    forwarded_values {
##      query_string = true
##      headers      = ["*"]
##
##      cookies {
##        forward = "all"
##      }
##    }
#
#    viewer_protocol_policy = "redirect-to-https"
#    min_ttl                = 0
#    default_ttl            = 3600
#    max_ttl                = 86400
#  }
#
##  ordered_cache_behavior {
##    path_pattern     = "/static/*"
##    allowed_methods  = ["GET", "HEAD", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"]
##    cached_methods   = ["GET", "HEAD"]
##    target_origin_id = "obt_alb_origin_id"
##
##    forwarded_values {
##      query_string = true
##      headers      = ["*"]
##
##      cookies {
##        forward = "all"
##      }
##    }
##
##    viewer_protocol_policy = "redirect-to-https"
##    min_ttl                = 0
##    default_ttl            = 3600
##    max_ttl                = 86400
##  }
#
#  price_class = "PriceClass_All"
#
#  restrictions {
#    geo_restriction {
#      restriction_type = "none"
#    }
#  }
#
#  viewer_certificate {
##    acm_certificate_arn = data.terraform_remote_state.universal.outputs.one_big_thing_cert_arn
##    ssl_support_method  = "sni-only"
#    cloudfront_default_certificate = true
#  }
#
##  web_acl_id = aws_wafv2_web_acl.obt-waf.id
#}
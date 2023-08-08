
resource "aws_route53_record" "this" {
  zone_id = data.terraform_remote_state.universal.outputs.ten_ds_domain_hosted_zone_id
  name    = "${var.record_prefix}.${data.terraform_remote_state.universal.outputs.ten_ds_domain_url}"
  type    = "A"

  alias {
    name                   = aws_alb.this.dns_name
    zone_id                = aws_alb.this.zone_id
    evaluate_target_health = true
  }
}

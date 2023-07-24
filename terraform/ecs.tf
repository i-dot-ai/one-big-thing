module "ecs" {
  source       = "terraform-aws-modules/ecs/aws"
  version      = "5.2.0"
  cluster_name = "${local.team}-${local.project}-${var.env}"

  services = {
    one-big-thing = {
      cpu    = 1024
      memory = 4096

      # Container definition(s)
      container_definitions = {

        one-big-thing = {
          cpu                       = 1024
          memory                    = 4096
          essential                 = true
          image                     = "${data.terraform_remote_state.universal.outputs.one_big_thing_ecr_repo_url}:${var.image_tag}"
          readonly_root_filesystem  = true
          enable_cloudwatch_logging = true
          environment = [
            {
              name  = "ENVIRONMENT"
              value = var.env
            },
            {
              name  = "DB_HOST"
              value = module.db.db_instance_address
            },
            {
              name  = "DB_PORT"
              value = local.db_port
            },
            {
              name  = "DB_USER"
              value = local.db_user
            },
            {
              name  = "DB_NAME"
              value = local.db_name
            },
            {
              name  = "DB_PASSWORD_SECRET_NAME"
              value = module.db.db_instance_master_user_secret_arn
            },
            {
              name  = "DJANGO_SECRET_KEY"
              value = "1n53cur3K3y"
            },
            {
              name  = "CONTACT_EMAIL"
              value = "test@example.com"
            },
            {
              name  = "FROM_EMAIL"
              value = "test@example.com"
            },
            {
              name  = "EMAIL_BACKEND_TYPE"
              value = "CONSOLE"
            },
            {
              # TODO: Change this when we have route 53
              name  = "BASE_URL"
              value = aws_alb.this.dns_name
            },
            {
              name  = "VCAP_APPLICATION"
              value = "{'space_name': 'local'}"
            },
            {
              name  = "REQUIRED_LEARNING_TIME"
              value = 420
            },
            {
              name  = "SEND_VERIFICATION_EMAIL"
              value = true
            },
          ]
        }

      }

      subnet_ids = data.terraform_remote_state.vpc.outputs.private_subnets
      security_group_rules = {
        alb_ingress = {
          type                     = "ingress"
          from_port                = 8055
          to_port                  = 8055
          protocol                 = "tcp"
          description              = "Service port"
          source_security_group_id = aws_security_group.load_balancer_security_group.id
        }
        egress_all = {
          type        = "egress"
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      }
    }
  }
}

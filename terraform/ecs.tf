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
          cpu       = 1024
          memory    = 4096
          essential = true
          port_mappings = [
            {
              name          = "application"
              containerPort = 8055
              protocol      = "tcp"
            }
          ]
          image                     = "${data.terraform_remote_state.universal.outputs.one_big_thing_ecr_repo_url}:${var.image_tag}"
          readonly_root_filesystem  = true
          enable_cloudwatch_logging = true
          secrets = [
            {
              name = "DJANGO_SECRET_KEY",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:DJANGO_SECRET_KEY:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "CONTACT_EMAIL",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:CONTACT_EMAIL:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "FEEDBACK_EMAIL",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:FEEDBACK_EMAIL:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "FROM_EMAIL",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:FROM_EMAIL:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "GOVUK_NOTIFY_API_KEY",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:GOVUK_NOTIFY_API_KEY:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "ALLOWED_DOMAINS",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:ALLOWED_DOMAINS:AWSCURRENT:AWSCURRENT"
            },

            {
              name = "SENTRY_DSN",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:SENTRY_DSN:AWSCURRENT:AWSCURRENT"
            },
            {
              name = "SENTRY_ENVIRONMENT",
              valueFrom = "arn:aws:secretsmanager:eu-west-2:817650998681:secret:one-big-thing-${var.env}:SENTRY_ENVIRONMENT:AWSCURRENT:AWSCURRENT"
            },
          ]
          environment = [
            {
              name  = "ENVIRONMENT"
              value = var.env
            },
            {
              name  = "POSTGRES_HOST"
              value = module.db.db_instance_address
            },
            {
              name  = "POSTGRES_PORT"
              value = local.db_port
            },
            {
              name  = "POSTGRES_USER"
              value = local.db_user
            },
            {
              name  = "POSTGRES_DB"
              value = local.db_name
            },
            {
              name  = "DB_PASSWORD_SECRET_NAME"
              value = module.db.db_instance_master_user_secret_arn
            },
            {
              name  = "EMAIL_BACKEND_TYPE"
              value = var.email_backend_type
            },
            {
              name  = "BASE_URL"
              value = aws_route53_record.this.fqdn
            },
            {
              name  = "VCAP_APPLICATION"
              value = jsonencode({ "space_name" : var.env })
            },
            {
              name  = "REQUIRED_LEARNING_TIME"
              value = var.required_learning_time
            },
            {
              name  = "SEND_VERIFICATION_EMAIL"
              value = var.send_verification_email
            },
            {
              name  = "PORT"
              value = var.port
            },
            {
              name = "SELF_REFLECTION_FILENAME"
              value = var.self_reflection_filename
            },
            {
              name = "BASE_URL"
              value = local.base_url
            },
          ]
        }

      }

      subnet_ids = data.terraform_remote_state.vpc.outputs.private_subnets
      load_balancer = {
        service = {
          target_group_arn = aws_lb_target_group.this.arn
          container_name   = "one-big-thing"
          container_port   = 8055
        }
      }
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

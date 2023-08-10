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
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:DJANGO_SECRET_KEY::",
            },
            {
              name = "CONTACT_EMAIL",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:CONTACT_EMAIL::",
            },
            {
              name = "FEEDBACK_EMAIL",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:FEEDBACK_EMAIL::",
            },
            {
              name = "FROM_EMAIL",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:FROM_EMAIL::",
            },
            {
              name = "GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID::",
            },
            {
              name = "GOVUK_NOTIFY_API_KEY",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:GOVUK_NOTIFY_API_KEY::",
            },
            {
              name = "ALLOWED_DOMAINS",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:ALLOWED_DOMAINS::",
            },

            {
              name = "SENTRY_DSN",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:SENTRY_DSN::",
            },
            {
              name = "SENTRY_ENVIRONMENT",
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-${var.env}-p08zry:SENTRY_ENVIRONMENT::",
            },
            {
              name  = "POSTGRES_PASSWORD"
              valueFrom = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-database-2mSGR4:password::"
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
              name  = "DEBUG"
              value = var.debug
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

module "ecs" {
  source                                = "terraform-aws-modules/ecs/aws"
  version                               = "5.2.0"
  cluster_name                          = "${local.team}-${local.project}-${var.env}"
  default_capacity_provider_use_fargate = true

  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 100
      }
    }
  }

  services = {
    one-big-thing = {
      cpu                       = 1024
      memory                    = 4096
      enable_autoscaling        = true
      desired_count             = 2
      autoscaling_min_capacity  = 2
      autoscaling_max_capacity  = 20
      autoscaling_policies =  {
        cpu = {
          policy_type = "TargetTrackingScaling"

          target_tracking_scaling_policy_configuration = {
            disable_scale_in    = false,
            scale_in_cooldown   = 300,
            scale_out_cooldown  = 60,
            target_value        = 90
            predefined_metric_specification = {
              predefined_metric_type = "ECSServiceAverageCPUUtilization"
            }
          }
        }
        memory = {
          policy_type = "TargetTrackingScaling"

          target_tracking_scaling_policy_configuration = {
            disable_scale_in    = false,
            scale_in_cooldown   = 300,
            scale_out_cooldown  = 60,
            target_value        = 90
            predefined_metric_specification = {
              predefined_metric_type = "ECSServiceAverageMemoryUtilization"
            }
          }
        }
      }

      # Container definition(s)
      container_definitions = {
        "one-big-thing-${var.env}" = {
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
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:DJANGO_SECRET_KEY::",
            },
            {
              name = "CONTACT_EMAIL",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:CONTACT_EMAIL::",
            },
            {
              name = "FEEDBACK_EMAIL",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:FEEDBACK_EMAIL::",
            },
            {
              name = "FROM_EMAIL",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:FROM_EMAIL::",
            },
            {
              name = "GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID::",
            },
            {
              name = "GOVUK_NOTIFY_API_KEY",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:GOVUK_NOTIFY_API_KEY::",
            },
            {
              name = "ALLOWED_DOMAINS",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:ALLOWED_DOMAINS::",
            },

            {
              name = "SENTRY_DSN",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:SENTRY_DSN::",
            },
            {
              name = "SENTRY_ENVIRONMENT",
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:SENTRY_ENVIRONMENT::",
            },
            {
              name  = "POSTGRES_PASSWORD"
              valueFrom = "${data.aws_secretsmanager_secret_version.env_secret.arn}:DATABASE_PASSWORD::"
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
          container_name   = "one-big-thing-${var.env}"
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

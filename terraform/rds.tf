resource "aws_security_group" "rds" {
  vpc_id      = data.terraform_remote_state.vpc.outputs.vpc_id
  description = "RDS security group access"
}

resource "aws_security_group_rule" "rds" {
  type              = "ingress"
  description       = "Securelist for the RDS instance"
  from_port         = local.db_port
  to_port           = local.db_port
  protocol          = "TCP"
  cidr_blocks       = var.ip_securelist
  security_group_id = aws_security_group.rds.id
}

resource "aws_security_group_rule" "ecs" {
  type                     = "ingress"
  description              = "Allow access to the ECS task"
  from_port                = local.db_port
  to_port                  = local.db_port
  protocol                 = "TCP"
  source_security_group_id = module.ecs.services["one-big-thing-${var.env}"].security_group_id
  security_group_id        = aws_security_group.rds.id
}

module "db" {
  source     = "terraform-aws-modules/rds-aurora/aws"
  version    = "8.3.1"
  name       = "i-dot-ai-one-big-thing-${var.env}"

  engine                      = "aurora-postgresql"
  engine_version              = "15.3"
  instance_class              = var.rds_instance_class
  instances                   = var.rds_instances
  database_name               = local.db_name
  master_username             = local.db_user
  port                        = local.db_port
  master_password             = local.db_password
  manage_master_user_password = false
  apply_immediately           = true

  autoscaling_enabled             = true
  autoscaling_min_capacity        = var.rds_autoscaling_min_capacity
  autoscaling_max_capacity        = var.rds_autoscaling_max_capacity
  autoscaling_scale_out_cooldown  = 5
  autoscaling_scale_in_cooldown   = 30

  create_security_group  = false
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = true

  preferred_maintenance_window = "Mon:00:00-Mon:03:00"
  preferred_backup_window      = "03:00-06:00"
  backup_retention_period      = 35

  # DB subnet group
  create_db_subnet_group = true
  db_subnet_group_name   = "${local.project}-${var.env}-rds-subnet"
  subnets                = data.terraform_remote_state.vpc.outputs.public_subnets

  # Database Deletion Protection
  deletion_protection = true
}

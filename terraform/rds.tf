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
  source_security_group_id = module.ecs.services["one-big-thing"].security_group_id
  security_group_id        = aws_security_group.rds.id
}

#resource "random_password" "obt_db_password" {
#  length           = 50
#  special          = true
#  override_special = "_!%^&*#"
#
##  lifecycle {
##    ignore_changes = []
##  }
#}
#
#resource "aws_secretsmanager_secret" "obt_db_password" {
#  name        = "obt_db_password"
#  description = "Terraform created password for the obt database"
#  recovery_window_in_days = 0
#}
#
#resource "aws_secretsmanager_secret_version" "obt_db_password" {
#  secret_id     = aws_secretsmanager_secret.obt_db_password.id
#  secret_string = random_password.obt_db_password.result
#}



module "db" {
  source     = "terraform-aws-modules/rds/aws"
  version    = "6.1.0"
  identifier = "i-dot-ai-one-big-thing-${var.env}"

  engine            = "postgres"
  engine_version    = "14"
  instance_class    = "db.t3.micro"
  family            = "postgres14"
  db_name           = local.db_name
  username          = local.db_user
  port              = local.db_port
  password          = local.db_password
  manage_master_user_password = false
  allocated_storage = 20

  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = true

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  # DB subnet group
  create_db_subnet_group = true
  subnet_ids             = data.terraform_remote_state.vpc.outputs.public_subnets

  # Database Deletion Protection
  deletion_protection = true
}

resource "aws_security_group" "rds" {
  vpc_id      = data.terraform_remote_state.vpc.outputs.vpc_id
  description = "RDS security group access"
}

resource "aws_security_group_rule" "rds" {
  type              = "ingress"
  description       = "Securelist for the RDS instance"
  from_port         = 5432
  to_port           = 5432
  protocol          = "TCP"
  cidr_blocks       = var.ip_securelist
  security_group_id = aws_security_group.rds.id
}


module "db" {
  source     = "terraform-aws-modules/rds/aws"
  version    = "6.1.0"
  identifier = "i-dot-ai-one-big-thing-${var.env}"

  engine            = "postgres"
  engine_version    = "14"
  instance_class    = "db.t3.micro"
  family            = "postgres14"
  db_name           = "obt"
  username          = "postgres"
  port              = "5432"
  allocated_storage = 20

  vpc_security_group_ids = [aws_security_group.rds.id]

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  # DB subnet group
  create_db_subnet_group = true
  subnet_ids             = data.terraform_remote_state.vpc.outputs.public_subnets

  # Database Deletion Protection
  deletion_protection = true

}


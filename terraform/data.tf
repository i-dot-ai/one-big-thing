data "terraform_remote_state" "vpc" {
  backend   = "s3"
  workspace = terraform.workspace
  config = {
    bucket = "i-dot-ai-prod-tfstate"
    key    = "vpc/terraform.tfstate"
    region = "eu-west-2"
  }
}

data "terraform_remote_state" "universal" {
  backend = "s3"

  config = {
    bucket = "i-dot-ai-prod-tfstate"
    key    = "universal/terraform.tfstate"
    region = "eu-west-2"
  }
}

locals {
  team    = "i-dot-ai"
  project = "one-big-thing"

  db_port = 5432
  db_user = "postgres"
  db_name = "obt"
}

data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

data "aws_secretsmanager_secret" "db_password_secret" {
  arn = "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:one-big-thing-database-2mSGR4"
}

data "aws_secretsmanager_secret_version" "db_password_secret" {
  secret_id = data.aws_secretsmanager_secret.db_password_secret.id
}

locals {
  db_secret_value = jsondecode(data.aws_secretsmanager_secret_version.db_password_secret.secret_string)
  db_password     = local.db_secret_value["password"]
}

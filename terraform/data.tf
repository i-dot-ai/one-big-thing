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

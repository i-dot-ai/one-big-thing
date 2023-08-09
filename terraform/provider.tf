terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-west-2"

  default_tags {
    tags = {
      Environment = var.env
      Project     = "i-dot-ai"
      Name        = "one-big-thing"
    }
  }
}

terraform {
  backend "s3" {}
}

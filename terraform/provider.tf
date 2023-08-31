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
  backend "s3" {
    dynamodb_table = "i-dot-ai-prod-tfstate"
    bucket         = "i-dot-ai-prod-tfstate"
    key            = "one-big-thing/terraform.tfstate"
    region         = "eu-west-2"
  }
}

provider "aws" {
  region = "us-east-1"
  alias  = "useast1"

  default_tags {
    tags = {
      Environment = var.env
      Project     = "i-dot-ai"
      Name        = "one-big-thing"
    }
  }
}
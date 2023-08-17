data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

data "aws_iam_policy_document" "github" {
  statement {
    sid    = "AssumeRoleWithWebIdentity"
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]

    principals {
      type = "Federated"

      identifiers = [
        data.aws_iam_openid_connect_provider.github.arn,
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com",
      ]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        "repo:i-dot-ai/one-big-thing:*"
      ]
    }
  }
}

resource "aws_iam_role" "github" {
  name               = "${local.project}-${var.env}-gitHubActionsRole"
  description        = "GitHub Actions role for ${local.project} repository."
  assume_role_policy = data.aws_iam_policy_document.github.json
}

#resource "aws_iam_role" "github" {
#  name               = "${local.project}-${var.env}-gitHubActionsRole"
#  description        = "GitHub Actions role for one-big-thing repository."
#  assume_role_policy = data.aws_iam_policy_document.github.json
#}
data "aws_iam_policy_document" "ecr" {
  statement {
    sid    = "GetAuthorizationToken"
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid    = "PutImage"
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
    ]

    resources = [
      data.terraform_remote_state.universal.outputs.one_big_thing_ecr_repo_arn,
      data.terraform_remote_state.universal.outputs.one_big_thing_proxy_ecr_repo_arn,
    ]
  }
}

resource "aws_iam_policy" "ecr" {
  name        = "${local.project}-${var.env}-ECRRepositoryUploadImageAccess"
  description = "Upload image access to one-big-thing ECR repositories."
  policy      = data.aws_iam_policy_document.ecr.json
}

resource "aws_iam_role_policy_attachment" "ecr" {
  role       = aws_iam_role.github.name
  policy_arn = aws_iam_policy.ecr.arn
}
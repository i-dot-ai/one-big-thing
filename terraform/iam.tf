data "aws_iam_policy_document" "secretsmanager" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:eu-west-2:817650998681:*"]
    effect = "Allow"
  }
}

resource "aws_iam_policy" "password_policy_secretsmanager" {
  name = "${local.team}-${local.project}-secretsmanager"
  description = "Secretsmanager IAM policy for ${local.team}-${local.project}"
  policy = data.aws_iam_policy_document.secretsmanager.json
}

resource "aws_iam_role_policy_attachment" "secretsmanager" {
  role       = module.ecs.services["one-big-thing"].tasks_iam_role_name
  policy_arn = aws_iam_policy.password_policy_secretsmanager.arn
}

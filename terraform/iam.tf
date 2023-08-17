data "aws_iam_policy_document" "secretsmanager" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:*"]
    effect = "Allow"
  }
}

resource "aws_iam_policy" "password_policy_secretsmanager" {
  name = "${local.team}-${local.project}-secretsmanager-${var.env}"
  description = "Secretsmanager IAM policy for ${local.team}-${local.project}-${var.env}"
  policy = data.aws_iam_policy_document.secretsmanager.json
}

resource "aws_iam_role_policy_attachment" "secretsmanager" {
  role       = module.ecs.services["one-big-thing-${var.env}"].tasks_iam_role_name
  policy_arn = aws_iam_policy.password_policy_secretsmanager.arn
}

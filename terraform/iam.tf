data "aws_iam_policy_document" "additional" {
  statement {
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [module.db.db_instance_master_user_secret_arn]
  }
}

resource "aws_iam_policy" "additional" {
  name        = "${local.team}-${local.project}-additional-policy"
  description = "Addtion IAM policy for ${local.team}-${local.project}"
  policy      = data.aws_iam_policy_document.additional.json
}

resource "aws_iam_role_policy_attachment" "additional" {
  role       = module.ecs.services["one-big-thing"].tasks_iam_role_name
  policy_arn = aws_iam_policy.additional.arn
}

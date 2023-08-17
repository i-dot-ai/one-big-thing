data "aws_iam_policy_document" "ecs_service_update" {
  statement {
    sid    = "RegisterTaskDefinition"
    effect = "Allow"

    actions = [
      "ecs:RegisterTaskDefinition",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid    = "PassRolesInTaskDefinition"
    effect = "Allow"

    actions = [
      "iam:PassRole",
    ]

    resources = flatten([for service in module.ecs.services : [service.task_exec_iam_role_arn, service.tasks_iam_role_arn]])
  }

  statement {
    sid    = "DeployService"
    effect = "Allow"

    actions = [
      "ecs:UpdateService",
      "ecs:DescribeServices",
    ]

    resources = [for service in module.ecs.services : service.id]
  }

  depends_on = [module.ecs]
}

resource "aws_iam_policy" "ecs_service_update" {
  name        = "${local.project}-${var.env}-ECSServiceUpdateAccess"
  description = "Provides access to update ${local.project}-${var.env} ECS service."
  policy      = data.aws_iam_policy_document.ecs_service_update.json
  depends_on = [module.ecs]
}

resource "aws_iam_role_policy_attachment" "github_ecs_service_update" {
  role       = "${local.project}-${var.env}-gitHubActionsRole"
  policy_arn = aws_iam_policy.ecs_service_update.arn
  depends_on = [module.ecs]
}
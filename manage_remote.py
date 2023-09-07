import boto3
import click

AWS_REGION = "eu-west-2"


def run(env: str, cmd: str, *args: str) -> str:
    """run arbitrary management commands in a remote environment"""
    task_definition_name = f"one-big-thing-{env}"
    container_name = f"one-big-thing-{env}"
    cluster_name = f"i-dot-ai-one-big-thing-{env}"

    session = boto3.Session(profile_name="i-dot-ai")
    ecs_client = session.client("ecs", region_name=AWS_REGION)
    ec2_client = session.client("ec2", region_name=AWS_REGION)
    task_def_arn = ecs_client.list_task_definitions(familyPrefix=task_definition_name, sort="DESC", maxResults=1)[
        "taskDefinitionArns"
    ][0]

    security_group_filters = [
        {"Name": "tag:Environment", "Values": [env]},
        {"Name": "tag:Project", "Values": ["i-dot-ai"]},
        {"Name": "tag:Name", "Values": ["one-big-thing"]},
    ]
    security_groups = ec2_client.describe_security_groups(Filters=security_group_filters)

    # TODO: this is a nasty hack, we must find a better way of labeling the
    # security group
    security_group_id = next(
        security_group["GroupId"]
        for security_group in security_groups["SecurityGroups"]
        if security_group["Description"] == "Managed by Terraform"
    )

    subnet_filters = [
        {"Name": "tag:Environment", "Values": [env]},
        {"Name": "tag:Project", "Values": ["ai-dot-ai"]},
        {"Name": "tag:Name", "Values": [f"i-dot-ai-{env}-vpc-private-eu-west-2b"]},
    ]
    subnets = ec2_client.describe_subnets(Filters=subnet_filters)
    subnet_id = subnets["Subnets"][0]["SubnetId"]

    kwargs = {
        "cluster": cluster_name,
        "taskDefinition": task_def_arn,
        "overrides": {"containerOverrides": [{"name": container_name, "command": ["python", "manage.py", cmd, *args]}]},
        "count": 1,
        "launchType": "FARGATE",
        "platformVersion": "1.4.0",
        "networkConfiguration": {
            "awsvpcConfiguration": {
                "subnets": [subnet_id],
                "securityGroups": [security_group_id],
                "assignPublicIp": "DISABLED",
            }
        },
    }

    task_arn = ecs_client.run_task(**kwargs)["tasks"][0]["taskArn"].split("/")[-1]
    url = (
        f"https://console.aws.amazon.com/ecs/home?region={AWS_REGION}#"
        f"/clusters/{cluster_name}/tasks/{task_arn}/details"
    )

    return url


@click.group()
def cli():
    """execute a limited number of management commands remotely"""
    pass


@cli.command()
@click.option("--env", default="dev", help="environment to run command in.")
def showmigrations(env):
    """show the migrations."""
    task = run(env, "showmigrations")
    click.echo(task)


@cli.command()
@click.option("--env", default="dev", help="environment to run command in.")
def user_stats(env):
    """gather user stats."""
    task = run(env, "user_stats")
    click.echo(task)


if __name__ == "__main__":
    cli()

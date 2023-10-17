# copied, pasted and adapted from https://github.com/azavea/django-ecsmanage
#
# NOTE to developers:
# Right now the management commands exposed are safe, however,
# in the future there may be a good case for adding commands that change the data.
# Add these with caution!!
# Also document unsafe command to ensure that whoever is running them gets that a
# second pair when doing so.

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
        {"Name": "tag:Name", "Values": [f"i-dot-ai-{env}-vpc-private-eu-west-2a"]},
    ]
    subnets = ec2_client.describe_subnets(Filters=subnet_filters)
    assert len(subnets["Subnets"]) == 1, "more than one subnet detected!"
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
    return task_arn


@click.group()
def cli():
    """execute a limited number of management commands remotely"""
    pass


env_option = click.option(
    "--env",
    type=click.Choice(["dev", "prod"]),
    default="dev",
    help="environment to run command in.",
)


@cli.command()
@env_option
def user_stats(env):
    """gather user stats."""
    if env.upper() == "PROD":
        click.secho("this is running things on the (live) server!", fg="red")

    task = run(env, "user_stats")
    click.echo(task)


@cli.command()
@env_option
def get_learning_breakdown_data(env):
    if env.upper() == "PROD":
        click.secho("this is running things on the (live) server!", fg="red")

    task = run(env, "get_learning_breakdown_data")
    click.echo(task)


@cli.command()
@env_option
@click.option("--email", type=str)
@click.option("--password", type=str)
def assign_superuser_status(env, email, password=None):
    """assign superuser status to a user"""
    if env.upper() == "PROD":
        click.secho("this is running things on the (live) server!", fg="red")

    if password is None:
        task = run(env, "assign_superuser_status?", "--email", email)
    else:
        task = run(env, "assign_superuser_status", "--email", email, "--password", password)
    click.echo(task)


@cli.command()
@env_option
@click.argument("arn", type=str)
def get_logs(env, arn):
    if env.upper() == "PROD":
        click.secho("this is running things on the (live) server!", fg="red")

    task_definition_name = f"one-big-thing-{env}"
    container_name = f"one-big-thing-{env}"
    cluster_name = f"i-dot-ai-one-big-thing-{env}"

    url = (
        f"https://console.aws.amazon.com/ecs/home?region={AWS_REGION}#" f"/clusters/{cluster_name}/tasks/{arn}/details"
    )
    click.secho(url, fg="blue")

    log_stream_name = f"ecs/{task_definition_name}/{arn}"
    log_group_name = f"/aws/ecs/{container_name}/{container_name}"

    session = boto3.Session(profile_name="i-dot-ai")
    log_client = session.client("logs", region_name=AWS_REGION)

    log_events = log_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
    )
    for event in sorted(log_events["events"], key=lambda e: e["timestamp"]):
        click.echo(event["message"])

    if not log_events["events"]:
        click.secho("no log events found, maybe try later?", fg="red")


@cli.command()
@env_option
def get_signups_by_date(env):
    if env.upper() == "PROD":
        click.secho("this is running things on the (live) server!", fg="red")

    task = run(env, "get_signups_by_date")
    click.echo(task)


@cli.command()
@env_option
def users_willing_to_follow_up(env):
    if env.upper() == "PROD":
        click.secho("this is running things on the (live) server!", fg="red")

    task = run(env, "users_willing_to_follow_up")
    click.echo(task)


if __name__ == "__main__":
    cli()

import boto3

AWS_REGION = "eu-west-2"
TASK_DEFINITION_NAME = "one-big-thing-dev"
CONTAINER_NAME = "one-big-thing-dev"
CLUSTER_NAME = "i-dot-ai-one-big-thing-dev"
LAUNCH_TYPE = "FARGATE"
PLATFORM_VERSION = "1.4.0"
CMD = ["python", "manage.py", "showmigrations"]


session = boto3.Session(profile_name="i-dot-ai")
ecs_client = session.client("ecs", region_name=AWS_REGION)
ec2_client = session.client("ec2", region_name=AWS_REGION)
task_def_arn = ecs_client.list_task_definitions(familyPrefix=TASK_DEFINITION_NAME, sort="DESC", maxResults=1)[
    "taskDefinitionArns"
][0]

security_group_filters = [
    {"Name": "tag:Environment", "Values": ["dev"]},
    {"Name": "tag:Project", "Values": ["i-dot-ai"]},
    {"Name": "tag:Name", "Values": ["one-big-thing"]},
]
security_groups = ec2_client.describe_security_groups(Filters=security_group_filters)
security_group_id = next(
    security_group["GroupId"]
    for security_group in security_groups["SecurityGroups"]
    if security_group["Description"] == "Managed by Terraform"
)

subnet_filters = [
    {"Name": "tag:Environment", "Values": ["dev"]},
    {"Name": "tag:Project", "Values": ["ai-dot-ai"]},
    {"Name": "tag:Name", "Values": ["i-dot-ai-dev-vpc-private-eu-west-2b"]},
]
subnets = ec2_client.describe_subnets(Filters=subnet_filters)
subnet_id = subnets["Subnets"][0]["SubnetId"]

task_def = ecs_client.describe_task_definition(taskDefinition=task_def_arn)["taskDefinition"]

kwargs = {
    "cluster": CLUSTER_NAME,
    "taskDefinition": task_def_arn,
    "overrides": {"containerOverrides": [{"name": CONTAINER_NAME, "command": CMD}]},
    "count": 1,
    "launchType": LAUNCH_TYPE,
    "platformVersion": PLATFORM_VERSION,
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
    f"https://console.aws.amazon.com/ecs/home?region={AWS_REGION}#" f"/clusters/{CLUSTER_NAME}/tasks/{task_arn}/details"
)

print(url)

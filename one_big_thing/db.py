import base64
import json

import boto3

AWS_REGION = "eu-west-2"


def get_secret(name: str):
    secrets_manager = boto3.client(service_name="secretsmanager", region_name=AWS_REGION)
    reponse = secrets_manager.get_secret_value(SecretId=name)

    if "SecretString" in reponse:
        return reponse["SecretString"]
    else:
        return base64.b64decode(reponse["SecretBinary"])


def fetch_db_password(secret_name):
    return json.loads(get_secret(secret_name))["password"]


def fetch_generic_secret(secret_name):
    return json.loads(get_secret(secret_name))[secret_name]

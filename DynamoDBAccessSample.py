import boto3

dynamodb = boto3.resource("dynamodb")
tables = dynamodb.Table("VocaloidSongs")


def handler(event, context):
    tables.wait_until_exists()
    print(tables.creation_date_time)
    return "Success"


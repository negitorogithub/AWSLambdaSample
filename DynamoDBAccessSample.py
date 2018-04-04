import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("VocaloidSongs")


def handler(event, context):
    table.wait_until_exists()
    print(table.creation_date_time)
    table.put_item(
        Item={
            "Producer" : "Sasakure.UK",
            "SongTitle": "終末がやってくる！"
        }
    )
    return "Success return"


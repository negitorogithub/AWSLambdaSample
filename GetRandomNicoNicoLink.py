import boto3
import random
from boto3.dynamodb.conditions import Key


def handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("VocaloidSongsTable")
    table.wait_until_exists()
    ITEM_COUNT = table.item_count

    for i in range(1, 100):
        song_id_to_query = random.randrange(0, ITEM_COUNT)
        link = getRandomLink(table, song_id_to_query)
        if link:
            return link


def getRandomLink(table, song_id_to_query):
    song_in_table = table.query(
        IndexName='id-index2',
        KeyConditionExpression=Key('id').eq(str(song_id_to_query))
    )
    #       成功時には中身が入る

    if "Items" in song_in_table.keys():
        return {
            "link": song_in_table["Items"][0]["NicoNicoLink"]
        }
    else:
        return False

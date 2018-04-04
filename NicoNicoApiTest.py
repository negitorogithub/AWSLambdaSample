import requests
from bs4 import BeautifulSoup


def handler(event, context):
    response = requests.get("http://ext.nicovideo.jp/api/getthumbinfo/sm3033822")
    print(BeautifulSoup(response.text))
    return "Success"



print(handler("", ""))

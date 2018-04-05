import boto3
import requests
import typing
from bs4 import BeautifulSoup


class Song:
    def __init__(self):
        self.title = ""
        self.niconicoLinks = []
        self.niconicoThumbnailLink = ""
        self.youtubeLinks = []
        self.youtubeThumbnailLink = ""
        self.niconicoAuthorId = -1

    # 曲説明のページを渡す
    def apply_info_by_wiki_page(self, soup: BeautifulSoup)-> "Song":
        self.title = soup.find("title").text.replace(" - 初音ミク Wiki - アットウィキ", "")
        youtube_tag = (soup.find(class_="test"))
        if youtube_tag:
            self.youtubeLinks.append(youtube_tag.get("href"))
        else:
            pass

        # "iframe"はニコニコ埋め込みのタグ
        iframe_tags = soup.find_all("iframe")
        for iframe_tag in iframe_tags:
            niconico_link_tag = iframe_tag.find("a")
            if niconico_link_tag:
                self.niconicoLinks.append(niconico_link_tag.get("href"))
            else:
                pass

        return self

    # http://ext.nicovideo.jp/api/getthumbinfo/sm***　のページを渡す
    def apply_info_by_niconico_api(self, soup: BeautifulSoup)-> "Song":
        self.niconicoAuthorId = soup.find("user_id").string
        self.niconicoThumbnailLink = soup.find("thumbnail_url").string
        return self


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("VocaloidSongs")


def handler(event, context):
    all_songs = find_songs_in_rss()

    table.wait_until_exists()

    print(table.creation_date_time)
    table.put_item(
        Item={
            "Producer": "Sasakure.UK",
            "SongTitle": "終末がやってくる！",
            "NicoNicoUrl": "None",

        }
    )
    return "Success return"


def find_songs_in_rss()->typing.List[Song]:
    response = requests.get("https:/]/www5.atwiki.jp/hmiku/rss10_new.xml")
    all_pages_url = [ref_li_tag["rdf:resource"]
                     for ref_li_tag
                     in BeautifulSoup(response.text, "xml").find_all("rdf:li")]
    songs = [Song().apply_info_by_wiki_page(BeautifulSoup(requests.get(page_url).text, "xml"))
             for page_url
             in all_pages_url]
    #TODO apply_info_by_niconico_apiを適用させる
    return songs




#print([song.niconicoLinks for song in songs])

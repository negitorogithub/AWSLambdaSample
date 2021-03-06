import boto3
from boto3.dynamodb.conditions import Key
import requests
import typing
from bs4 import BeautifulSoup

MAX_SCRAPING_SONG_AMOUNT = 30


class Song:
    def __init__(self):
        self.title = ""
        self.songId = -1
        self.niconicoLinks = []
        self.niconicoThumbnailLink = ""
        self.youtubeLinks = []
        self.youtubeThumbnailLink = ""
        self.niconicoAuthorId = -1
        self.niconicoAuthorName = ""
        self.otherLinks = []



    # 曲説明のページを渡す
    def apply_info_by_wiki_page(self, soup: BeautifulSoup)-> "Song":
        self.title = soup.find("title").text.replace(" - 初音ミク Wiki - アットウィキ", "")
        youtube_tag = (soup.find(class_="test"))
        if youtube_tag:
            self.youtubeLinks.append(youtube_tag.get("href"))
        else:
            pass

        # "iframe"はニコニコ埋め込みのタグ
        iframe_tags = soup.find(id="wikibody").find_all("iframe")
        for iframe_tag in iframe_tags:
            niconico_link_tag = iframe_tag.find("a")
            if "www.nicovideo.jp/watch/" in niconico_link_tag.get("href"):
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
table = dynamodb.Table("VocaloidSongsTable")


def handler(event, context):

    response = requests.get("https://www5.atwiki.jp/hmiku/pages/238.html")
    all_songs = find_new_songs(BeautifulSoup(response.text))
    table.wait_until_exists()
    ITEM_COUNT = table.item_count
    new_song_count = 0

    """
    song_in_table = table.query(
        IndexName="id-index2",
        KeyConditionExpression=Key("id").
    )
    print(song_in_table)
    """

    for song in all_songs:
        if len(song.youtubeLinks) == 0:
            song.youtubeLinks = [None]

        if len(song.niconicoLinks) == 0:
            song.niconicoLinks = [None]

        song_in_table = table.get_item(Key={"Title": song.title})

#       成功時には中身が入る
        if "Item" in song_in_table.keys():
            table.update_item(
                Key={
                    "Title": str(song_in_table["Item"]["Title"]),
                },
                UpdateExpression="set NicoNicoLink=:ni, YoutubeLink=:yo",
                ExpressionAttributeValues={
                                            ':ni': song.niconicoLinks[0],
                                            ':yo': song.youtubeLinks[0],
                },
            )
        else:
            new_song_count += 1
            table.put_item(
                Item={
                    "id": str(ITEM_COUNT + new_song_count),
                    "Title": str(song.title),
                    "NicoNicoLink": song.niconicoLinks[0],
                    "YoutubeLink": song.youtubeLinks[0]
                }
            )

    return "Success return"


"""


"""


def find_songs_in_rss()->typing.List[Song]:
    response = requests.get("https://www5.atwiki.jp/hmiku/rss10_new.xml")
    print(response.text)
    all_pages_url = [ref_li_tag["rdf:resource"]
                     for ref_li_tag
                     in BeautifulSoup(response.text).find_all("rdf:li")]
    print(all_pages_url)
    songs = [Song().apply_info_by_wiki_page(BeautifulSoup(requests.get(page_url).text))
             for page_url
             in all_pages_url]
    print(songs)
    return songs


def find_new_songs(soup: BeautifulSoup)->"typing.List[Song]":
    edge_songs_a_tags = [a_tag
                         for a_tag
                         in
                         soup.find("div", class_="plugin_list_by_tag").find_all("a")
                         ]

    edge_songs = []
    for edge_song_a_tag in edge_songs_a_tags:
        song2add = Song()
        song2add.title = edge_song_a_tag.string
        wiki_page = requests.get("https:"+edge_song_a_tag["href"])
        song2add.apply_info_by_wiki_page(BeautifulSoup(wiki_page.text))
        edge_songs.append(song2add)
        if len(edge_songs) > MAX_SCRAPING_SONG_AMOUNT:
            break
    return edge_songs


import boto3
import requests
import typing
from bs4 import BeautifulSoup


class Song:
    def __init__(self):
        self.title = ""
        self.niconicoLinks = None
        self.niconicoThumbnailLink = ""
        self.youtubeLinks = None
        self.youtubeThumbnailLink = ""
        self.niconicoAuthorId = -1
        self.niconicoAuthorName = ""
        self.otherLinks = None

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
    edge_songs_names = [a_tag.string
                        for a_tag
                        in
                        soup.find("div", class_="plugin_list_by_tag").find_all("a")
                        ]
    songs = []
    for edge_song_name in edge_songs_names:
        song2add = Song()
        song2add.title = edge_song_name
        songs.append(song2add)
    return songs


response = requests.get("https://www5.atwiki.jp/hmiku/pages/238.html")
all_songs = find_new_songs(BeautifulSoup(response.text))
for song in all_songs:
    print(song.title)




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
        self.niconicoAuthorName = ""
        self.otherLinks = []

    # 曲説明のページを渡す
    def apply_info_by_wiki_page(self, soup: BeautifulSoup)-> "Song":

        self.title = soup.find("title").text.replace(" - 初音ミク Wiki - アットウィキ", "")
        print("applying "+self.title)
        youtube_tag = (soup.find(class_="test"))
        if youtube_tag:
            self.youtubeLinks.append(youtube_tag.attrs["href"])
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


def find_songs_in_rss()->typing.List[Song]:
    response_rss = requests.get("https://www5.atwiki.jp/hmiku/rss10_new.xml")
    print(response_rss.text)
    all_pages_url = [ref_li_tag["rdf:resource"]
                     for ref_li_tag
                     in BeautifulSoup(response_rss.text).find_all("rdf:li")]
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
        song2add.title_ = edge_song_a_tag.string
        wiki_page = requests.get("https:" + edge_song_a_tag["href"])
        song2add.apply_info_by_wiki_page(BeautifulSoup(wiki_page.text))
        edge_songs.append(song2add)
        if len(edge_songs) > 20:
            break
    return edge_songs


response = requests.get("https://www5.atwiki.jp/hmiku/pages/238.html")
all_songs = find_new_songs(BeautifulSoup(response.text))
for song in all_songs:
    print(song.niconicoLinks)

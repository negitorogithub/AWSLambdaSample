import typing

from bs4 import BeautifulSoup
import requests


class Song:
    def __init__(self):
        self.title = ""
        self.nikonikoLinks = []
        self.nikonikoCount = -1
        self.nikonikoThumbnailLink = ""
        self.youtubeLinks = []
        self.youtubeCount = -1
        self.youtubeThumbnailLink = ""
        self.authors = []

    # 曲説明のページを渡す
    def apply_info_by_page(self, soup: BeautifulSoup)-> "Song":
        self.title = soup.find("title").text.replace(" - 初音ミク Wiki - アットウィキ", "")

        youtube_tag = (soup.find(class_="test"))
        if youtube_tag:
            self.youtubeLinks.append(youtube_tag.get("href"))
        else:
            pass

        # "iframe"はニコニコ埋め込みのタグ
        iframe_tags = soup.find_all("iframe")
        for iframe_tag in iframe_tags:
            nikoniko_link_tag = iframe_tag.find("a")
            if nikoniko_link_tag:
                self.nikonikoLinks.append(nikoniko_link_tag.get("href"))
            else:
                pass
        return self


def find_new_songs(soup: BeautifulSoup)->"typing.List[Song]":
    edge_songs_names = [a_tag.string
                        for a_tag
                        in
                        soup.find("div", class_="plugin_list_by_tag").find_all("a")
                        ]
    songs = []
    for edge_song_name in edge_songs_names:
        songs.append(Song())
        songs[len(songs)-1].title = edge_song_name
    return songs


response = requests.get("https://www5.atwiki.jp/hmiku/pages/238.html")
for song in find_new_songs(BeautifulSoup(response.text)):
    print(song.title)

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


response = requests.get("https://www5.atwiki.jp/hmiku/rss10_new.xml")
all_pages_url = [ref_li_tag["rdf:resource"]
                 for ref_li_tag
                 in BeautifulSoup(response.text, "xml").find_all("rdf:li")]
print(all_pages_url)
songs = [Song().apply_info_by_page(BeautifulSoup(requests.get(page_url).text, "xml")) for page_url in all_pages_url]
print([song.nikonikoLinks for song in songs])


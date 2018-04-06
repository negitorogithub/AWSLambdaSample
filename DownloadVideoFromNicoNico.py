from bs4 import BeautifulSoup
import requests

response = requests.get("http://www.nicovideo.jp/watch/sm32574538")
print(response.text)

"""
soup = BeautifulSoup(response.text)
video_tag = soup.find("video")
video_url = video_tag["src"]

print(video_url)
"""

import requests
from bs4 import BeautifulSoup

TOKEN = "rTNAfXuSPK2GWd6eXtmZwuHVMitzHO-iAl5CKKPNiQ-m2arGCN7eqRRRy7v1F6j8"

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer '+TOKEN}

def getLyrics(songTitle, artist):
  song_title = songTitle
  artist_name = artist

  def prune(lyrics):
    lines = lyrics.split('\n')
    pruned = ""
    for line in lines:
      if line.find('[') == -1 and len(line) > 0:
        pruned += line + '\n'
    return pruned

  def verseExtractor(lyrics):
    lines = lyrics.split('\n')
    pruned = ""
    inVerse = False
    for line in lines:
      if inVerse:
        if line.find('[') == -1 and len(line) > 0:
          pruned += line + '\n'
        else:
          inVerse = False
      if line.find('[Verse') > -1:
        inVerse = True
    return pruned


  def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("lyrics").get_text()
    lyrics = verseExtractor(lyrics)
    return lyrics



  search_url = base_url + "/search"
  data = {'q': song_title}
  response = requests.get(search_url, data=data, headers=headers)
  json = response.json()
  song_info = None
  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == artist_name:
      song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    return lyrics_from_song_api_path(song_api_path)


# song_title = "Backseat Freestyle"
# artist_name = "Kendrick Lamar"
# print getLyrics(song_title, artist_name)
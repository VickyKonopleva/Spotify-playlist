import re
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
pp = pprint.PrettyPrinter(indent=1)
REDIRECT_URI="http://example.com"
CLIENT_ID="97e6c746a80641c4ae9158e9b207079c"
CLIENT_SECRET="ea6bb5c98a4445cb9b2760cb7a27c318"
URL="https://www.billboard.com/charts/hot-100"
PLAYLIST_ID="0o68EagK9hFU0q2V9Fdo1x"


#SEARCHING FOR A SONGS LIST THROUGH A WEBSITE
date=input("What time would you like to travel to? YYYY-MM-DD\n")
year=date.split("-")[0]

response=requests.get(url=f"{URL}/{date}")
songs_web_page=response.text
soup=BeautifulSoup(songs_web_page, "html.parser")
song_names=[]
singers=[]
names=soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
artists=soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
for song in names:
    song_names.append(song.getText())

for artist in artists:
    singers.append(artist.getText())

dict={}
for i in range (len(singers)-1):
    dict.update({singers[i]:song_names[i]})
print(dict)

#INTERACTION WITH SPOTIFY
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path=".cache"))

user_id = sp.current_user()["id"]


#SEARCHING FOR A SONG URI

songs_uris=[]
for song in song_names:
    try:
        res=sp.search(q="track:" + song + " year:" + year, type="track", limit=1)["tracks"]["items"][-1]["uri"]
    except:
        pass
    else:
        songs_uris.append(res)

playlist_id=sp.user_playlist_create(user=user_id, name=date, public=False)["id"]
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=songs_uris)












import json
import requests
from bs4 import BeautifulSoup
import datetime as dt
import spotipy

USERNAME = YOUR_SPOTIFY_USERNAME
CLIENT_ID = YOUR_SPOTIFY_API_ID
CLIENT_SECRET = YOUR_SPOTIFY_API_SECRET

# get date entry from user
valid = False
while not valid:
    date_of_playlist = input("What date would you like to travel to? (MM-DD-YYY):\n")
    if date_of_playlist.split("-") == 3:
        print("Please separate numbers with a '-'")
        continue
    try:
        month = int(date_of_playlist.split("-")[0].strip())
        day= int(date_of_playlist.split("-")[1].strip())
        year = int(date_of_playlist.split("-")[2].strip())
    except (TypeError or ValueError):
        print("Only integers please")
        continue
    else:
        try:
            date_obj = dt.date(year, month, day)
        except ValueError:
            raise Exception("Invalid Date")
        else:
            valid = True
if month < 10:
    month = f"0{month}"
if day < 10:
    day = f"0{day}"

# get html from top 100 songs from date
billboard = f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}"
response = requests.get(url=billboard)

# convert html to soup
soup = BeautifulSoup(response.text, "html.parser")
song_artists = []
song_list = []
song_box = soup.find_all(name="div", class_="o-chart-results-list-row-container")# list containing all the element information

# for each song on website, mine song title and artist
for song in song_box:
    song_box1 = song.find('li',class_="lrv-u-width-100p")
    song_box2 = song_box1.find('li',class_="o-chart-results-list__item")
    song_name = song_box1.find('h3',id="title-of-a-story").text.strip('\n')
    song_box3 = song_box2.find('span',class_='c-label').text
    song_artist = song_box3.strip('\n')
    song_artists.append(song_artist)
    song_list.append(song_name)

# get OAuth token for USERNAME
# completed once, not needed again.
# if first run results in error, try again. Sometimes the token gets updated but still fails on first run
new_auth = spotipy.oauth2.SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://example.com/",
        show_dialog=True,
        scope="playlist-modify-private",
        cache_path=".cache")

with open(".cache", "r") as file:
    auth_text = file.read()

# get authentication token from json data file that loaded from newly created cache file
auth_dict = json.loads(auth_text)
auth_token = auth_dict["access_token"]
refresh_token = auth_dict["refresh_token"]

# "log in" from authentication data
new_user = spotipy.client.Spotify(auth=auth_token)

# try to get user id from api function
# Error handling, if first sign in fails create new client and try again. if error, try running again
try:
    user_id = new_user.current_user()["display_name"]
except spotipy.exceptions.SpotifyException:
    refresh = new_auth.refresh_access_token(refresh_token)
    print(refresh)
    refresh_token = refresh["refresh_token"]
    new_user = spotipy.client.Spotify(auth=refresh_token)
    user_id = new_user.current_user()["display_name"]

# Get song data
search_endpoint = "https://api.spotify.com/v1/search"
count = 0
track_id_list = []

# for each song in song list,
for songs in song_list:

    # design query {artist AND song} - > search query - > get track ID
    try:
        query = f"artist:{song_artists[count]} track:{song_list[count]}"
        track_info = new_user.search(q=query)
        track_id = track_info["tracks"]["items"][0]["id"]

    # if no track ID, serch again but just {song}
    except IndexError:
        try:
            query = f"track:{song_list[count]}"
            track_info = new_user.search(q=query)
            track_id = track_info["tracks"]["items"][0]["id"]

        # if error, song cannot be found, skip
        except IndexError:
            count += 1
            continue
        else:
            count += 1
            track_id_list.append(track_id)
    else:
        count += 1
        track_id_list.append(track_id)

# create new playlist
playlist = new_user.user_playlist_create(user=user_id, name=f"Top 100 for {month}-{day}-{year}",
                                         public=False,
                                         description=f"Billboard top 100 for {month}-{day}-{year}")
# add items to playlist
new_user.playlist_add_items(playlist_id=playlist["id"], items=track_id_list)

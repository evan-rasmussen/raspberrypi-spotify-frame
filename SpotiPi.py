import spotipy
import datetime
import requests
from time import sleep
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "31067bbc7709464cae84a8e834d1d7b4" #client ID
SPOTIPY_CLIENT_SECRET = "2f3f38aea497433e9c2a2678732a6456" #client secrent
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback/'

scope = "user-read-currently-playing" #scope of what we want to access

def main():
    # new spotipy application
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
					scope=scope,
					client_id=SPOTIPY_CLIENT_ID,
					client_secret=SPOTIPY_CLIENT_SECRET,
					redirect_uri=SPOTIPY_REDIRECT_URI))

    #infinite loop
    while True:
        #get the currently playing track item
        print("getting track...")
        track = sp.current_user_playing_track()
        if not track == None:
	    # extract track name from item
            track_name = track['item']['name']

	    # format the release date from Y-m-d to M/D/Y
            release_date = datetime.datetime.strptime(track['item']['album']['release_date'], '%Y-%m-%d')
            release_date = '{0}/{1}/{2}'.format(release_date.month, release_date.day, release_date.year)

            # get artist list
            artists = []
            for artist in track['item']['artists']:
                artists.append(artist['name'])

            # format artist list to include commas in-between artist names
            artists_str = ""
            for i in range(len(artists)-1):
                artists_str += artists[i] + ", "
            artists_str += artists[len(artists)-1] # append last artist without comma

            print(f"{track_name}/n{artists_str}/n{release_date}")
            # gets the 64x64 album art URL
            img_url = track['item']['album']['images'][2]['url']
            # get the actual image
            response = requests.get(img_url).content
            # open image file and save locally
            image = open("album_art.png", "wb")
            image.write(response)
            image.close()
            sleep(60)
        else:
            sleep(10)

if __name__=="__main__":
    main()

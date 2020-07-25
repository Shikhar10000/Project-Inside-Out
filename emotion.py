from __future__ import print_function
import spotify
import sys
import spotipy
from python_utils import*
import os
from util import prompt_for_user_token
from spotify_local import SpotifyLocal
import oauth2
import client
import random
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore



cred = credentials.Certificate("insideout-d7b9f-917ca2d27c46.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'appreciation').limit(100000000)

try:
    docs = doc_ref.get()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')
	
#
a = doc.to_dict()
listx = list(a.items()) 
b = listx[0][1]
print(b)

mood = b
client_id = 'e78a9e994e544c60a551186a93440214'
client_secret = '946f2ab97326448f9b5be8194806c849'
redirect_uri = 'https://localhost:8008'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
username='4svyvf1988xwob4idzpyhy3q5'

# with SpotifyLocal() as s:
	# pass

def prompt_for_user_token(username, scope=None, client_id = None,
        client_secret = None, redirect_uri = None, cache_path = None):
    ''' prompts the user to login if necessary and returns
        the user token suitable for use with the spotipy.Spotify 
        constructor
        Parameters:
         - username - the Spotify username
         - scope - the desired scope of the request
         - client_id - the client id of your app
         - client_secret - the client secret of your app
         - redirect_uri - the redirect URI of your app
         - cache_path - path to location to save tokens
    '''
    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        print('''
            You need to set your Spotify API credentials. You can do this by
            setting environment variables like so:
            export SPOTIPY_CLIENT_ID='your-spotify-client-id'
            export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
            export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
            Get your credentials at     
                https://developer.spotify.com/my-applications
        ''')
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    cache_path = cache_path or ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=scope, cache_path=cache_path)

    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print('''
            User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.
        ''')
        auth_url = sp_oauth.get_authorize_url()
        try:
            import webbrowser
            webbrowser.open(auth_url)
            print("Opened %s in your browser" % auth_url)
        except:
            print("Please navigate here: %s" % auth_url)

        print()
        print()
        try:
            response = raw_input("Enter the URL you were redirected to: ")
        except NameError:
            response = input("Enter the URL you were redirected to: ")

        print()
        print() 

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    # Auth'ed API request
    if token_info:
        return token_info['access_token']
    else:
        return None
token = prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)


if token:
	
	#Step 1. Authenticating Spotipy

	def authenticate_spotify():
		print('...connecting to Spotify')
		sp = spotipy.Spotify(auth=token)
		return sp

    #Step 2. Creating a list of your favorite artists

	def aggregate_top_artists(sp):
		print('...getting your top artists')
		top_artists_name = []
		top_artists_uri = []

		ranges = ['short_term', 'medium_term', 'long_term']
		for r in ranges:
			top_artists_all_data = sp.current_user_top_artists(limit=50, time_range= r)
			top_artists_data = top_artists_all_data['items']
			for artist_data in top_artists_data:
				if artist_data["name"] not in top_artists_name:		
					top_artists_name.append(artist_data['name'])
					top_artists_uri.append(artist_data['uri'])

		followed_artists_all_data = sp.current_user_followed_artists(limit=50)
		followed_artists_data = (followed_artists_all_data['artists'])
		for artist_data in followed_artists_data["items"]:
			if artist_data["name"] not in top_artists_name:
				top_artists_name.append(artist_data['name'])
				top_artists_uri.append(artist_data['uri'])
		return top_artists_uri


    #Step 3. For each of the artists, get a set of tracks for each artist
    
	def aggregate_top_tracks(sp, top_artists_uri):
		print("...getting top tracks")
		top_tracks_uri = []
		for artist in top_artists_uri:
			top_tracks_all_data = sp.artist_top_tracks(artist)
			top_tracks_data = top_tracks_all_data['tracks']
			for track_data in top_tracks_data:
				top_tracks_uri.append(track_data['uri'])
		return top_tracks_uri

	# Step 4. From top tracks, select tracks that are within a certain mood range

	def select_tracks(sp, top_tracks_uri):
		
		print("...selecting tracks")
		selected_tracks_uri = []

		def group(seq, size):
			return (seq[pos:pos + size] for pos in range(0, len(seq), size))

		random.shuffle(top_tracks_uri)
		for tracks in list(group(top_tracks_uri, 50)):
			tracks_all_data = sp.audio_features(tracks)
			for track_data in tracks_all_data:
				try:
					if mood < 0.10:
						if (0 <= track_data["valence"] <= (mood + 0.15)
						and track_data["danceability"] <= (mood*8)
						and track_data["energy"] <= (mood*10)):
							selected_tracks_uri.append(track_data["uri"])					
					elif 0.10 <= mood < 0.25:						
						if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
						and track_data["danceability"] <= (mood*4)
						and track_data["energy"] <= (mood*5)):
							selected_tracks_uri.append(track_data["uri"])
					elif 0.25 <= mood < 0.50:						
						if ((mood - 0.05) <= track_data["valence"] <= (mood + 0.05)
						and track_data["danceability"] <= (mood*1.75)
						and track_data["energy"] <= (mood*1.75)):
							selected_tracks_uri.append(track_data["uri"])
					elif 0.50 <= mood < 0.75:						
						if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
						and track_data["danceability"] >= (mood/2.5)
						and track_data["energy"] >= (mood/2)):
							selected_tracks_uri.append(track_data["uri"])
					elif 0.75 <= mood < 0.90:						
						if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
						and track_data["danceability"] >= (mood/2)
						and track_data["energy"] >= (mood/1.75)):
							selected_tracks_uri.append(track_data["uri"])
					elif mood >= 0.90:
						if ((mood - 0.15) <= track_data["valence"] <= 1
						and track_data["danceability"] >= (mood/1.75)
						and track_data["energy"] >= (mood/1.5)):
							selected_tracks_uri.append(track_data["uri"])
				except TypeError as te:
					continue

		return selected_tracks_uri			

	# Step 5. From these tracks, create a playlist for user

	def create_playlist(sp, selected_tracks_uri):

		print("...creating playlist")
		user_all_data = sp.current_user()
		user_id = user_all_data["id"]

		playlist_all_data = sp.user_playlist_create(user_id, "Inside Out " + str(mood))
		playlist_id = playlist_all_data["id"]

		random.shuffle(selected_tracks_uri)
		sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri[0:30])


	spotify_auth = authenticate_spotify()
	top_artists = aggregate_top_artists(spotify_auth)
	top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
	selected_tracks = select_tracks(spotify_auth, top_tracks)
	create_playlist(spotify_auth, selected_tracks)
else:
    print("Can't get token for", username)
#

# with SpotifyLocal() as s:
        # print(s.get_current_status())
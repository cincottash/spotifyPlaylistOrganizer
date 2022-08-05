import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import pprint 
import spotipy.util as util
import requests
pp = pprint.PrettyPrinter(indent=1)


masterID = '**************'
clientID = '**************'
userID = '**************'
clientSecret = '**************'

#client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret='47030e7e93314cefbc42ef18d9e1e705')
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = userID
token = util.prompt_for_user_token(
    scope='playlist-modify-public playlist-modify-private', 
    client_id=clientID, 
    client_secret=clientSecret, 
    redirect_uri="http://localhost:8888/callback"

)
sp = spotipy.Spotify(auth=token)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

masterID = '5rIfKE22hnQfVojjYI6xre'
userID = 'f0afa03a332f4f499904815cdee524fe'

auth_manager = SpotifyClientCredentials('f0afa03a332f4f499904815cdee524fe', 'ff2fce807bb94c5cb9827eb913d9213c')
sp = spotipy.Spotify(auth_manager=auth_manager)
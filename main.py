from setup import *

def get_playlist_tracks(username, playlist_id):
	results = sp.user_playlist_tracks(username,playlist_id)
	
	tracks = results['items']
	
	while results['next']:
		results = sp.next(results)
		
		#w/o this we only get the first 100 results
		tracks.extend(results['items'])
	
	return tracks

def getTrackGenres(track):
	#genre of the first named artist from the track is associated with
	trackGenres = sp.artist(track['track']['artists'][0]["external_urls"]["spotify"])['genres']

	return trackGenres

def main():
	masterTracks = get_playlist_tracks(userID, masterID)

	for track in masterTracks:
		trackName = track['track']['name']
		
		#List of all the genres an artist is associated with
		trackGenres = getTrackGenres(track)

		#print(trackGenres)

		#TODO: Add track to a playlist according to each genre the artist is associated with

		#check a playlist for each genre already exists, if it does, add this song to that playlist, if not, make the playlist and add the song





		#only do the first track for testing
		break

if __name__ == '__main__':
	main()
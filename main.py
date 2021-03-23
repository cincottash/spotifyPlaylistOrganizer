from setup import *
import requests

def getPlaylistTracks(username, playlist_id):
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

def getUserPlaylists(username):
	playlistsData = sp.user_playlists(username)
	playlistNames = []

	for item in playlistsData['items']:
		playlistNames.append(item['name'])

	return playlistNames

def checkPlaylistExists(genre, playlistNames):
	if genre in playlistNames:
		return True

	return False

#get playlist id from its name attribute
def getPlaylistID(playlistName, username):

	#THIS HAS A LIMIT OF 50 AND IS FUCKING EVERYTHIN UP
	playlistsData = sp.user_playlists(username, limit=50)
	print(len(playlistsData['items']))
	for item in playlistsData['items']:
		#print(item['name'])
		if item['name'] == playlistName:
			playlistID = item['id']
			return playlistID
	return None

	

def addSongToPlaylist(playlistID, trackID):
	#user_playlist_add_tracks(user, playlist_id, tracks, position=None)
	sp.user_playlist_add_tracks(userID, playlistID, [trackID], position=None)


def makePlaylist(playlistName):
	sp.user_playlist_create(userID, playlistName, public=True)


def main():
	masterTracks = getPlaylistTracks(clientID, masterID)
	playlistNames = getUserPlaylists(userID)
	print(playlistNames)

	for track in masterTracks:
		trackName = track['track']['name']

		trackID = track['track']['id']
		print(trackName)

		#List of all the genres an artist is associated with
		trackGenres = getTrackGenres(track)
		print(trackGenres)
		print('\n')
		#for each genre associated with an artists, check if a playlist with that name already exists
		for genre in trackGenres:
			if not checkPlaylistExists(genre, playlistNames):
				print('playlist for genre {} not found, creating playlist {}'.format(genre, genre))
				makePlaylist(genre)
				playlistNames.append(genre)
				playlistID = getPlaylistID(genre, userID)
			else:
				print('playlist found for genre {}'.format(genre))
				playlistID = getPlaylistID(genre, userID)
			
			#Sometimes playlistID is none and idk why, it ends up skipping that song
			if(playlistID == None):
				print('Couldnt get playlistID of genre {}, skipping genre {}'.format(genre, genre))
				print(playlistNames)
				exit(0)
				continue
			else:
				#check if song already exsists in playlist
				playlistTracks = getPlaylistTracks(clientID, playlistID)
				
				trackExists = False
				for playlistTrack in playlistTracks:
					if playlistTrack['track']['id'] == trackID:
						trackExists = True
						print('Track {} already exists in playlist {}, skipping track\n'.format(trackName, genre))
						break
					trackExists = False

				if not trackExists:
					print('adding {} to {}\n'.format(trackName, genre))			
					addSongToPlaylist(playlistID, trackID)
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~\n')


if __name__ == '__main__':
	main()

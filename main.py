from setup import *

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
	trackGenres = sp.artist(track['track']['artists'][0]['external_urls']['spotify'])['genres']

	return trackGenres

def getUserPlaylists(username):
	playlistsData = sp.user_playlists(username)
	
	playlistNames = []

	offset = 0
	while(len(playlistsData['items']) >= 50):
		playlistsData = sp.user_playlists(username, offset = offset)
		for item in playlistsData['items']:
			if item['name'] not in playlistNames:
				playlistNames.append(item['name'])
		offset += 50
	return playlistNames

def checkPlaylistExists(genre, playlistNames):
	if genre in playlistNames:
		return True

	return False

#get playlist id from its name attribute
def getPlaylistID(playlistName, username):
	foundID = False
	offset = 0
	while(True):
		#THIS HAS A LIMIT OF 50 SO THATS WHY IM IN A WHILE LOOP AHHHH FML
		playlistsData = sp.user_playlists(username, offset = offset)

		for item in playlistsData['items']:
			if item['name'] == playlistName:
				playlistID = item['id']
				return playlistID

		offset += 50

def addSongToPlaylist(playlistID, trackID):
	#user_playlist_add_tracks(user, playlist_id, tracks, position=None)
	sp.user_playlist_add_tracks(userID, playlistID, [trackID], position=None)
	
def makePlaylist(playlistName):
	sp.user_playlist_create(userID, playlistName, public=True)


def main():
	masterTracks = getPlaylistTracks(clientID, masterID)
	
	playlistNames = getUserPlaylists(userID)
	print(playlistNames)
	
	totalTracks = len(masterTracks)
	
	completedTracks = 0
	
	for track in masterTracks:
		print('Completed {} / {} tracks'.format(completedTracks, totalTracks))
		trackName = track['track']['name']

		trackID = track['track']['id']
		print(trackName)

		#List of all the genres an artist is associated with
		trackGenres = getTrackGenres(track)
		print('{}\n'.format(trackGenres))
		
		#for each genre associated with an artists, check if a playlist with that name already exists
		for genre in trackGenres:
			if not checkPlaylistExists(genre, playlistNames):
				print('playlist for genre {} not found, creating playlist {}'.format(genre, genre))
				makePlaylist(genre)
				playlistNames.append(genre)
			else:
				print('playlist found for genre {}'.format(genre))
			
			#check if song already exsists in playlist
			try:
				playlistID = getPlaylistID(genre, userID)
				playlistTracks = getPlaylistTracks(clientID, playlistID)
			except requests.exceptions.ReadTimeout:
				print('Timeout error, attempting to re-add track to playlist')
				playlistID = getPlaylistID(genre, userID)
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
		completedTracks +=1 
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~\n')


if __name__ == '__main__':
	main()


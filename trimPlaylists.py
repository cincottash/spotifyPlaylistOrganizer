from setup import *

def getUserPlaylists(username):
	playlistsData = sp.user_playlists(username)
	
	playlists = []
	'''
	playlistsData = sp.user_playlists(username)
	for item in playlistsData['items']:
		if item['name'] not in playlists:
			playlists.append(item)
	'''

	offset = 0
	while(len(playlistsData['items']) >= 50):
		playlistsData = sp.user_playlists(username, offset = offset)
		for item in playlistsData['items']:
			if item['name'] not in playlists:
				playlists.append(item)
		offset += 50
	return playlists

def main():
	#iterate over each playlist and list the ID, Name and Size (song count)
	playlistsData = getUserPlaylists(userID)
	playlistsDeleted = 0
	playListsToDelete = []

	for playlist in playlistsData:
		'''
		print(pp.pprint(playlist))
		print('\n')
		print(count)
		'''
		playlistName = playlist['name']
		playlistID = playlist['id']
		playlistTotalTracks = playlist['tracks']['total']
		
		if(playlistName in playListsToDelete):
			print('DELETING NAME: {} ID: {} TOTAL TRACKS: {}'.format(playlistName, playlistID, playlistTotalTracks))
			
			#Unfollows (deletes) a playlist for a user
			sp.user_playlist_unfollow(userID, playlistID)
			
			playlistsDeleted += 1
			print('Playlists Deleted: {}\n'.format(playlistsDeleted))

		#pp.pprint(playlist)






main()
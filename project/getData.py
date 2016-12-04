import getLyrics, getArtistId
import unidecode 

def getData(artistName):
	Data = []
	client_access_token = "rTNAfXuSPK2GWd6eXtmZwuHVMitzHO-iAl5CKKPNiQ-m2arGCN7eqRRRy7v1F6j8"
	songs = getArtistId.search(artistName, client_access_token)
	print "numSongs: ",len(songs)
	for song in songs:
		print song
		songTitle = unidecode.unidecode(song[2])
		#print songTitle, artistName
		lyrics = getLyrics.getLyrics(songTitle, artistName)
		for i in range(0, 10):
			Data.append(lyrics)
	return Data

# kendrick = getData("Kendrick Lamar")
# print kendrick[0]
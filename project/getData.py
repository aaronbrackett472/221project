import getLyrics, getArtistId
import unidecode 

def getData(artistName):
	# Data = ""
	# client_access_token = "rTNAfXuSPK2GWd6eXtmZwuHVMitzHO-iAl5CKKPNiQ-m2arGCN7eqRRRy7v1F6j8"
	# songs = getArtistId.search(artistName, client_access_token)
	# print "numSongs: ",len(songs)
	# for song in songs:
	# 	print song
	# 	songTitle = unidecode.unidecode(song[2])
	# 	#print songTitle, artistName
	# 	lyrics = getLyrics.getLyrics(songTitle, artistName)
	# 	if lyrics != None:
	# 		lyrics = lyrics.encode("utf-8")
	# 		for i in range(0, 10):
	# 			# print lyrics
	# 			Data += lyrics
	f = open('corpus.txt', 'r')
	lyrics = f.read()
	Data = unicode(lyrics, "utf-8")
	return Data

# kendrick = getData("Kendrick Lamar")
# print kendrick[0]
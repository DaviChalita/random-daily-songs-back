import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
genre_list = sp.recommendation_genre_seeds()['genres']


file = open('genres.txt', 'w')
for genre_i in genre_list:
    file.write(genre_i)
    file.write("\n")
file.close()

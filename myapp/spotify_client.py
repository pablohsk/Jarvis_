import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public,user-library-modify,user-library-read,user-read-playback-state,user-modify-playback-state'))

    def search_song(self, query):
        results = self.sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return track['uri']
        else:
            return None

    def create_playlist(self, playlist_name):
        self.sp.user_playlist_create(user=self.sp.me()['id'], name=playlist_name, public=True)

    def add_song_to_playlist(self, playlist_id, song_uri):
        self.sp.playlist_add_items(playlist_id, [song_uri])

    def play_song(self, song_uri):
        self.sp.start_playback(uris=[song_uri])

    def pause_song(self):
        self.sp.pause_playback()

    def skip_song(self):
        self.sp.next_track()

    def previous_song(self):
        self.sp.previous_track()

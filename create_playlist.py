import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datamanager import GetData
import json
from tkinter import messagebox
from tkinter import *

CLIENT_ID = os.environ.get('SpotifyID')
CLIENT_KEY = os.environ.get('SpotifyKey')


class CreatePlaylist(GetData):
    def __init__(self):
        super().__init__()
        # Create an instance of the SpotifyOAuth class
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_KEY, redirect_uri='https://example.com',
                                scope='playlist-modify-public', cache_path='token.txt')
        auth_url = sp_oauth.get_authorize_url()
        print("Please visit this URL to authorize the application: " + auth_url)
        redirected_url = input("Enter the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(redirected_url)
        token_info = sp_oauth.get_access_token(code)

        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        self.user_id = self.sp.current_user()['id']
        self.uri = []
        self.nouri = []

    def get_uri(self):
        """Gets the uri of songs """
        for song in self.song_list:
            uri = self.sp.search(q=f'track:{song}', type='track')
            try:
                uri_result = uri["tracks"]["items"][0]["uri"]
                self.uri.append(uri_result)
            except IndexError:
                messagebox.showinfo('Song Error', f'{song} does not exist in spotify')



    def create_playlist(self, plist_name, description):
        """Creates a spotify Playlist"""
        playlist_name = plist_name
        descript = description
        playlist_id = self.sp.user_playlist_create(user=self.user_id, name=playlist_name, public=True,
                                                   description=descript)
        try:
            with open('playlistID.json', mode='r') as file:
                data = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[playlist_name] = playlist_id

        with open('playlistID.json', mode='w') as file:
            json.dump(data, file)

    def add_song(self, pid):
        self.sp.playlist_add_items(playlist_id=pid, items=self.uri)

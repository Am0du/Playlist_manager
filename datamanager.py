import requests
from bs4 import BeautifulSoup
from tkinter import messagebox


class GetData:
    def __init__(self):
        self.year = ''
        self.song_list = []

    def song_title(self, y):
        """Scrapes billboard for hits 100"""
        try:
            response = requests.get(f'https://www.billboard.com/charts/hot-100/{y}')
        except requests.exceptions.HTTPError:
            messagebox.showerror('Error', 'You Entered a wrong Date format')
        else:
            top_songs = response.text
            soup = BeautifulSoup(top_songs, 'html.parser')

            songs = soup.select('li ul li h3')
            # artists = soup.select('li ul li span')
            # raw_artist_list = [artist.text.strip() for artist in artists]
            # artist_list = raw_artist_list[0:len(raw_artist_list):7]
            self.song_list = [songs[i].text.strip() for i in range(len(songs) - 1)]
            self.year = y[:4]

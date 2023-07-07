import json

from create_playlist import CreatePlaylist
from datamanager import GetData
from tkinter import *
from tkinter import messagebox


class Ui(CreatePlaylist, GetData):
    def __init__(self):
        super().__init__()
        self.plist_id = ''
        self.window = Tk()
        self.window.title('Playlist Manager')
        self.window.geometry("400x400")
        self.bg_img = PhotoImage(file='bg.png')
        self.window.config(padx=100, pady=50)
        self.startup()

        self.window.mainloop()

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def quit(self):
        quit_m = messagebox.askyesno('Quit', 'Do you want to quit the manager')
        if quit_m:
            self.window.destroy()

    def startup(self):
        """The Startup widget"""
        self.clear()

        canvas = Canvas(width=200, height=200, highlightthickness=0)
        canvas.create_image(100, 100, image=self.bg_img)
        canvas.grid(row=0, column=0, columnspan=2, pady=20)

        playlist_button = Button(text='Create playlist', highlightthickness=0, command=self.create_plist)
        playlist_button.grid(row=1, column=0)

        add_button = Button(text='Add Song', highlightthickness=0, command=self.song)
        add_button.grid(row=1, column=1, )

    def song(self):
        """Add song widget"""
        def get_song():
            plist_name = playlist_entry.get().title()
            song = song_entry.get()
            self.song_list.append(song)
            self.get_uri()
            with open("playlistID.json") as file:
                data = json.load(file)
            try:
                playlist_id = data[plist_name]['id']
            except KeyError:
                messagebox.showerror('Playlist Name', f'{plist_name} does not exist')
            else:
                self.add_song(pid=playlist_id)
                messagebox.showinfo('Song added', f'{song} has been added')
                self.quit()

        self.clear()
        self.window.config(padx=70, pady=50)
        playlist_label = Label(text='Name of Playlist:')
        playlist_entry = Entry()
        playlist_label.grid(row=0, column=0, sticky='w', pady=20)
        playlist_entry.grid(row=0, column=1, columnspan=3)

        song_label = Label(text='Name of song:')
        song_entry = Entry()
        song_label.grid(row=1, column=0, sticky='w', pady=20)
        song_entry.grid(row=1, column=1, columnspan=3)

        back_button = Button(text='Back', command=self.startup)
        back_button.grid(row=2, column=0)
        button = Button(text='Submit', command=get_song)
        button.grid(row=2, column=1)

        canvas = Canvas(width=200, height=200, highlightthickness=0)
        canvas.create_image(100, 100, image=self.bg_img)
        canvas.grid(row=3, column=0, columnspan=2, pady=20)

    def create_plist(self):
        """Create playlist button"""

        def create():

            plist_name = playlist_entry.get().title()
            self.plist_id = plist_name
            plist_des = description_entry.get().title()

            if plist_des == '' or plist_name == '':
                messagebox.showerror('Error', 'playlist name or description cannot be empty')
            else:
                self.create_playlist(plist_name=plist_name, description=plist_des)
                add = messagebox.askyesno(f'{plist_name} created successfully',
                                          'Do you want to hit songs from billboard ?')
                if add:
                    self.add_billboard()

        self.clear()
        self.window.config(padx=70, pady=50)
        playlist_label = Label(text='Name of Playlist:')
        playlist_entry = Entry()
        playlist_label.grid(row=0, column=0, sticky='w', pady=20)
        playlist_entry.grid(row=0, column=1, columnspan=3)

        description_label = Label(text='Description:')
        description_entry = Entry()
        description_label.grid(row=1, column=0, sticky='w', pady=20)
        description_entry.grid(row=1, column=1, columnspan=3)

        back_button = Button(text='Back', command=self.startup)
        back_button.grid(row=2, column=1)

        create_button = Button(text='Create', command=create)
        create_button.grid(row=2, column=0)

        canvas = Canvas(width=200, height=200, highlightthickness=0)
        canvas.create_image(100, 100, image=self.bg_img)
        canvas.grid(row=3, column=0, columnspan=2, pady=20)

    def add_billboard(self):
        def song():
            date = year_entry.get()
            with open('playlistID.json') as file:
                data = json.load(file)

            plid = data[self.plist_id]['id']

            self.song_title(y=date)
            self.get_uri()
            self.add_song(pid=plid)
            messagebox.showinfo('songs added', 'Enjoy your playlist')
            self.quit()
            # except:
            #     messagebox.showerror('Error', 'Error while adding songs')

        self.clear()
        self.window.config(padx=50, pady=50)
        year_label = Label(text='Date of Hit (YYYY-MM-DD):')
        year_entry = Entry()
        year_label.grid(row=0, column=0, sticky='w', pady=20)
        year_entry.grid(row=0, column=1, columnspan=3)

        back_button = Button(text='back', command=self.startup)
        back_button.grid(row=1, column=0)
        button = Button(text='Add', command=song)
        button.grid(row=1, column=1)
        canvas = Canvas(width=200, height=200, highlightthickness=0)
        canvas.create_image(100, 100, image=self.bg_img)
        canvas.grid(row=2, column=0, columnspan=2, pady=20)

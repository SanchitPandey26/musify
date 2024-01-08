import os
import tkinter as tk

import eyed3
import mysql
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import LEFT, ttk, filedialog, END, ACTIVE
from mysql import connector
from libs.constants import AppName, appFont, blackColor, blueColor

stop_play_pause = "stop"
song_len = 0
play_time = 0


def licenses(windows, appVersrion=None):
    width = 500
    height = 480
    win = tk.Toplevel()
    win.wm_title(AppName + " - License Info")
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    win.focus_set()
    main_icon = tk.PhotoImage(file="images/musify.png")
    win.iconphoto(False, main_icon)
    info_frame = tk.Frame(win, height=60, width=390)
    info_frame.place(x=45, y=5)
    name_lbl = tk.Label(info_frame, text=AppName + ' - Music Player', font=(appFont, 13))
    name_lbl.place(x=105, y=5)
    version_lbl = tk.Label(info_frame, text=appVersrion)
    version_lbl.place(x=160, y=30)

    line = tk.Frame(win, height=1, width=397, highlightthickness=1, highlightbackground='black')
    line.place(x=40, y=80)

    mit_lbl = tk.Label(win, text='MIT License')
    mit_lbl.place(x=208, y=100)
    copyryt_lbl = tk.Label(win, text='Copyright (c) 2022 Sanchit Pandey')
    copyryt_lbl.place(x=150, y=115)

    bottom_frame = tk.Frame(win, height=290, width=420)
    bottom_frame.place(x=45, y=145)
    license_text_lbl = tk.Label(bottom_frame,
                                text='Permission is hereby granted, free of charge, to any person obtaining a copy\n'
                                     'of this software and associated documentation files (the "Software"), to deal\n'
                                     'in the Software without restriction, including without limitation the rights to\n'
                                     'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies\n'
                                     'of the Software, and to permit persons to whom the Software is furnished to \n'
                                     'do so, subject to the following conditions:\n\n'
                                     'The above copyright notice and this permission  notice shall be included in\n'
                                     'all copies or substantial portions of the Software.\n\n'
                                     'THE  SOFTWARE  IS  PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\n'
                                     'EXPRESS  OR  IMPLIED, INCLUDING  BUT NOT LIMITED TO THE WARRANTIES \n'
                                     'OF MERCHANTABILITY, FITNESS  FOR  A  PARTICULAR PURPOSE AND NON-\n'
                                     'INFRINGEMENT.IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLD-\n'
                                     'ERS BE  LIABLE  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\n'
                                     'IN AN ACTION  OF CONTRACT, TORT  OR OTHERWISE, ARISING FROM, OUT\n'
                                     'OF  OR  IN  CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR OTHER\n'
                                     'DEALINGS IN THE SOFTWARE.', justify=LEFT)
    license_text_lbl.place(x=0, y=0)

    close_button = ttk.Button(win, text="Close", command=win.destroy)
    close_button.place(x=205, y=435)


def about(windows):
    width = 500
    height = 500
    win = tk.Toplevel()
    win.wm_title(AppName + " - About")
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    win.focus_set()
    main_icon = tk.PhotoImage(file="images/musify.png")
    win.iconphoto(False, main_icon)

    info_frame = tk.Frame(win, height=165, width=390)
    info_frame.place(x=45, y=15)
    name_lbl = tk.Label(info_frame, text=AppName + ' - Music Player', font=(appFont, 13))
    name_lbl.place(x=105, y=5)
    version_lbl = tk.Label(info_frame, text='Version 1.0.0')
    version_lbl.place(x=160, y=30)
    line = tk.Frame(win, height=1, width=397, highlightthickness=1, highlightbackground=blackColor)
    line.place(x=49, y=80)

    about_frame = tk.Frame(win, height=230, width=420)
    about_frame.place(x=45, y=100)
    about_lbl = tk.Label(about_frame,
                         text='Musify is a Stylish, Powerful and  Fast Music Player  with  elegant design. \n'
                              'It lets you manage all your music files and folder quickly and easily. \n\n'
                              'This audio  player  supports  almost all types of music files such as mp3, aac, \n'
                              'wav and m4a audio formats. Easily browse and play music songs by albums, \n'
                              'artists , songs and folder.', justify=LEFT)
    about_lbl.place(x=0, y=0)

    features_lbl = tk.Label(about_frame, text='Currently Musify fully Supports (Features): \n\n' \
                                              '    - A simple, flat and material UI design\n' \
                                              '    - Audio file formats such as MP3, WAV, M4A and AAC\n' \
                                              '    - Volume Slider and ProgressBar works fine\n' \
                                              '    - Add Songs via Folder or you can select single audio files\n' \
                                              '    - Remove songs, (current or all songs)', justify=LEFT)
    features_lbl.place(x=0, y=100)

    line1 = tk.Frame(win, height=1, width=397, highlightthickness=1, highlightbackground='black')
    line1.place(x=49, y=340)

    footer_frame = tk.Frame(win, height=60, width=420)
    footer_frame.place(x=45, y=360)
    footer_lbl = tk.Label(footer_frame,
                          text='Musify player is a Music  Player  for  Windows. Send  me  the feedbacks,\n'
                               'bug-reports and suggestions about MusicByte to:', justify=LEFT)
    footer_lbl.place(x=0, y=0)
    email_lbl = tk.Label(footer_frame, text='sanchitpandey263@gmail.com', fg=blueColor, cursor="hand2")
    email_lbl.place(x=110, y=35)

    close_button = ttk.Button(win, text="Close", command=win.destroy)
    close_button.place(x=210, y=440)


def add_lib_folder(scroll, music_list):
    songs_dir = filedialog.askdirectory()
    try:
        songs = os.listdir(songs_dir)
    except FileNotFoundError:
        return

    music_list.config(yscrollcommand=scroll.set)
    scroll.config(command=music_list.yview)
    for song_name in songs:
        music_list.config(font=(appFont, 10))
        song = os.path.join(songs_dir, song_name)
        music_list.insert(END, f'  {song}')
    music_list.config(height=25, width=75)


def add_song(scroll, music_list):
    song_file_name = filedialog \
        .askopenfilenames(title="Select File",
                          filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
    if song_file_name == "":
        return

    music_list.config(yscrollcommand=scroll.set)
    scroll.config(command=music_list.yview)
    for song in song_file_name:
        music_list.config(font=('Helvetica bold', 10))
        music_list.insert(END, f'  {song}')
    music_list.config(height=25, width=75)


def remove_song(music_list):
    current_song = music_list.curselection()
    if current_song:
        music_list.delete(current_song)
        music_list.selection_set(current_song, last=None)


def remove_all(music_list):
    music_list.delete(0, END)


def play(music_list, play_btn, play_icon, pause_icon, artist_lbl):
    global stop_play_pause, song_len, play_time
    if stop_play_pause == "stop":
        selected = music_list.curselection()
        if len(selected) == 0:
            music_list.selection_clear(0, END)
            music_list.activate(0)
            music_list.selection_set(0, last=None)
        song = music_list.get(ACTIVE)
        song = song.replace('\\', '/')
        song = song.replace(' ', '')
        try:
            mixer.music.load(song)
            mixer.music.play()
            play_btn.config(image=pause_icon)
            stop_play_pause = "play"
            song_load = MP3(song)
            song_len = song_load.info.length
            play_time = 0
            song_info(song, artist_lbl)
        except:
            return
    elif stop_play_pause == "pause":
        mixer.music.unpause()
        play_btn.config(image=pause_icon)
        stop_play_pause = "play"
    else:
        mixer.music.pause()
        play_btn.config(image=play_icon)
        stop_play_pause = "pause"


def stop(play_btn, play_icon, artist_lbl):
    global stop_play_pause, song_len, play_time
    mixer.music.stop()
    stop_play_pause = "stop"
    play_btn.config(image=play_icon)
    song_len = 0
    play_time = 0
    song_info(None, artist_lbl)


def play_next(music_list, play_btn, pause_icon, artist_lbl):
    global stop_play_pause, song_len, play_time
    next_song = music_list.curselection()
    try:
        next_song = next_song[0] + 1
    except:
        next_song = 0
    song = music_list.get(next_song)
    song = song.replace('\\', '/')
    song = song.replace(' ', '')
    try:
        mixer.music.load(song)
        mixer.music.play()
        play_btn.config(image=pause_icon)
        stop_play_pause = "play"
        song_load = MP3(song)
        song_len = song_load.info.length
        play_time = 0
        song_info(song, artist_lbl)
    except:
        pass
    try:
        music_list.selection_clear(0, END)
        music_list.activate(next_song)
        music_list.selection_set(next_song, last=None)
    except:
        pass


def play_previous(music_list, play_btn, pause_icon, artist_lbl):
    global stop_play_pause, song_len, play_time
    prev_song = music_list.curselection()
    try:
        prev_song = prev_song[0] - 1
    except:
        prev_song = music_list.size() - 1
    song = music_list.get(prev_song)
    song = song.replace('\\', '/')
    song = song.replace(' ', '')
    try:
        mixer.music.load(song)
        mixer.music.play()
        play_btn.config(image=pause_icon)
        stop_play_pause = "play"
        song_load = MP3(song)
        song_len = song_load.info.length
        play_time = 0
        song_info(song, artist_lbl)
    except:
        pass
    try:
        music_list.selection_clear(0, END)
        music_list.activate(prev_song)
        music_list.selection_set(prev_song, last=None)
    except:
        pass


def play_forward():
    global stop_play_pause, song_len, play_time
    if stop_play_pause == "play" and (play_time + 10 < song_len):
        if play_time == 0:
            current_song_pos = mixer.music.get_pos() / 1000
            play_time = current_song_pos + 10
        else:
            play_time = play_time + 10
        mixer.music.rewind()
        mixer.music.set_pos(play_time)


def play_rewind():
    global stop_play_pause, song_len, play_time
    if stop_play_pause == "play":
        if play_time == 0:
            current_song_pos = mixer.music.get_pos() / 1000
            if (current_song_pos - 10) > 0:
                play_time = current_song_pos - 10
            else:
                play_time = 1
        else:
            if (play_time - 10) < 0:
                play_time = 1
            else:
                play_time = play_time - 10
        mixer.music.rewind()
        mixer.music.set_pos(play_time)


def song_info(song, artist_lbl):
    if song is None:
        artist_lbl.config(text='')
    else:
        audio_f = eyed3.load(song)
        lbl = audio_f.tag.title + "(" + audio_f.tag.album_artist + ")"
        if lbl == "":
            artist_lbl.config(text="UnKnown Artist")
        else:
            artist_lbl.config(text=lbl)


def verify_login(user, password):
    db = mysql.connector.connect(host="localhost", user="root", passwd="Sanchit", database="musify")
    mycur = db.cursor()
    sql1 = "select * from users where name = %s"
    sql2 = "select * from users where name = %s and password = %s"
    mycur.execute(sql1, [user])
    results1 = mycur.fetchall()
    if results1:
        mycur.execute(sql2, [user, password])
        results2 = mycur.fetchall()
        if results2:
            return "Pass"
        else:
            return "Fail"
    else:
        return "Invalid"


def sign_up(user, password):
    db = mysql.connector.connect(host="localhost", user="root", passwd="Sanchit", database="musify")
    mycur = db.cursor()
    sql = "insert into users values(%s,%s)"
    mycur.execute(sql, [user, password])
    db.commit()

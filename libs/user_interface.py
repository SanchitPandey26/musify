import tkinter as tk
from tkinter import GROOVE, BOTTOM, HORIZONTAL, ttk, E, X

from pygame import mixer

from libs.constants import appFont, blueColor, fgColor, grayColor, bgColor, blackColor
from libs.functions import about, licenses, add_lib_folder, add_song, remove_song, remove_all, play, stop, play_next, \
    play_previous, play_forward, play_rewind

vol_percent_lbl = None
volume_slider = None
mute = False


def now_playing_panel(frame):
    now_playing_header_frame = tk.Frame(frame, height=30, width=200, bg=blueColor)
    now_playing_header_frame.place(x=25, y=360)
    now_playing_header_label = tk.Label(now_playing_header_frame, text="Now Playing...", bg=blueColor, fg=fgColor,
                                        font=(appFont, 13))
    now_playing_header_label.place(x=50, y=0)
    now_playing_img_frame = tk.Frame(frame, height=200, width=200, bg=grayColor)
    now_playing_img_label = tk.Label(now_playing_img_frame, height=200, width=200, bg=grayColor, borderwidth=0)
    now_playing_img_frame.place(x=25, y=390)
    now_playing_img_label.place(x=0, y=0)
    return now_playing_img_label


def help_menu(frame, windows):
    help_text = tk.Label(frame, text="HELP", font=(appFont, 13), borderwidth=0, bg=bgColor, fg=fgColor)
    help_text.place(x=30, y=190)
    about_btn = tk.Button(frame, text="About", font=(appFont, 13), borderwidth=0,
                          fg=fgColor, bg=bgColor, command=lambda: about(windows))
    about_btn.place(x=55, y=220)
    license_btn = tk.Button(frame, text="License", font=(appFont, 13), borderwidth=0,
                            fg=fgColor, bg=bgColor, command=lambda: licenses(windows))
    license_btn.place(x=55, y=250)


def music_menu(frame, scroll, music_list):
    music_text = tk.Label(frame, text="MUSIC", font=(appFont, 13), borderwidth=0, bg="gray", fg=fgColor)
    music_text.place(x=30, y=30)
    add_library_btn = tk.Button(frame, text="Add Library", font=(appFont, 13), borderwidth=0, fg=fgColor,
                                bg=bgColor, command=lambda: add_lib_folder(scroll, music_list))
    add_library_btn.place(x=55, y=60)
    add_songs_btn = tk.Button(frame, text="Add Song", font=(appFont, 13), borderwidth=0, fg=fgColor,
                              bg=bgColor, command=lambda: add_song(scroll, music_list))
    add_songs_btn.place(x=55, y=90)
    remove_songs_btn = tk.Button(frame, text="Remove Song", font=(appFont, 13), borderwidth=0, fg=fgColor,
                                 bg=bgColor, command=lambda: remove_song(music_list))
    remove_songs_btn.place(x=55, y=120)
    remove_all_songs_btn = tk.Button(frame, text="Remove All", font=(appFont, 13), borderwidth=0,
                                     fg=fgColor, bg=bgColor, command=lambda: remove_all(music_list))
    remove_all_songs_btn.place(x=55, y=150)


def heading_logo(frame, logo_img):
    logo_panel = tk.Frame(frame, height=50, width=137)
    logo_panel.place(x=35, y=15)
    logo_lbl = tk.Label(logo_panel, height=50, width=137, image=logo_img, borderwidth=0)
    logo_lbl.place(x=0, y=0)


def left_panel(root, image):
    left_content_frame = tk.Frame(root, height=620, width=250)
    left_content_frame.place(x=0, y=0)
    left_content_label = tk.Label(left_content_frame, height=620, width=250, image=image, borderwidth=0)
    left_content_label.place(x=0, y=0)
    return left_content_frame


def details_panel(frame):
    details_frame = tk.Frame(frame, height=70, width=200, bg=grayColor)
    details_frame.place(x=23, y=245)
    artist_lbl = tk.Label(details_frame, text='Artist: ', bg=grayColor)
    artist_lbl.place(x=0, y=5)
    length_lbl = tk.Label(details_frame, text='Length: ', bg=grayColor)
    length_lbl.place(x=0, y=25)
    bit_rate_lbl = tk.Label(details_frame, text='Bit rate: ', bg=grayColor)
    bit_rate_lbl.place(x=0, y=45)


def coming_up(frame):
    coming_next_frame = tk.Frame(frame, height=30, width=200, bg=blueColor)
    coming_next_frame.place(x=23, y=10)
    coming_next_lbl = tk.Label(coming_next_frame, text='Coming Up Next...', fg=fgColor, bg=blueColor,
                               font=(appFont, 13))
    coming_next_lbl.place(x=25, y=0)
    coming_next_img_frame = tk.Frame(frame, height=200, width=200, bg=grayColor)
    coming_next_img_label = tk.Label(coming_next_img_frame, height=200, width=200, bg=grayColor, borderwidth=0)
    coming_next_img_frame.place(x=23, y=40)
    coming_next_img_label.place(x=0, y=0)
    return coming_next_img_label


def right_panel(root, image):
    right_content_frame = tk.Frame(root, height=620, width=250)
    right_content_frame.place(x=810, y=0)
    right_content_label = tk.Label(right_content_frame, height=620, width=250, image=image, borderwidth=0)
    right_content_label.place(x=0, y=0)
    return right_content_frame


def music_list(root):
    musicbox_frame = tk.Frame(root, height=500, width=560)
    musicbox_frame.place(x=254, y=20)
    music_lists = tk.Listbox(musicbox_frame, height=25, width=85, borderwidth=0, bg='#f0f0f0')
    music_lists.pack(side='left', fill='y')
    scroll = tk.Scrollbar(musicbox_frame, orient='vertical')
    scroll.pack(side='right', fill='y')
    return scroll, music_lists


def music_time(frame):
    slider_end_frame = tk.Frame(frame, height=21, width=35)
    slider_end_frame.place(x=500, y=5)
    slider_end_lbl = tk.Label(slider_end_frame, text='00:00')
    slider_end_lbl.place(x=0, y=0)

    slider_start_frame = tk.Frame(frame, height=21, width=40)
    slider_start_frame.place(x=20, y=7)
    slider_start_lbl = tk.Label(slider_start_frame, text="00:00", relief=GROOVE, anchor=E, borderwidth=0)
    slider_start_lbl.pack(fill=X, side=BOTTOM)

    # SLIDER FRAME
    slider_frame = tk.Frame(frame, height=21, width=350)
    slider_frame.place(x=58, y=4)
    slider_progress_bar = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=432)
    slider_progress_bar.pack()


def music_buttons(frame, play_icon, stop_icon, forward_icon,
                  rewind_icon, next_icon, previous_icon, pause_icon,
                  music_lists, artist_lbl):
    play_btn = tk.Button(frame, image=play_icon, borderwidth=0)
    stop_btn = tk.Button(frame, image=stop_icon, borderwidth=0)
    forward_btn = tk.Button(frame, image=forward_icon, borderwidth=0)
    next_btn = tk.Button(frame, image=next_icon, borderwidth=0)
    previous_button = tk.Button(frame, image=previous_icon, borderwidth=0)
    rewind_button = tk.Button(frame, image=rewind_icon, borderwidth=0)
    previous_button.place(x=23, y=11)
    rewind_button.place(x=62, y=11)
    play_btn.place(x=100, y=6)
    stop_btn.place(x=150, y=8)
    forward_btn.place(x=195, y=12)
    next_btn.place(x=233, y=11)
    play_btn.config(command=lambda: play(music_lists, play_btn, play_icon, pause_icon, artist_lbl))
    stop_btn.config(command=lambda: stop(play_btn, play_icon, artist_lbl))
    next_btn.config(command=lambda: play_next(music_lists, play_btn, pause_icon, artist_lbl))
    previous_button.config(command=lambda: play_previous(music_lists, play_btn, pause_icon, artist_lbl, ))
    forward_btn.config(command=lambda: play_forward())
    rewind_button.config(command=lambda: play_rewind())


def volume_control(vol_frame, volume_icon, mute_icon):
    global vol_percent_lbl, volume_slider
    mute_button = tk.Button(vol_frame, image=volume_icon, borderwidth=0)
    mute_button.config(command=lambda: mute_volume(mute_button, volume_icon, mute_icon))
    mute_button.place(x=40, y=0)
    vol_percent_frame = tk.Frame(vol_frame, height=20, width=100)
    vol_percent_frame.place(x=70, y=3)
    vol_lbl = tk.Label(vol_percent_frame, text='Volume:', fg=blackColor)
    vol_lbl.place(x=0, y=0)
    vol_percent_lbl = tk.Label(vol_percent_frame, text='50%', fg=blackColor)
    vol_percent_lbl.place(x=50, y=1)
    vol_slider_frame = tk.Frame(vol_frame, height=21, width=150, bg=grayColor)
    vol_slider_frame.place(x=170, y=3)
    volume_slider = ttk.Scale(vol_slider_frame, from_=0, to=100, orient=HORIZONTAL, value=50, length=100,
                              command=set_volume)
    volume_slider.pack()
    return vol_percent_lbl


def set_volume(percent):
    global vol_percent_lbl
    vol = float(percent) / 100
    mixer.music.set_volume(vol)
    vol_percent_lbl.config(text=str(int(float(percent))) + '%')


def mute_volume(mute_button, volume_icon, mute_icon):
    global mute, volume_slider
    if mute:
        mute = False
        mixer.music.set_volume(volume_slider.get())
        mute_button.config(image=volume_icon)
    else:
        mute = True
        mixer.music.set_volume(0)
        mute_button.config(image=mute_icon)

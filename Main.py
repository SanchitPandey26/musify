from tkinter import Toplevel, Label, StringVar, Entry, Button, messagebox

from easygui import multpasswordbox

from libs.constants import *
from libs.functions import sign_up, verify_login
from libs.user_interface import *


if __name__ == "__main__":
    # Login or SignUp
    msg = "Login existing user or SignUp new user"
    title = "Musify"
    fieldNames = ["user", "password"]
    fieldValues = []

    while 1:
        fieldValues = multpasswordbox(msg, title, fieldNames)
        if fieldValues is None:
            exit()
        elif fieldValues[0] == "":
            messagebox.showerror(title="Error", message="Please enter login name")
        elif fieldValues[1] == "":
            messagebox.showerror(message="Please enter password")
        else:
            login = verify_login(fieldValues[0], fieldValues[1])
            if login == "Pass":
                break
            elif login == "Fail":
                messagebox.showerror(message="Invalid Password")
            elif messagebox.askyesno(message="Login does not exist. Do you want to SignUp?"):
                sign_up(fieldValues[0], fieldValues[1])
                break
            else:
                exit()

    # Create main window
    windows = tk.Tk()
    windows.title(AppName)

    # Set window width and height
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    windows.geometry("{}x{}+{}+{}".format(width, height, x, y))
    windows.resizable(False, False)

    # Set main window icon
    main_icon = tk.PhotoImage(file="images/musify.png")
    windows.iconphoto(False, main_icon)

    # Create the root frame
    root = tk.Frame(windows, height=height, width=width)
    root.pack()

    # Create the right panel
    right_content_img = tk.PhotoImage(file="images/right-panel.png")
    right_content_frame = right_panel(root, right_content_img)

    # Create Music List box
    scroll, music_lists = music_list(root)

    # Create the left panel
    left_content_img = tk.PhotoImage(file="images/left-panel.png")
    left_content_frame = left_panel(root, left_content_img)
    logo_img = tk.PhotoImage(file="images/musify-logo.png")
    heading_logo(left_content_frame, logo_img)

    # Menu Items
    menu_panel = tk.Frame(left_content_frame, height=280, width=210, bg=bgColor)
    menu_panel.place(x=10, y=70)
    music_menu(menu_panel, scroll, music_lists)
    help_menu(menu_panel, windows)

    # Create Song Info
    info_frame = tk.Frame(root, height=30, width=540)
    info_frame.place(x=260, y=460)
    artist_lbl = tk.Label(info_frame, text=' ')
    artist_lbl.place(x=0, y=0)

    # Create play time control
    control_frame = tk.Frame(root, height=100, width=560)
    control_frame.place(x=250, y=510)

    # Create Music button control
    button_control_frame = tk.Frame(control_frame, height=48, width=300)
    button_control_frame.place(x=120, y=0)
    play_icon = tk.PhotoImage(file="images/play-button.png")
    stop_icon = tk.PhotoImage(file="images/stop.png")
    forward_icon = tk.PhotoImage(file="images/forward.png")
    rewind_icon = tk.PhotoImage(file="images/rewind.png")
    next_icon = tk.PhotoImage(file="images/next.png")
    previous_icon = tk.PhotoImage(file="images/previous.png")
    pause_icon = tk.PhotoImage(file="images/pause.png")
    music_buttons(button_control_frame, play_icon, stop_icon, forward_icon,
                  rewind_icon, next_icon, previous_icon, pause_icon, music_lists,
                  artist_lbl)

    # Create Volume control
    vol_frame = tk.Frame(control_frame, height=30, width=300)
    vol_frame.place(x=110, y=55)
    volume_icon = tk.PhotoImage(file="images/volume.png")
    mute_icon = tk.PhotoImage(file="images/mute.png")
    vol_percent_lbl = volume_control(vol_frame, volume_icon, mute_icon)

    mixer.init()
    mixer.music.set_volume(0.5)
    windows.focus_force()
    windows.mainloop()

import tkinter
from tkinter import Tk, Entry, Canvas
from final import country_info
import PIL
from PIL import ImageTk, Image
import requests
from io import BytesIO
import threading
from time import sleep
import sys


# Constants for flag display
FLAG_SCALE = 0.1
FLAG_OFFSET = (30, 15)

x = 0
y = 0
flag = None
flag_url = "https://flagpedia.net/data/flags/normal/tg.png"     # default value for flag to begin with
flag_image = None
flag_update = True   # boolean flag for whether to update the flag

def motion(event):
    global x, y, flag_url
    x, y = event.x, event.y
    lon = (x - 184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90

    country, facts, trends, flag_url = country_info.get_info(lat, lon)

    # print(lat, lon)
    # print(country, facts, trends, flag_url)


def right_click(event):
    # draw a pin at the clicked location
    image_canvas.create_image(event.x, event.y, image=pin)
    # prompt for user entry to add text associated with the pin


def update():
    while flag_update:
        # find flag image from url
        global flag, flag_url, flag_image
        response = requests.get(flag_url)
        img_data = response.content

        try:
            # get image size + resize
            width, height = Image.open(BytesIO(img_data)).size
            flag_image = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((int(width*FLAG_SCALE), int(height*FLAG_SCALE)), Image.ANTIALIAS))
        except PIL.UnidentifiedImageError:
            # hard-coded resize; no_flag is 550x275px.
            flag_image = ImageTk.PhotoImage(Image.open("../images/no_flag.png").resize((int(550*FLAG_SCALE), int(275*FLAG_SCALE))))

        # redraw flag
        image_canvas.delete(flag)
        flag = image_canvas.create_image(x+FLAG_OFFSET[0], y+FLAG_OFFSET[1], anchor=tkinter.NW, image=flag_image)

        print(flag_update)
        sleep(0.01)
    return


def on_closing():
    global flag_update
    flag_update = False
    sys.exit()


root = Tk()
root.geometry("1186x609")

# set up canvas
image_canvas = Canvas(root, bg="blue", width=1186, height=609)
image_canvas.place(relx=0, rely=0)

# load up initial images
world_map = ImageTk.PhotoImage(Image.open("../images/world_map.png"))
pin = ImageTk.PhotoImage(Image.open("../images/pin.png").resize((20, 30)))

# draw map
image_canvas.create_image(593, 304, image=world_map)

# bind actions
root.bind('<Motion>', motion)
root.bind("<Button-2>", right_click)

# multithreading on flag loading
threads = []
a = threading.Thread(target=update)
threads.append(a)
a.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


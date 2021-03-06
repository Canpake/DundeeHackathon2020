import tkinter
from tkinter import Tk, Frame, Canvas, PhotoImage
from final import country_info
from PIL import ImageTk, Image
import requests
from io import BytesIO
import threading
from time import sleep

x = 0
y = 0
flag = None
flag_url = "https://flagpedia.net/data/flags/normal/tg.png"
flag_canvas = None
pin_locations = []


def motion(event):
    global x, y, flag_url
    x, y = event.x, event.y
    lon = (x - 184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90

    country, facts, trends, flag_url = country_info.get_info(lat, lon)

    # print(lat, lon)
    # print(country, facts, trends, flag_url)


def right_click(event):
    print("right click")
    image_canvas.create_image(event.x, event.y, anchor=tkinter.NW, image=pin)


def update():
    while True:
        # set flag url
        global flag_url
        response = requests.get(flag_url)
        img_data = response.content

        # find flag image (and resize)
        global flag
        try:
            current = ImageTk.PhotoImage(
                Image.open(BytesIO(img_data)).resize((int(550 / 10), int(367 / 10)), Image.ANTIALIAS))
        except:
            continue
        flag = current

        # redraw map + flag + pins

        global flag_canvas
        image_canvas.delete(flag_canvas)
        flag_canvas = image_canvas.create_image(x + 30, y + 15, anchor=tkinter.NW, image=flag)
        # draw each pin

        sleep(0.01)


root = Tk()
root.geometry("1186x609")

# set up canvas + load initial images
image_canvas = Canvas(root, bg="blue", width=1186, height=609)
image_canvas.place(relx=0, rely=0)
world_map = ImageTk.PhotoImage(Image.open("../images/world_map.png"))
pin = ImageTk.PhotoImage(Image.open("../images/pin.png").resize((20, 30)))

image_canvas.create_image(593, 304, image=world_map)

# bind actions
root.bind('<Motion>', motion)
root.bind("<Button-2>", right_click)

# multithreading on flag loading
threads = []
a = threading.Thread(target=flag_update)
threads.append(a)
a.start()

root.mainloop()


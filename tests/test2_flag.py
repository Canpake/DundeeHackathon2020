# move an Image on the canvas with tkinter
 
import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
from final import country_info
import threading
from time import sleep
 
# Create the window with the Tk class
root = tk.Tk()
root.geometry("1200x519")
 
# Create the canvas and make it visible with pack()
canvas = tk.Canvas(root, width=1200, height=750)
canvas.place(relx=0, rely=0)
canvas.pack() # this makes it visible

# define a flag variable
flag = None
# Loads and create image (put the image in the folder)
img = tk.PhotoImage(file="../images/world_map.png")
image = canvas.create_image(0, 0, anchor=tk.NW, image=img)

flag_url = "https://flagpedia.net/data/flags/normal/tg.png"
x = 0
y = 0


def update():
    while True:
        global flag_url
        response = requests.get(flag_url)
        img_data = response.content
        global flag
        try:
            current = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((int(550/10), int(367/10)), Image.ANTIALIAS))
        except:
            continue
        flag = current
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.create_image(x, y, anchor=tk.NW, image=flag)
        sleep(0.01)

def motion(event):
    global x, y, flag_url
    x, y = event.x, event.y
    lon = (x - 184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90

    print(lat, lon)

    country, facts, trends, flag_url = country_info.get_info(lat, lon)
    print(country, facts, trends, flag_url)



 
# This bind window to keys so that move is called when you press a key

root.bind('<Motion>', motion)

threads = []
a = threading.Thread(target=flag_update)
threads.append(a)
a.start()
# this creates the loop that makes the window stay 'active'
root.mainloop()
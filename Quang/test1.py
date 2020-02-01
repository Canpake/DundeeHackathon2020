# move an Image on the canvas with tkinter
 
import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
from final import country_info

 
# Create the window with the Tk class
root = tk.Tk()
root.geometry("1200x519")
 
# Create the canvas and make it visible with pack()
canvas = tk.Canvas(root, width=1200, height=750)
canvas.place(relx=0, rely=0)
canvas.pack() # this makes it visible


flag = ""
# Loads and create image (put the image in the folder)
img = tk.PhotoImage(file="../images/world_map.png")
image = canvas.create_image(0, 0, anchor=tk.NW, image=img)
canvas.create_image(0, 0, anchor=tk.NW, image=flag)

def motion(event):
    x, y = event.x, event.y
    lon = (x - 137) * 344 / 977 - 166
    lat = -(y) * 137 / 490 + 88
    print(lat, lon)
    canvas.delete("all")

    country, facts, trends, flag_url = country_info.get_info(lat, lon)
    print(country, facts, trends, flag_url)

    response = requests.get(flag_url)
    img_data = response.content
    global flag
    flag = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    canvas.create_image(0,0,anchor=tk.NW, image=img)
    canvas.create_image(x,y,anchor=tk.NW, image=flag)

 
# This bind window to keys so that move is called when you press a key

root.bind('<Motion>', motion)
 
# this creates the loop that makes the window stay 'active'
root.mainloop()
# move an Image on the canvas with tkinter
 
import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO

 
# Create the window with the Tk class
root = tk.Tk()
root.geometry("1200x519")
 
# Create the canvas and make it visible with pack()
canvas = tk.Canvas(root, width=1200, height=750)
canvas.place(relx=0, rely=0)
canvas.pack() # this makes it visible
 
# Loads and create image (put the image in the folder)
img = tk.PhotoImage(file="world_map.png")
img_url = "https://cdn.britannica.com/33/4833-004-297297B9/Flag-United-States-of-America.jpg"
response = requests.get(img_url)
img_data = response.content
flag = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
image = canvas.create_image(0, 0, anchor=tk.NW, image=img)


def motion(event):
    x, y = event.x, event.y
    long = (x - 137) * 344 / 977 - 166
    lat = -(y) * 137 / 490 + 88
    print(lat, long)
    canvas.delete("all")
    canvas.create_image(0,0,anchor=tk.NW, image=img)
    canvas.create_image(x,y,anchor=tk.NW, image=flag)
    

 
# This bind window to keys so that move is called when you press a key

root.bind('<Motion>', motion)
 
# this creates the loop that makes the window stay 'active'
root.mainloop()
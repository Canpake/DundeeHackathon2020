import tkinter
from tkinter import Tk, Frame, Canvas, PhotoImage
from final import country_info
from PIL import ImageTk, Image
import requests
from io import BytesIO

flag = None

def motion(event):
    x, y = event.x, event.y
    lon = (x-184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90

    country, facts, trends, flag_url = country_info.get_info(lat, lon)

    response = requests.get(flag_url)
    img_data = response.content

    global flag
    flag = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    image_canvas.delete("all")
    image_canvas.create_image(593, 304, image=world_map)
    image_canvas.create_image(x, y, anchor=tkinter.NW, image=flag)

    print(lat, lon)
    print(country, facts, trends)


def right_click(event):
    print("right click")
    # doesn't work, yikes
    # pin = ImageTk.PhotoImage(file="../images/pin.png")
    # pin_canvas = Canvas(root, bg="blue", width=80, height=120)
    # pin_canvas.create_image(event.x, event.y, image=pin)
    # pin_canvas.place(x=event.x, y=event.y)

    # pin_canvas = Canvas(root, width=80, height=120)
    # pin_canvas.place(x=100, y=100)
    #
    # pin = ImageTk.PhotoImage(file="../images/pin.png")
    # pin_canvas.create_image(40, 60, image=pin)


root = Tk()
root.geometry("1186x609")

image_canvas = Canvas(root, bg="blue", width=1186, height=609)
image_canvas.place(relx=0, rely=0)

world_map = ImageTk.PhotoImage(Image.open("../images/world_map.png"))
image_canvas.create_image(593, 304, image=world_map)

root.bind('<Motion>', motion)
root.bind("<Button-2>", right_click)
root.mainloop()


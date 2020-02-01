from PIL import ImageTk,Image  
from tkinter import Tk, Canvas, PhotoImage


def motion(event):
    x, y = event.x, event.y
    lon = (x - 137) * 344 / 977 - 166
    lat = -(y) * 137 / 490 + 88
    print(lat, lon)



root = Tk()
root.geometry("1186x609")
root.bind('<Motion>', motion)
image_canvas = Canvas(root, bg = "blue", width=1186, height=609)
image_canvas.place(relx=0, rely=0)

world_map = ImageTk.PhotoImage(Image.open("world_map.png"))  
image_canvas.create_image(593, 304, image=world_map)
root.mainloop()
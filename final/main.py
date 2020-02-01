from tkinter import Tk, Canvas, PhotoImage
from final import country_info
from PIL import ImageTk, Image


def motion(event):
    x, y = event.x, event.y
    lon = (x-184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90
    print(lat, lon)

    country, facts, trends = country_info.get_info(lat, lon)
    print(country, facts, trends)


root = Tk()
root.geometry("1186x609")
root.bind('<Motion>', motion)
image_canvas = Canvas(root, bg = "blue", width=1186, height=609)
image_canvas.place(relx=0, rely=0)

# world_map = PhotoImage(file="../images/world_map.png")    # alternative information
world_map = ImageTk.PhotoImage(Image.open("../images/world_map.png"))
image_canvas.create_image(593, 304, image=world_map)
root.mainloop()


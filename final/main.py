from tkinter import Tk, Canvas, PhotoImage
from final import country_info


def motion(event):
    x, y = event.x, event.y
    long = (x - 137) * 344 / 977 - 166
    lat = -(y) * 137 / 490 + 88
    print(lat, long)

    country, facts, trends = country_info.get_info(lat, long)
    print(country, facts, trends)


root = Tk()
root.geometry("1200x519")
root.bind('<Motion>', motion)
image_canvas = Canvas(root, width=1200, height=750)
image_canvas.place(relx=0, rely=0)
world_map = PhotoImage(file="../images/world_map.gif")
# world_map = PhotoImage(file="../images/world_map.png")    # alternative information
image_canvas.create_image(600, 259.5, image=world_map)
root.mainloop()
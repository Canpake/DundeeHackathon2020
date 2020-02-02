import tkinter
from tkinter import Tk, Canvas, Entry, Button, Label, HORIZONTAL
from tkinter.ttk import *
from final import country_info
import PIL
from PIL import ImageTk, Image
import requests
from io import BytesIO
import threading
from time import sleep
import sys
import wikipedia


# Constants for flag display
FLAG_SCALE = 0.1
FLAG_OFFSET = (30, 15)

x = 0
y = 0
country = None
flag = None
flag_url = "https://flagpedia.net/data/flags/normal/tg.png"     # default value for flag to begin with
flag_image = None
flag_update = True   # boolean flag for whether to update the flag
facts = []

def motion(event):
    global x, y, country, facts, flag_url
    x, y = event.x, event.y
    lon = (x - 184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90

    country, facts, trends, flag_url = country_info.get_info(lat, lon)

    # debug
    # print(lat, lon)
    # print(country, facts, trends, flag_url)


def right_click(event):
    # draw a pin at the clicked location
    image_canvas.create_image(event.x, event.y, image=pin)

    # prompt for user entry to add text associated with the pin
    def set_pin_text():
        pin_label = Label(image_canvas, text=pin_entry.get(), bg='gray')
        pin_label.place(x=event.x, y=event.y+20)
        pin_entry.place_forget()
        pin_button.place_forget()

    # set entry + button
    pin_entry = Entry(image_canvas)
    pin_entry.place(x=event.x+10, y=event.y+10)

    pin_button = Button(image_canvas, text="set", width=6, command=set_pin_text)
    pin_button.place(x=event.x+10, y=event.y+40)


current_wikipedia = ""


def left_click(event):

    _x, _y = event.x, event.y

    lon = (_x - 184) * 302 / 939 - 124
    lat = -(_y) * 180 / 609 + 90

    country, facts, trends, flag_url = country_info.get_info(lat, lon)

    global current_wikipedia
    if country == current_wikipedia:
        current_wikipedia = ""
        image_canvas.itemconfigure(country_wikipedia, anchor=tkinter.NW, text="")
    else:
        current_wikipedia = country
        sentences = str(wikipedia.summary(country, sentences=5))
        image_canvas.itemconfigure(country_wikipedia, anchor=tkinter.NW, text=sentences)


# updates on flag + country information
def update():
    while flag_update:
        # find flag image from url
        global country, flag, flag_url, flag_image, facts
        response = requests.get(flag_url)
        img_data = response.content

        try:
            # get image size + resize
            width, height = Image.open(BytesIO(img_data)).size
            flag_image = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((int(width*FLAG_SCALE), int(height*FLAG_SCALE)), Image.ANTIALIAS))
        except PIL.UnidentifiedImageError:
            # hard-coded resize; no_flag is 550x275px.
            flag_image = ImageTk.PhotoImage(Image.open("../images/no_flag.png").resize((int(550*FLAG_SCALE), int(275*FLAG_SCALE))))

        # redraw flag at cursor location
        image_canvas.delete(flag)
        flag = image_canvas.create_image(x+FLAG_OFFSET[0], y+FLAG_OFFSET[1], anchor=tkinter.NW, image=flag_image)

        # redraw text
        image_canvas.itemconfigure(country_text, anchor=tkinter.SW, text=country)

        # text_to_display = "Statistics:\n\n"
        text_to_display = ""
        try:
            order_of_stats = ["Population: ", "GDP: ", "Area: "]
            for i in range(len(facts)):
                text_to_display = text_to_display + order_of_stats[i] + str(facts[i]) + "\n"
                # print("Text to display ", text_to_display)
            image_canvas.itemconfigure(country_stats, anchor=tkinter.NW, text=text_to_display)
        except TypeError:
            continue
        try:
            if len(facts) == 3:
                update_progress_bar(int(facts[0]), int(facts[1].split()[0]), int(facts[2].split(" ")[0]))
            else:
                update_progress_bar(0,0,0)
        except ValueError:
            update_progress_bar(0,0,0)
            continue
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

# draw text
country_text = image_canvas.create_text(10, 520, width=300, font=('Courier', 20, 'bold'))
country_stats = image_canvas.create_text(10, 520, width=300, font=('Courier', 16))
country_wikipedia = image_canvas.create_text(390, 445, width=610, font=('Courier', 10))


# Test 4 upadte =======================
population_bar = image_canvas.create_rectangle(300, 400, 700, 440, fill='red')
gdp_bar = image_canvas.create_rectangle(300, 450, 700, 490, fill='red')
area_bar = image_canvas.create_rectangle(300, 500, 700, 540, fill='red')
def update_progress_bar(population, gdp, area):
    global  population_bar, gdp_bar, area_bar
    image_canvas.delete(population_bar)
    image_canvas.delete(gdp_bar)
    image_canvas.delete(area_bar)
    population_bar = image_canvas.create_rectangle(10, 460*(1 - population/1409517000) + 10, 30, 470, fill='red')
    gdp_bar = image_canvas.create_rectangle(40, 460*(1 - gdp/18036648) + 10, 60, 470, fill='blue')
    area_bar = image_canvas.create_rectangle(70, 460*(1 - area/17098246) + 10, 90, 470, fill='green')

update_progress_bar(400,400,400)

# bind actions
root.bind('<Motion>', motion)
root.bind("<Button-2>", right_click)
root.bind('<Button-1>', left_click)

# multithreading on flag loading
threads = []
a = threading.Thread(target=update)
threads.append(a)
a.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

import tkinter
from tkinter import Tk, Canvas, Entry, Button, Label
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
trends = None
flag_url = ""  # default value for flag to begin with
flag_image = None
flag_update = True  # boolean flag for whether to update the flag
facts = []
current_country = None
pins = []
pin_labels = []
duck = False    # ???


def motion(event):
    global x, y, country, facts, trends, flag_url, duck
    x, y = event.x, event.y
    lon = (x - 184) * 302 / 939 - 124
    lat = -(y) * 180 / 609 + 90

    if round(lon) == -1 and round(lat) == 63:
        duck = True
    else:
        duck = False

    country, facts, trends, flag_url = country_info.get_info(lat, lon)

    # debug
    # print(lat, lon)
    # print(country, facts, trends, flag_url)


def left_click(event):
    global current_country, trends
    if country == current_country:
        # if clicking on the same country as previously, both trends + wikipedia
        current_country = None
        image_canvas.itemconfigure(country_trends, anchor=tkinter.SW, text="")
        image_canvas.itemconfigure(country_wikipedia, anchor=tkinter.SW, text="")
    else:
        # update wikipedia text
        current_country = country
        sentences = str(wikipedia.summary(country, sentences=3))
        image_canvas.itemconfigure(country_wikipedia, anchor=tkinter.SW, text=sentences)

        if trends is not None and len(trends) > 0:
            # update trend text
            trend_text = "Trends\n\n"
            for i in range(len(trends)):
                trend_text += (trends[i] + '\n')
            image_canvas.itemconfigure(country_trends, anchor=tkinter.SW, text=trend_text)
        else:
            image_canvas.itemconfigure(country_trends, anchor=tkinter.SW, text="")


def right_click(event):
    # draw a pin at the clicked location
    pin_image = image_canvas.create_image(event.x, event.y, image=pin_img)

    # prompt for user entry to add text associated with the pin
    def set_pin_text():
        if pin_entry.get():
            pin_label = Label(image_canvas, text=pin_entry.get(), bg='gray')
            pin_label.place(x=event.x, y=event.y + 20)
            pin_entry.place_forget()
            pin_button.place_forget()

            # for i in range(0, 10):
            #     image_canvas.move(pin_image, 0, 1)

            # add to list of pins and pin_labels (for later removal)
            pins.append(pin_image)
            pin_labels.append(pin_label)
        else:   # if pin text is empty, then delete the pin and don't place a label
            image_canvas.delete(pin_image)
            pin_entry.place_forget()
            pin_button.place_forget()

    # set entry + button
    pin_entry = Entry(image_canvas)
    pin_entry.place(x=event.x + 10, y=event.y + 10)

    pin_button = Button(image_canvas, text="set", width=6, command=set_pin_text)
    pin_button.place(x=event.x + 10, y=event.y + 40)


def reset_pins():
    global pins, pin_labels
    # .delete() on pins, .destroy() on labels
    for pin in pins:
        image_canvas.delete(pin)
    for label in pin_labels:
        label.destroy()

    # reset lists
    pins = []
    pin_labels = []


# updates on flag + country information
def update():
    while flag_update:
        # find flag image from url
        global country, flag, flag_url, flag_image, facts, duck

        # ???
        if duck:
            flag_image = ImageTk.PhotoImage(
                Image.open("../images/quack.jpeg").resize((int(1000*FLAG_SCALE), int(1000*FLAG_SCALE))))
        else:
            try:
                response = requests.get(flag_url)
                img_data = response.content
                # get image size + resize
                width, height = Image.open(BytesIO(img_data)).size
                flag_image = ImageTk.PhotoImage(
                    Image.open(BytesIO(img_data)).resize((int(width * FLAG_SCALE), int(height * FLAG_SCALE)),
                                                         Image.ANTIALIAS))
            except (PIL.UnidentifiedImageError, requests.exceptions.MissingSchema):
                # hard-coded resize; no_flag is 550x350px.
                flag_image = ImageTk.PhotoImage(
                    Image.open("../images/no_flag.png").resize((int(550 * FLAG_SCALE), int(350 * FLAG_SCALE))))

        # redraw flag at cursor location
        image_canvas.delete(flag)
        flag = image_canvas.create_image(x + FLAG_OFFSET[0], y + FLAG_OFFSET[1], anchor=tkinter.NW, image=flag_image)

        # redraw country text
        image_canvas.itemconfigure(country_text, anchor=tkinter.SW, text=country)

        # redraw country information
        text_to_display = ""
        try:
            order_of_stats = ["Population: ", "GDP: ", "Area: "]
            for i in range(len(facts)):
                text_to_display = text_to_display + order_of_stats[i] + str(facts[i]) + "\n"
                # print("Text to display ", text_to_display)
            image_canvas.itemconfigure(country_stats, anchor=tkinter.NW, text=text_to_display)
        except ValueError:
            continue

        # redraw population bars
        try:
            if len(facts) == 3:
                update_progress_bar(int(facts[0]), int(facts[1].split()[0]), int(facts[2].split(" ")[0]))
            else:
                update_progress_bar(0, 0, 0)
        except ValueError:
            update_progress_bar(0, 0, 0)
            continue

        sleep(0.01)
    return


# updates on information bars
def update_progress_bar(population, gdp, area):
    global population_bar, gdp_bar, area_bar
    image_canvas.delete(population_bar)
    image_canvas.delete(gdp_bar)
    image_canvas.delete(area_bar)
    population_bar = image_canvas.create_rectangle(10, 460 * (1 - population / 1409517000) + 10, 30, 470, fill='red')
    gdp_bar = image_canvas.create_rectangle(40, 460 * (1 - gdp / 18036648) + 10, 60, 470, fill='blue')
    area_bar = image_canvas.create_rectangle(70, 460 * (1 - area / 17098246) + 10, 90, 470, fill='green')


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
pin_img = ImageTk.PhotoImage(Image.open("../images/pin.png").resize((20, 30)))

# draw map
image_canvas.create_image(593, 304, image=world_map)

# draw rectangles around text
# rects = []  # list of rectangles
# def create_rectangle(x1, y1, x2, y2, **kwargs):
#     if 'alpha' in kwargs:
#         alpha = int(kwargs.pop('alpha') * 255)
#         fill = kwargs.pop('fill')
#         fill = root.winfo_rgb(fill) + (alpha,)
#         rect = Image.new('RGBA', (x2-x1, y2-y1), fill)
#         rects.append(ImageTk.PhotoImage(rect))
#         image_canvas.create_image(x1, y1, image=rects[-1], anchor='nw')
#     image_canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
#
# create_rectangle(340, 495, 1000, 600, outline='black', width='2', fill='white', alpha=0.4)

# draw text
country_text = image_canvas.create_text(10, 540, width=300, font=('Courier', 20, 'bold'))
country_stats = image_canvas.create_text(10, 540, width=300, font=('Courier', 16))
country_wikipedia = image_canvas.create_text(450, 540, width=610, font=('Courier', 10))
country_trends = image_canvas.create_text(150, 500, width=200, font=("Courier", 14))

# draw initial info bars
population_bar = image_canvas.create_rectangle(0, 0, 0, 0, fill='red')
gdp_bar = image_canvas.create_rectangle(0, 0, 0, 0, fill='red')
area_bar = image_canvas.create_rectangle(0, 0, 0, 0, fill='red')
# draw text under info bars
image_canvas.create_text(20, 485, width=30, font=('Courier', 16, 'bold'), text="P")
image_canvas.create_text(50, 485, width=30, font=('Courier', 16, 'bold'), text="G")
image_canvas.create_text(80, 485, width=30, font=('Courier', 16, 'bold'), text="A")

# add pin reset button
pin_reset = Button(root, text='Reset Pins', width='9', command=reset_pins)
pin_reset.place(x=1176, y=10, anchor=tkinter.NE)

# bind actions
root.bind('<Motion>', motion)
root.bind('<Button-1>', left_click)
root.bind("<Button-2>", right_click)

# multithreading on flag loading
threads = []
a = threading.Thread(target=update)
threads.append(a)
a.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

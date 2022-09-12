import tkinter as tk
import ai
import numpy as np
from tkinter import *
from PIL import Image, ImageTk, ImageDraw

model = ai.load_ai()

window = tk.Tk()
window.title("Tebak Angka")

img = Image.new(mode="1", size=(500,500), color=0)
tkimage = ImageTk.PhotoImage(img)
canvas = tk.Label(window, image=tkimage)
canvas.pack()

draw = ImageDraw.Draw(img)

last_point = (0, 0)
prediction = tk.StringVar()
label = tk.Label(window, textvariable=prediction)


def draw_image(event):
    global last_point, tkimage
    current_point = (event.x, event.y)
    draw.line([last_point, current_point], fill=255, width=25)
    last_point=current_point
    tkimage = ImageTk.PhotoImage(img)
    canvas['image'] = tkimage
    canvas.pack
    img_temp = img.resize((28, 28))
    img_temp = np.array(img_temp)
    img_temp = img_temp.flatten()
    output = model.predict([img_temp])
    if(output[0] == 0):
        prediction.set("Nomor yang anda gambar adalah = satu")
    elif(output[0] == 1):
        prediction.set("Nomor yang anda gambar adalah = dua")
    else:
        prediction.set("Nomor yang anda gambar adalah = tiga")
    label.pack()

def start_draw(event):
    global last_point
    last_point=(event.x, event.y)

def reset_canvas(event):
    global tkimage, img, draw, prediction
    img = Image.new(mode="1", size=(500,500), color=0)
    draw = ImageDraw.Draw(img)
    tkimage = ImageTk.PhotoImage(img)
    canvas['image'] = tkimage
    canvas.pack
    prediction.set("")

satu=0
dua=0
tiga=0

def save_image(event):
    global satu,dua,tiga
    img_temp=img.resize((28,28))
    if(event.char== "1"):
        img_temp.save(f"satu/{satu}.png")
        satu += 1
    elif(event.char== "2"):
        img_temp.save(f"dua/{dua}.png")
        dua += 1
    if(event.char== "3"):
        img_temp.save(f"tiga/{tiga}.png")
        tiga += 1
 
window.bind("<B1-Motion>", draw_image)
window.bind("<ButtonPress-1>", start_draw)
window.bind("<ButtonPress-3>", reset_canvas)
window.bind("<Key>", save_image)
window.mainloop()
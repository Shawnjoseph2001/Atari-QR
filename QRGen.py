# Python program to generate QR code
import cv2
import qrcode
import os
from tkmacosx import Button
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk

current_a26_file = ""
window = Tk()
global qr_image


def save_a26_file():
    qr_image.save(filedialog.asksaveasfilename(title="Save as:", defaultextension="png", initialdir=os.getcwd()))


def open_a26_file():
    window.a26_filename = filedialog.askopenfilename(title="Select file",
                                                     filetypes=((".A26 file:", "*.A26"), (".BIN file", ".BIN")))
    global current_a26_file
    global qr_image
    current_a26_file = window.a26_filename
    if current_a26_file != "":
        if os.path.getsize(current_a26_file) > 3023872:
            print("This file is too big. Only Atari 2600 games designed for a 2KB cartridge will work.")
        else:
            atari_file = open(current_a26_file, mode='rb').read()
            my_qr = qrcode.QRCode(
                version=40,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=2,
                border=4,
            )
            my_qr.add_data(atari_file)
            qr_image = my_qr.make_image()
            img = ImageTk.PhotoImage(qr_image)
            save_button = Button(window, text="Save file: ", fg='blue', command=save_a26_file)
            save_button.place(x=80, y=60)
            panel = Label(window, image=img)
            panel.image = img
            panel.place(x=0, y=90)


def play_a26_qr():
    window.import_qr = filedialog.askopenfilename(title="Select file",
                                                  filetypes=((".JPG file:", "*.jpg"), (".BIN file", ".png")))
    qr_img = cv2.imread(window.import_qr)
    det = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = det.detectAndDecode(qr_img)
    print("Data: ", data, "Bbox: ", bbox, "straight: ", straight_qrcode)


window.title('A2')
currentFile = ""
window.geometry("400x500+10+20")
openButton = Button(window, text="Convert a game file: ", fg='blue', command=open_a26_file)
play_a26 = Button(window, text="Play a QR code: ", fg='blue', command=play_a26_qr)
openButton.place(x=80, y=0)
play_a26.place(x=80, y=30)
window.mainloop()

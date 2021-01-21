# Python program to generate QR code
import qrcode
import os
from tkmacosx import Button
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import zxing
import base91
import subprocess
import cv2

current_a26_file = ""
window = Tk()
global qr_image


def save_a26_file():
    qr_image.save(filedialog.asksaveasfilename(title="Save as:", defaultextension="png", initialdir=os.getcwd()))


def open_a26_file():
    window.a26_filename = filedialog.askopenfilename(title="Select file")
    global current_a26_file
    global qr_image
    current_a26_file = window.a26_filename
    if current_a26_file != "":
        atari_file = open(current_a26_file, mode='rb').read()
        my_qr = qrcode.QRCode(
            version=40,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )
        qr_string = base91.encode(atari_file)
        my_qr.add_data(qr_string)
        qr_image = my_qr.make_image()
        img = ImageTk.PhotoImage(qr_image)
        save_button = Button(window, text="Save file: ", fg='blue', command=save_a26_file)
        save_button.place(x=80, y=90)
        panel = Label(window, image=img)
        panel.image = img
        panel.image = img
        panel.place(x=0, y=120)


def play_a26_qr():
    window.import_qr = filedialog.askopenfilename(title="Select file")
    reader = zxing.BarCodeReader()
    barcode = reader.decode(window.import_qr)
    # print(barcode.raw)
    converted_file = base91.decode(barcode.raw)
    output_file = open("output.a26", "wb")
    output_file.write(converted_file)
    output_file.close()
    subprocess.run(["stella", "output.a26"])


def video_reader():
    cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    loop_cont = True
    qr_data = ""
    while loop_cont:
        _, img = cam.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            print("QR Code detected-->", data)
            qr_data = data
            loop_cont = False
        cv2.imshow("img", img)
    cam.release()
    cv2.destroyAllWindows()
    converted_file = base91.decode(qr_data)
    output_file = open("output.a26", "wb")
    output_file.write(converted_file)
    output_file.close()
    subprocess.run(["stella", "output.a26"])


window.title('Atari QR')
currentFile = ""
window.geometry("400x550+10+20")
openButton = Button(window, text="Convert a game file: ", fg='blue', command=open_a26_file)
play_a26 = Button(window, text="Play a QR code from an image file: ", fg='blue', command=play_a26_qr)
play_qr_cam = Button(window, text="Scan a QR code from the camera:", fg='blue', command=video_reader)
openButton.place(x=80, y=0)
play_a26.place(x=80, y=30)
play_qr_cam.place(x=80, y=60)
window.mainloop()

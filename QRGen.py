# Python program to generate QR code
import qrcode

import os
f = open("")
my_QR = qrcode.make()
image = my_QR.get_image()
print(image)
image.save("File.png")
# command to move the QR code to the desktop


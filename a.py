
from __future__ import division, print_function, unicode_literals

import os
import sys
import random
from PIL import Image
import argparse
import logging
__version__ = "0.1"
import numpy as np


def load_image(name):
    return Image.open(name)

def prepare_message_image(image, size):
    if size != image.size:
        image = image.resize(size, Image.ANTIALIAS)
    return image

def generate_secret(size, secret_image = None):
    width, height = size
    new_secret_image = Image.new(mode = "RGB", size = (width * 2, height * 2))

    for x in range(0, 2 * width, 2):
        for y in range(0, 2 * height, 2):
            color1 = np.random.randint(255)
            color2 = np.random.randint(255)
            color3 = np.random.randint(255)
            new_secret_image.putpixel((x,  y),   (color1,color2,color3))
            new_secret_image.putpixel((x+1,y),   (255-color1,255-color2,255-color3))
            new_secret_image.putpixel((x,  y+1), (255-color1,255-color2,255-color3))
            new_secret_image.putpixel((x+1,y+1), (color1,color2,color3))
                
    return new_secret_image

def generate_ciphered_image(secret_image, prepared_image):
    width, height = prepared_image.size
    ciphered_image = Image.new(mode = "RGB", size = (width * 2, height * 2))
    for x in range(0, width*2, 2):
        for y in range(0, height*2, 2):
            sec = secret_image.getpixel((x,y))
            msssg = prepared_image.getpixel((int(x/2),int(y/2)))
            color1 = (msssg[0]+sec[0])%256
            color2 = (msssg[1]+sec[1])%256
            color3 = (msssg[2]+sec[2])%256
            ciphered_image.putpixel((x,  y),   (color1,color2,color3))
            ciphered_image.putpixel((x+1,y),   (255-color1,255-color2,255-color3))
            ciphered_image.putpixel((x,  y+1), (255-color1,255-color2,255-color3))
            ciphered_image.putpixel((x+1,y+1), (color1,color2,color3))
                
    return ciphered_image


def generate_image_back(secret_image, ciphered_image):
    width, height = secret_image.size
    new_image = Image.new(mode = "RGB", size = (int(width / 2), int(height / 2)))
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            sec = secret_image.getpixel((x,y))
            cip = ciphered_image.getpixel((x,y))
            color1 = (cip[0]-sec[0])%256
            color2 = (cip[1]-sec[1])%256
            color3 = (cip[2]-sec[2])%256
            new_image.putpixel((int(x/2),  int(y/2)),   (color1,color2,color3))
               
    return new_image



def main():
    message_image = load_image(sys.argv[2])
    size = message_image.size
    width, height = size

    save_secret = False
    secret_image = generate_secret(size)
    secret_image.save("secret.png")
    save_secret = True

    prepared_image = prepare_message_image(message_image, size)
    ciphered_image = generate_ciphered_image(secret_image, prepared_image)
    new_image = generate_image_back(secret_image, ciphered_image)
    new_image1 = new_image.convert("RGB")

    ciphered_image.save("ciphered.png")
    prepared_image.save("prepared.png")
    new_image1.save("new.png")

    

if __name__ == '__main__':
    main()

__author__ = 'Terrace Boiz'

#!/usr/bin/python

# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

import Image
import ImageDraw
import time
import ImageFont
import mbtaTimeDisplay, mbtaJsonParse, Weather
from collections import defaultdict
from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 2)
# Bitmap example w/graphics prims
image = Image.new("1", (64, 32)) # Can be larger than matrix if wanted!!
draw  = ImageDraw.Draw(image)    # Declare Draw instance before prims
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf",12)
train = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",10)
weather = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",8)


def main():
    draw.text((5,-2), "Next Trains", font=font, fill=1)
    trainDisplay()
    weatherDisplay()
    matrix.Clear()
    matrix.SetImage(image.im.id,0,0)

def trainDisplay():
    try:
        #temp = defaultdict(list)
        #temp['Northbound'].append(78)
        #temp['Northbound'].append(300)
        #train1,train2 = mbtaTimeDisplay.panelTrain(temp)
        train1, train2 = mbtaTimeDisplay.panelTrain(mbtaJsonParse.schedule)
        draw.text((9, 10), train1, font=train, fill=1)
        draw.text((9,20), train2, font=train, fill=1)
    except:
        draw.text((9, 10), "No Trains", font=train, fill=1)
        draw.text((9,20), "Faggot", font=train, fill=1)

def weatherDisplay():
    try:
        currentWeather = Weather.weatherPanel()
        draw.text((48, 22), currentWeather, font=weather, fill=1)
    except:
        draw.text((48, 22), "NO", font=weather, fill=1)



if __name__ == "__main__":
    main()



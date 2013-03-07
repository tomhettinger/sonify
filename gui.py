#!/usr/bin/python
from Tkinter import *
from PIL import Image, ImageTk

def write_wave():
    pass

def play_wave():
    pass

def sonify():
    pass

def load_image():
    filename = loadEntry.get()
    print filename
    try:
        image = Image.open("./images/forest.jpg")
    except:
        print "bad entry"
        return
    if image.size[0] < image.size[1]:
        factor = 512. / image.size[0]
    else:
        factor = 364. / image.size[1]
    width = int(image.size[0]*factor)
    height = int(image.size[1]*factor)
    resizedImage = image.resize((width, height), Image.ANTIALIAS)  
    photo = ImageTk.PhotoImage(resizedImage)
    imOrig.configure(image=photo)
    imOrig.image = photo


root = Tk()
root.title("Sonify")

# Frames within root
welcomeFrame = Frame(root)  # Size is overwritten by its contents.
welcomeFrame.grid(column=0, row=0)

dataFrame = Frame(root)  # Size is overwritten by its contents.
dataFrame.grid(column=0, row=1)

imageFrame = Frame(root)
imageFrame.grid(column=1, row=0)

powerFrame = Frame(root)
powerFrame.grid(column=1, row=1)


# Welcome frame
dummyFrame1 = Frame(welcomeFrame, width=512, height=364, relief='sunken', borderwidth=2)
dummyFrame1.grid(column=0, row=0)
introText = """
Hello, and welcome to Sonify.  To begin, load an image from your
computer and click 'sonify'. Similar colors will be grouped into
notes from the C Major scale.  The color the note has, the stronger
the note is played.

After you sonify, you can play it back or write it to a file.

<Currently only supports RGB .jpg.>
"""
greeting = Label(welcomeFrame, text=introText, justify="left")
greeting.grid(column=0, row=0, rowspan=5, columnspan=5)


# Data frame
dummyFrame2 = Frame(dataFrame, width=512, height=364, relief='sunken', borderwidth=2)
dummyFrame2.grid(column=0, row=0, columnspan=2, rowspan=6)

loadFrame = Frame(dataFrame)
loadFrame.grid(column=0, row=0)
loadEntry = Entry(loadFrame, width=45)
loadEntry.insert(0, "./images/forest.jpg")
loadEntry.grid(column=0, row=0)
loadButton = Button(loadFrame, text='Load', command=load_image)
loadButton.grid(column=1, row=0)

sonifyButton = Button(dataFrame, text='Sonify', width=50, command=sonify)
sonifyButton.grid(column=0, row=1)

playButton = Button(dataFrame, text='Play', width=50, command=play_wave)
playButton.grid(column=0, row=2)

writeFrame = Frame(dataFrame)
writeFrame.grid(column=0, row=3)
writeEntry = Entry(writeFrame, width=45)
writeEntry.grid(column=0, row=0)
writeButton = Button(writeFrame, text='Write', command=write_wave)
writeButton.grid(column=1, row=0)

quitButton = Button(dataFrame, text='Quit', width=50, command=root.destroy)
quitButton.grid(column=0, row=4)


# Image frame
dummyFrame3 = Frame(imageFrame, width=512, height=364, relief='sunken', borderwidth=2)
dummyFrame3.grid(column=0, row=0)
imOrig = Label(imageFrame, image=None)
imOrig.grid(column=0, row=0)


# Power frame
dummyFrame4 = Frame(powerFrame, width=512, height=364, relief='sunken', borderwidth=2)
dummyFrame4.grid(column=0, row=1)
powerSpec = Label(powerFrame, text="Power Spec Here")
powerSpec.grid(column=0, row=1)


root.mainloop()
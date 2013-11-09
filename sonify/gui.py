#!/usr/bin/python
"""A graphical interface for loading images and coverting 
them into sounds based on the number of pixels present
around the color wheel."""

import os
from Tkinter import *

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import wavebender

import sonify

class GUI:

    def __init__(self, parent):
        # Instance Attributes
        self.targetImage = None
        self.channels = None
        self.maxWidth = 1000
        self.maxHeight = 600
        self.rate = 16000
        self.time = 4
        self.myParent = parent
        self.introText = """
        Hello, and welcome to Sonify.  To begin, load an image from your
        computer. Similar colors will be grouped into notes from the 
        C Major scale.  The more color a note has, the stronger
        the note is played.

        After you sonify, you can write it to a file and play it back.

        <Currently only supports RGB .jpg>
        """

        # Parent Frame containing four sub-frames
        self.welcomeFrame = Frame(parent)  # Size is overwritten by its contents.
        self.welcomeFrame.grid(column=0, row=0)
        self.dataFrame = Frame(parent)     # Size is overwritten by its contents.
        self.dataFrame.grid(column=0, row=1)
        self.imageFrame = Frame(parent)
        self.imageFrame.grid(column=1, row=0)
        self.powerFrame = Frame(parent)
        self.powerFrame.grid(column=1, row=1)

        # Welcome frame
        self.dummyFrame1 = Frame(self.welcomeFrame, width=self.maxWidth/2, height=self.maxHeight/2, relief='sunken', borderwidth=2)
        self.dummyFrame1.grid(column=0, row=0)
        self.greetingLabel = Label(self.welcomeFrame, text=self.introText, justify="left")
        self.greetingLabel.grid(column=0, row=0, rowspan=5, columnspan=5)

        # Data frame
        self.dummyFrame2 = Frame(self.dataFrame, width=self.maxWidth/2, height=self.maxHeight/2, relief='sunken', borderwidth=2)
        self.dummyFrame2.grid(column=0, row=0, columnspan=2, rowspan=5)
        # Load entry and button
        self.loadImageFrame = Frame(self.dataFrame)
        self.loadImageFrame.grid(column=0, row=0)
        self.loadImageEntry = Entry(self.loadImageFrame, width=45)
        self.loadImageEntry.insert(0, "./images/forest.jpg")
        self.loadImageEntry.grid(column=0, row=0)
        self.loadImageButton = Button(self.loadImageFrame, text='Load', command=self.load_image)
        self.loadImageButton.grid(column=1, row=0)
        # Sonify button
        self.sonifyButton = Button(self.dataFrame, text='Sonify', width=50, command=self.sonify_image)
        self.sonifyButton.grid(column=0, row=1)
        # Write field and button
        self.writeFrame = Frame(self.dataFrame)
        self.writeFrame.grid(column=0, row=2)
        self.writeEntry = Entry(self.writeFrame, width=45)
        self.writeEntry.insert(0, "./new_sonification.wav")
        self.writeEntry.grid(column=0, row=0)
        self.writeButton = Button(self.writeFrame, text='Write', command=self.write_wave)
        self.writeButton.grid(column=1, row=0)
        # Quit button
        self.quitButton = Button(self.dataFrame, text='Quit', width=50, command=parent.destroy)
        self.quitButton.grid(column=0, row=3)
        # Message Label
        self.messageLabel = Label(self.dataFrame, justify="left")
        self.messageLabel.grid(column=0, row=4)

        # Image frame
        self.dummyFrame3 = Frame(self.imageFrame, width=self.maxWidth/2, height=self.maxHeight/2, relief='sunken', borderwidth=2)
        self.dummyFrame3.grid(column=0, row=0)
        self.displayIm = Label(self.imageFrame, image=None)
        self.displayIm.grid(column=0, row=0)

        # Power frame
        self.dummyFrame4 = Frame(self.powerFrame, width=self.maxWidth/2, height=self.maxHeight/2, relief='sunken', borderwidth=2)
        self.dummyFrame4.grid(column=0, row=1)
        self.powerFigure = Figure(figsize=(self.maxWidth/200., self.maxHeight/200.), dpi=97)
        self.powerFigureCanvas = FigureCanvasTkAgg(self.powerFigure, master=self.powerFrame)
        self.powerFigureCanvas.show()
        self.powerWidget = self.powerFigureCanvas.get_tk_widget()
        self.powerWidget.grid(column=0, row=1)


    def write_wave(self):
        """Pull the output path from the write field 
        and save the sound wave to this file."""
        self.messageLabel.configure(text="")
        if self.channels is None:
            self.messageLabel.configure(text="Must sonify image first.")
            return
        filename = self.writeEntry.get()
        if filename is None:
            self.messageLabel.configure(text="Enter a filename to write.")
            return
        self.messageLabel.configure(text="Writing ...")
        self.myParent.update_idletasks()
        try:
            thisSamples = wavebender.compute_samples(self.channels, nsamples=self.rate*self.time)
            wavebender.write_wavefile(filename, samples=thisSamples, nframes=self.rate*self.time, 
                                      nchannels=1, framerate=self.rate)
            self.messageLabel.configure(text="Successfully written to %s" % filename)
        except:
            self.messageLabel.configure(text="Write failed. Try another image or output filename.")


    def sonify_image(self):
        """Use the sonify module to create a sound wave based on color."""
        self.messageLabel.configure(text="")
        if self.targetImage is None:
            self.messageLabel.configure(text="Must load an image first.")
            return
        if self.targetImage.mode != 'RGB':
            self.messageLabel.configure(text='Not RGB.  %s is invalid.' % self.targetImage.mode)
            return
        self.messageLabel.configure(text="Converting ...")
        self.myParent.update_idletasks()

        # Convert the image to YCbCr
        imYCbCr = self.targetImage.convert("YCbCr")
        phi, rad, lum = sonify.phi_from_YCbCr(imYCbCr)
        amps = sonify.get_amplitudes(phi, figure=self.powerFigure)
        self.powerFigureCanvas.show()
        self.channels = ((sonify.super_sine_wave(freqs=sonify.TONES, amps=amps, framerate=self.rate),),)        
        self.messageLabel.configure(text="Sonification complete.")


    def load_image(self):
        """Open the image from the path specified in the load field."""
        self.messageLabel.configure(text="")
        filename = self.loadImageEntry.get()
        try:
            self.targetImage = Image.open(filename)
        except:
            self.messageLabel.configure(text="Try another filename.")
            return
        if self.targetImage.size[0] < self.targetImage.size[1]:
            factor = self.maxWidth / 2. / float(self.targetImage.size[0])
        else:
            factor = self.maxHeight / 2. / float(self.targetImage.size[1])
        width = int(self.targetImage.size[0]*factor*0.95)
        height = int(self.targetImage.size[1]*factor*0.95)
        resizedImage = self.targetImage.resize((width, height), Image.ANTIALIAS)  
        photo = ImageTk.PhotoImage(resizedImage)
        self.displayIm.configure(image=photo)
        self.displayIm.image = photo


def main():
    """Begin GUI loop."""
    root = Tk()
    root.title("Sonify")
    myGUI = GUI(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()

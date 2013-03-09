#!/usr/bin/python
from Tkinter import *
from PIL import Image, ImageTk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import sonify
import wavebender as wb

class GUI:
    # Class Attributes

    def __init__(self, parent):
        # Instance Attributes
        self.targetImage = None
        self.samples = None
        self.maxWidth = 1000
        self.maxHeight = 600
        self.rate = 8000
        self.time = 4
        self.myParent = parent
        self.introText = """
        Hello, and welcome to Sonify.  To begin, load an image from your
        computer and click 'sonify'. Similar colors will be grouped into
        notes from the C Major scale.  The color the note has, the stronger
        the note is played.

        After you sonify, you can play it back or write it to a file.

        <Currently only supports RGB .jpg.>
        """

        # Four main frames within the parent
        self.welcomeFrame = Frame(parent)  # Size is overwritten by its contents.
        self.welcomeFrame.grid(column=0, row=0)
        self.dataFrame = Frame(parent)  # Size is overwritten by its contents.
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
        self.dummyFrame2.grid(column=0, row=0, columnspan=2, rowspan=6)
        # Load entry and button
        self.loadFrame = Frame(self.dataFrame)
        self.loadFrame.grid(column=0, row=0)
        self.loadEntry = Entry(self.loadFrame, width=45)
        self.loadEntry.insert(0, "./images/forest.jpg")
        self.loadEntry.grid(column=0, row=0)
        self.loadButton = Button(self.loadFrame, text='Load', command=self.load_image)
        self.loadButton.grid(column=1, row=0)
        # Sonify button
        self.sonifyButton = Button(self.dataFrame, text='Sonify', width=50, command=self.sonify_image)
        self.sonifyButton.grid(column=0, row=1)
        # Play button
        self.playButton = Button(self.dataFrame, text='Play', width=50, command=self.play_wave)
        self.playButton.grid(column=0, row=2)
        # Write field and button
        self.writeFrame = Frame(self.dataFrame)
        self.writeFrame.grid(column=0, row=3)
        self.writeEntry = Entry(self.writeFrame, width=45)
        self.writeEntry.insert(0, "./sounds/temp.wav")
        self.writeEntry.grid(column=0, row=0)
        self.writeButton = Button(self.writeFrame, text='Write', command=self.write_wave)
        self.writeButton.grid(column=1, row=0)
        # Quit button
        self.quitButton = Button(self.dataFrame, text='Quit', width=50, command=parent.destroy)
        self.quitButton.grid(column=0, row=4)
        # Message Label
        self.messageLabel = Label(self.dataFrame, justify="left")
        self.messageLabel.grid(column=0, row=5)
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
        self.messageLabel.configure(text="")
        if self.samples is None:
            self.messageLabel.configure(text="Must sonify image first.")
            return
        filename = self.writeEntry.get()
        if filename is None:
            self.messageLabel.configure(text="Enter a filename to write.")
            return
        try:
            wb.write_wavefile(filename, samples=self.samples, nframes=self.rate*self.time, 
                              nchannels=1, framerate=self.rate)
            self.messageLabel.configure(text="Successfully written to %s" % filename)
        except:
            self.messageLabel.configure(text="Write failed. Try another image or output filename.")

    def play_wave(self):
        self.messageLabel.configure(text="")
        self.messageLabel.configure(text="Not yet implemented.")

    def sonify_image(self):
        self.messageLabel.configure(text="")
        if self.targetImage is None:
            self.messageLabel.configure(text="Must load an image first.")
            return
        if self.targetImage.mode != 'RGB':
            self.messageLabel.configure(text='Not RGB.  %s is invalid.' % self.targetImage.mode)
            return
        self.messageLabel.configure(text="Converting ...")
        self.myParent.update_idletasks()
        imYCbCr = self.targetImage.convert("YCbCr")                       # Convert the image to YCbCr
        phi, rad, lum = sonify.phi_from_YCbCr(imYCbCr)
        amps = sonify.get_amplitudes(phi, figure=self.powerFigure)
        self.powerFigureCanvas.show()
        channels = ((sonify.super_sine_wave(freqs=sonify.tones, amps=amps, framerate=self.rate),),)
        self.samples = wb.compute_samples(channels, nsamples=self.rate*self.time)
        self.messageLabel.configure(text="Sonification complete.")

    def load_image(self):
        self.messageLabel.configure(text="")
        filename = self.loadEntry.get()
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
    # Begin gui framework
    root = Tk()
    root.title("Sonify")
    myGUI = GUI(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()
import Image
import math
from matplotlib import pyplot as pl


# Play a .wav file
#import Tkinter
#import tkSnack as snack
#root = Tkinter.Tk()
#snack.initializeSnack(root) 
#s = snack.Sound(load='./sounds/wail-long.wav')
#c = snack.SnackCanvas(root, height=400) 
#c.pack() 
#c.create_waveform(0, 0, sound=s, height=100, zerolevel=1)
#c.create_spectrogram(0, 150, sound=s, height=200)
#s.play(blocking=True)

# Define the notes to be used
notes = ['a3', 'b3', 'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4', 'c5', 'd5', 'e5', 'f5', 'g5', 'a5']
tones = [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 587.33, 659.26, 698.46, 783.99, 880.00]
scale = zip(notes,tones)

def plot_histogram(im):
    pl.plot(im.histogram())
    pl.title("Pixel Counts by color value for all bands.")
    if im.mode == 'RGB':
        pl.xlabel("Color: R(0-255), B(256-511), G(512-767)")
    pl.ylabel("Number of Pixels")
    pl.yscale("log")
    pl.show()

# Convert CbCr to phi,r
def phi_from_YCbCr(im):
    # This may not be the fastest way.  Consider using im.getdata() or im.split() or colorsys.rgb_to_yiq(r, g, b).
    phi = []
    rad = []
    lum = []
    pix = im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            Y, Cb, Cr = pix[x,y]
            # Offset so values range from [-128,127]
            Cb = Cb - 128
            Cr = Cr - 128
            # Ensure no divide-by-zero
            if Cb == 0: Cb = 1
            if Cr == 0: Cr = 1
            # Append luminosity
            lum.append(Y)
            # Calculate radius
            rad.append(math.sqrt(Cb*Cb + Cr*Cr))
            # Calculate phi
            phi0 = math.atan(Cr/Cb)
            if Cb >= 0 and Cr >= 0:
                phi.append(phi0)
            elif Cb < 0 and Cr >= 0:
                phi.append(phi0 + math.pi)
            elif Cb < 0 and Cr < 0:
                phi.append(phi0 + math.pi)
            else:
                phi.append(phi0 + 2*math.pi)
    return phi, rad, lum


# Open image file and read in the image.
#im = Image.open("./images/test.jpg")
#im = Image.open("./images/firefox.png")
#im = Image.open("./images/fire.jpg")
#im = Image.open("./images/forest.jpg")
#im = Image.open("./images/blue.png")
im = Image.open("./images/mountain.png")

if False:
    thisPix = im.getpixel((400, 100))    # slow.  use .load() instead.
    print "\nRGB for pix(400,100) is %s" % str(thisPix)
    #plot_histogram(im)
    pix = im.load()
    print "\nRGB for pix(400,100) is %s" % str(pix[400, 100])
    size = im.size
    print "\nThe image is %d by %d pixels (%d total)." % (size[0], size[1], size[0]*size[1])
    # Get the number of pixels sitting in each color
    colors = im.getcolors(maxcolors=size[0]*size[1])
    print "\nThere are %d unique colors in this image." % len(colors)
    flatSequence = im.getdata()
    print "\nWhen flattened, the image is %d pixels long." % len(flatSequence)

out = im.convert("YCbCr")
#print "\nThe converted image has mode=%s" % out.mode
#print "\nYCbCr for pix(400,100) is %s" % str(out.load()[400, 100])
#print "\nRGB for pix(400,100) is %s" % str(im.load()[400, 100])

# Split into three images (one for each band).
#y,cb,cr = out.split()
#print min(list(cb.getdata())), max(list(cb.getdata()))
#print y.getextrema(), print cb.getextrema(), print cr.getextrema()
#cb.show()
#im.show()
#cr.show()
#y.show()

# Calculate and plot phi
phi, rad, Y = phi_from_YCbCr(out)


n, bins, patches = pl.hist(phi, 15, log=True)
maxn = math.log10(max(n))
amp = []
for val in n:
    if val == 0:
        amp.append(0)
    else:
        amp.append(math.log10(val) / maxn)
if True:
    pl.xlabel('$\phi$ Tone Parameter')
    pl.ylabel('Number of Pixels')
    pl.show()
    print amp, sum(amp), max(amp)
    print n, len(n)
else:
    import sys
    import wavebender as wb
    fr = 26000
    channels = ((wb.sine_wave(tones[0], amplitude=amp[0], framerate=fr),), 
                (wb.sine_wave(tones[1], amplitude=amp[1], framerate=fr),),
                (wb.sine_wave(tones[2], amplitude=amp[2], framerate=fr),), 
                (wb.sine_wave(tones[3], amplitude=amp[3], framerate=fr),), 
                (wb.sine_wave(tones[4], amplitude=amp[4], framerate=fr),), 
                (wb.sine_wave(tones[5], amplitude=amp[5], framerate=fr),), 
                (wb.sine_wave(tones[6], amplitude=amp[6], framerate=fr),), 
                (wb.sine_wave(tones[7], amplitude=amp[7], framerate=fr),), 
                (wb.sine_wave(tones[8], amplitude=amp[8], framerate=fr),), 
                (wb.sine_wave(tones[9], amplitude=amp[9], framerate=fr),), 
                (wb.sine_wave(tones[10], amplitude=amp[10], framerate=fr),), 
                (wb.sine_wave(tones[11], amplitude=amp[11], framerate=fr),), 
                (wb.sine_wave(tones[12], amplitude=amp[12], framerate=fr),), 
                (wb.sine_wave(tones[13], amplitude=amp[13], framerate=fr),), 
                (wb.sine_wave(tones[14], amplitude=amp[14], framerate=fr),), ) 
    samples = wb.compute_samples(channels)
    wb.write_wavefile(sys.stdout, samples, framerate=fr, nchannels=15)
import Image
import math

from matplotlib import pyplot as pl

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
    # This may not be the fastest way.  Consider using im.getdata() or im.split().
    phi = []
    rad = []
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
            
    print len(phi), phi[100]
    print len(rad), rad[100]
    #for i in range(len(phi)):
        #phi[i] = phi[i]*180. / math.pi
    pl.hist(phi, 100)
    pl.xlabel('Frequency * Const')
    pl.ylabel('Number of Pixels')
    pl.show()
    return phi, rad


# Open image file and read in the image.
im = Image.open("./images/test.jpg")
extrema = im.getextrema()
print "\nExtrema:"
print extrema

#palette = im.getpalette()           # im.putpalette()
#print palette

thisPix = im.getpixel((400, 100))    # slow.  use .load() instead.
print "\nRGB for pix(400,100) is %s" % str(thisPix)

#plot_histogram(im)

pix = im.load()
print "\nRGB for pix(400,100) is %s" % str(pix[400, 100])

#im.show()

size = im.size
print "\nThe image is %d by %d pixels (%d total)." % (size[0], size[1], size[0]*size[1])

# Get the number of pixels sitting in each color
colors = im.getcolors(maxcolors=size[0]*size[1])
print "\nThere are %d unique colors in this image." % len(colors)

flatSequence = im.getdata()
print "\nWhen flattened, the image is %d pixels long." % len(flatSequence)

out = im.convert("YCbCr")
print "\nThe converted image has mode=%s" % out.mode
print "\nYCbCr for pix(400,100) is %s" % str(out.load()[400, 100])
print "\nRGB for pix(400,100) is %s" % str(im.load()[400, 100])

y,cb,cr = out.split()
#print min(list(cb.getdata())), max(list(cb.getdata()))
#print y.getextrema()
#print cb.getextrema()
#print cr.getextrema()
cb.show()
im.show()
#cr.show()
#y.show()

phi_from_YCbCr(out)

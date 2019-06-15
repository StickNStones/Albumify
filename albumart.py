import sys
from PIL import Image
from resizeimage import resizeimage


def main():
    xwidth = 0
    yheight = 0
    pixels = int(sys.argv[2])
    inputFile = sys.argv[1]

    

    with open(inputFile, 'r+b') as f:
        with Image.open(f) as image:
            print(image.size)
            xwidth = image.size[0]
            yheight = image.size[1]
            pix = image.load()
            i = 0
            r = 0
            z = 0
            k = 0
            j = 0
            colourIndex = 1

            count = 0
            sumCountx = 0
            sumCounty = 0
            sumCountz = 0

            averages = []

            while (j < (yheight/pixels)):
                k = 0
                while (k < (xwidth/pixels)):
                    i = 0
                    average = (0,0,0)
                    sumCountx = 0
                    sumCounty = 0
                    sumCountz = 0
                    count = 0
                    while (i + (j*pixels) < pixels*(j+1)):
                        r = 0
                        while (r + (k * pixels) < pixels*(k+1)):
                            if ( i + (j*pixels) < yheight) and (r + (k * pixels) < xwidth):
                                #print(pix[i + (j*pixels), r + (k * pixels)])
                                #pix[i + (j*pixels), r + (k * pixels)] = (pix[i + (j*pixels), r + (k * pixels)][0], pix[i + (j*pixels), r + (k * pixels)][2], pix[i + (j*pixels), r + (k * pixels)][1])
                                pixelLoc = i + (j*pixels), r + (k * pixels)
                                #if (colourIndex == 1):
                                #    pix[pixelLoc] = (255,255,0)
                                #    colourIndex = 0

                                count = count + 1
                                sumCountx = sumCountx + pix[pixelLoc][0]
                                sumCounty = sumCounty + pix[pixelLoc][1]
                                sumCountz = sumCountz + pix[pixelLoc][2]

                                z = z + 1
                            # print("r is =" + str(r) + " i is = " + str(i))
                            r = r + 1  
                        atuple = (sumCountx//count, sumCounty//count, sumCountz//count)
                        average = atuple
                        i = i + 1
                    print("whilei)")

                    ie = 0
                    averages.append(atuple)  
                    while (ie + (j*pixels) < pixels*(j+1)):
                        re = 0
                        while (re + (k * pixels) < pixels*(k+1)):
                            if ( ie + (j*pixels) < yheight) and (re + (k * pixels) < xwidth):
                                pix[ie + (j*pixels), re + (k * pixels)] = average
                            re = re + 1
                        ie = ie + 1
                    #if colourIndex == 1:
                    #    colourIndex = 0
                    #else:
                    #    colourIndex = 1 
                    k = k + 1
                j = j + 1
            print(z)
            print(averages)
            print(len(averages))
            image.show()
          #  result.save('out.bmp')
            
            
    

if __name__ == "__main__":
    main()

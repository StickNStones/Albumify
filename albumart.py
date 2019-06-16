import sys
from PIL import Image
from resizeimage import resizeimage
import math

def singleAverage(inputFile, pixels):
    xwidth = 0
    yheight = 0
    average = []
    with open(inputFile, 'r+b') as f:
        with Image.open(f) as image:
          #  print(image.size)
            xwidth = image.size[0]
            yheight = image.size[1]
            pix = image.load()
            i = 0
            r = 0

            average = (0,0,0)
            sumCountx = 0
            sumCounty = 0
            sumCountz = 0
            count = 0

            while i < xwidth:
                r = 0 
                while r < yheight:
                    #print(pix[i,r])
                    sumCountx = sumCountx + pix[i,r][0]
                    sumCounty = sumCounty + pix[i,r][1]
                    sumCountz = sumCountz + pix[i,r][2]
                    count = count + 1

                    r = r + 1
                i = i + 1
            average = (sumCountx//count, sumCounty//count, sumCountz//count)


    return average


def listAverages(image, pixels):
    xwidth = 0
    yheight = 0

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
#   print(averages)
#  print(len(averages))



    image.show()
    #  result.save('out.bmp')
    return averages


def main():
    pixels = int(sys.argv[2])
    inputFile = sys.argv[1]
    
    artFile1 = open("lordemelodrama.jpg", 'r+b')
    artFileImage1 = Image.open(artFile1)
    artFileImage1 = resizeimage.resize_cover(artFileImage1, [1152,1152])
    artFileImage1.show()

    artFile2 = open("Cover.jpg", 'r+b')
    artFileImage2 = Image.open(artFile2)
    artFileImage2 = resizeimage.resize_cover(artFileImage2, [184,184])

    artFile3 = open("anti.jpg", 'r+b')
    artFileImage3 = Image.open(artFile3)
    artFileImage3 = resizeimage.resize_cover(artFileImage3, [184,184])

    averageDict = {}

    # The final
    # currently hard code the size of image you want result to be. 
    # Note the end pixel sizes will need to reflect the size
    # 
    result = Image.new('RGB', (1152, 1152))

    with open(inputFile, 'r+b') as f:
        with Image.open(f) as image:
            averagesMainImage = listAverages(artFileImage1, pixels)           
            print(len(averagesMainImage))
            averageDict[inputFile] = [(singleAverage(inputFile, pixels)), image]
            averageDict["Cover.jpg"] = [(singleAverage("Cover.jpg", pixels)), artFileImage2]
            averageDict["anti.jpg"] = [(singleAverage("anti.jpg", pixels)), artFileImage3]


            xwidth, yheight = image.size
            newArray = [xwidth]
            # @@@@ THIS IS ONLY CUZS THE NEW SIZE> MAKE STUFF DYNAMIC 
            xwidth = 1152

            # sqrt(255^2 * 3) which is max distance should always be less than 1000
            minDist = 1000
            minName = None
            i = 0
            while i < len(averagesMainImage):
               # print(averagesMainImage[i])

                r = 0
                minDist = 1000
                #while r < len(averageDict):
                for key, value in averageDict.items():
                    distance = math.sqrt((value[0][0]-averagesMainImage[i][0])**2 + (value[0][1]-averagesMainImage[i][1])**2 + (value[0][2]-averagesMainImage[i][2])**2)

                    if distance < minDist:
                        minDist = distance
                        print("distance is " + str(distance), key)
                        minName = key


                    r = r + 1
                xbox, ybox = divmod(i, xwidth//pixels)
                print(ybox, xbox)
                
                result.paste(im=resizeimage.resize_cover(averageDict.get(minName)[1], [pixels,pixels]), box=(xbox*pixels,ybox*pixels))
                


                i = i + 1
        result.show()

    artFile1.close()
    artFile2.close()
            
    

if __name__ == "__main__":
    main()

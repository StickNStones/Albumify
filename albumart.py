import sys
from PIL import Image
from resizeimage import resizeimage
import math
import urllib.request
import musicbrainzngs

def singleAverage(inputFile, pixels):
    xwidth = 0
    yheight = 0
    average = []
    with open(inputFile, 'r+b') as f:
        with Image.open(f) as image:

            # artFileImage3 = resizeimage.resize_cover(artFileImage3, [184,184])

            image = resizeimage.resize_cover(image, [184,184])
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
                    try:
                        sumCountx = sumCountx + pix[i,r][0]
                        sumCounty = sumCounty + pix[i,r][1]
                        sumCountz = sumCountz + pix[i,r][2]
                        count = count + 1
                    except:
                        return (-1,-1,-1)

                    r = r + 1
                i = i + 1
            average = (sumCountx//count, sumCounty//count, sumCountz//count)

    return average

def pixelAverage(image):
    xwidth = 0
    yheight = 0
    average = []

    image = resizeimage.resize_cover(image, [184,184])
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
            try:
                sumCountx = sumCountx + pix[i,r][0]
                sumCounty = sumCounty + pix[i,r][1]
                sumCountz = sumCountz + pix[i,r][2]
                count = count + 1
            except:
                return (-1,-1,-1)

            r = r + 1
        i = i + 1
    average = (sumCountx//count, sumCounty//count, sumCountz//count)

    return average

def musicBrainz(artistName, aDict):
    musicbrainzngs.set_useragent(123, 123, contact=None)
    someID = musicbrainzngs.search_artists(artistName).get('artist-list')[0].get('id')
    allTapes = musicbrainzngs.get_artist_by_id(someID, 'release-groups').get('artist').get('release-group-list')

    for key in allTapes:
        if key.get('secondary-type-list') is None:
            image = Image.open(urllib.request.urlopen(musicbrainzngs.get_release_group_image_list(key.get('id')).get('images')[0].get('thumbnails').get('small')))
            albumName = key.get('title')
            aDict[albumName] = [pixelAverage(image), image]


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
    

    # Top one is the drawn image
    #artFile1 = open(inputFile, 'r+b')
    #artFileImage1 = Image.open(artFile1)
    #artFileImage1 = resizeimage.resize_cover(artFileImage1, [1152,1152])
    #artFileImage1.show()

    averageDict = {}

    # The final
    # currently hard code the size of image you want result to be. 
    # Note the end pixel sizes will need to reflect the size
    # 
   # result = Image.new('RGB', (1152, 1152))

    with open(inputFile, 'r+b') as f:
        with Image.open(f) as image:
            xwidth, yheight = image.size
            result = Image.new('RGB', (xwidth, xwidth))
            image = resizeimage.resize_cover(image, [xwidth,xwidth])

            print(len(sys.argv))
            i = 3
            while i < len(sys.argv):
                averagesMainImage = listAverages(image, pixels)
                musicBrainz(sys.argv[i], averageDict)
                i = i + 1

            for key in list(averageDict):
                if (averageDict.get(key)[0][0] == -1):
                    averageDict.pop(key)

            # @@@@ THIS IS ONLY CUZS THE NEW SIZE> MAKE STUFF DYNAMIC 

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
                    if (value[0][0] != -1):
                        distance = math.sqrt((value[0][0]-averagesMainImage[i][0])**2 + (value[0][1]-averagesMainImage[i][1])**2 + (value[0][2]-averagesMainImage[i][2])**2)

                    if distance < minDist:
                        minDist = distance
                        #print("distance is " + str(distance), key)
                        minName = key

                    r = r + 1

                xbox, ybox = divmod(i, xwidth//pixels)
               # print(ybox, xbox)
                
                result.paste(im=resizeimage.resize_cover(averageDict.get(minName)[1], [pixels,pixels]), box=(xbox*pixels,ybox*pixels))

                i = i + 1
            result.show()
            
    

if __name__ == "__main__":
    main()

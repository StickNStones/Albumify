import sys
from PIL import Image
from resizeimage import resizeimage
import math
import urllib.request
import musicbrainzngs
from functools import reduce

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

  #  print(allTapes)

    for key in allTapes:
        if key.get('secondary-type-list') is None:
            try:
                image = Image.open(urllib.request.urlopen(musicbrainzngs.get_release_group_image_list(key.get('id')).get('images')[0].get('thumbnails').get('small')))
                albumName = key.get('title')
                aDict[albumName] = [pixelAverage(image), image]
            except:
                pass
        
        elif key.get('secondary-type-list')[0] == 'Compilation':
          #  print(key.get('secondary-type-list')[0])
            try:
                image = Image.open(urllib.request.urlopen(musicbrainzngs.get_release_group_image_list(key.get('id')).get('images')[0].get('thumbnails').get('small')))
                albumName = key.get('title')
                aDict[albumName] = [pixelAverage(image), image]
            except:
                pass


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
            k = k + 1
        j = j + 1
    print(z)

    image.show()
    #  result.save('out.bmp')
    return averages

def printFactors(num):
    step = 2 if num % 2 else 1
    vals = []
    for i in range(1, int(math.sqrt(num))+1, step):
        if num % i == 0:
            vals.append(i)
            print(i, end=" ")
    i = len(vals)-1
    while i > 0:
        print(num//vals[i], end=" ")
        i = i - 1
        
    
    



def main():
    #pixels = int(sys.argv[2])
    inputFile = sys.argv[1]

    averageDict = {}

    print("Enter artist names to use their album art as pixels!")
    inputString = []
    while len(inputString) == 0 or inputString[-1] != "":
        inputString.append(input())

    with open(inputFile, 'r+b') as f:
        with Image.open(f) as image:
            xwidth, yheight = image.size
            side = min(xwidth,yheight)
            print("Optional pixel sizes:")
            printFactors(side)
            pixels = int(input("\nWhat size of pixel do you want to use? ")) 

            result = Image.new('RGB', (side, side))
            image = resizeimage.resize_cover(image, [side,side])

            print(len(sys.argv))
            averagesMainImage = listAverages(image, pixels)

            for item in inputString:
                musicBrainz(item, averageDict)
                i = i + 1

            for key in list(averageDict):
                if (averageDict.get(key)[0][0] == -1):
                    averageDict.pop(key)

            # sqrt(255^2 * 3) which is max distance should always be less than 1000
            minDist = 10000
            minName = None
            i = 0
            while i < len(averagesMainImage):

                r = 0
                minDist = 1000
                for key, value in averageDict.items():
                    if (value[0][0] != -1):
                        distance = math.sqrt((value[0][0]-averagesMainImage[i][0])**2 + (value[0][1]-averagesMainImage[i][1])**2 + (value[0][2]-averagesMainImage[i][2])**2)

                    if distance < minDist:
                        minDist = distance
                        #print("distance is " + str(distance), key)
                        minName = key

                    r = r + 1

                xbox, ybox = divmod(i, side//pixels)
                
                result.paste(im=resizeimage.resize_cover(averageDict.get(minName)[1], [pixels,pixels]), box=(xbox*pixels,ybox*pixels))

                i = i + 1
            result.show()
            
    

if __name__ == "__main__":
    main()

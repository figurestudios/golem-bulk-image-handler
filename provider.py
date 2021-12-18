from PIL import Image
from PIL import ImageFilter
import py7zr
import time
im = Image.open("/golem/input/input.jpg")

def rotate(num):
    processedImages = 0
    orientations = [Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]
    while (num > processedImages):
        for i in range(0, len(orientations)):
            out = im.transpose(orientations[i])
            out.save("/golem/input/output/rotation/rotation"+str(processedImages)+"."+"JPEG", "JPEG")
            processedImages += 1

def addfilter(num):
    processedImages = 0
    filters = [ImageFilter.BLUR, ImageFilter.CONTOUR, ImageFilter.DETAIL, ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE, ImageFilter.EMBOSS, ImageFilter.FIND_EDGES, ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE]
    while (num > processedImages):
        for i in range(0, len(filters)):
            out = im.filter(filters[i])
            out.save("/golem/input/output/filter/filter"+str(processedImages)+"."+"JPEG", "JPEG")
            processedImages += 1

def resize(num):
    processedImages = 0
    sizes = [[32, 32], [64, 64], [128, 128], [256, 256], [512, 512], [1024, 1024], [2048, 2048], [4096, 4096]]
    ratios = [0.25, 0.5, 1.5, 2, 3, 4, 5, 7.5, 10]
    while (num > processedImages):
        for i in range(0, len(sizes)):
            out = im.resize((sizes[i][0],sizes[i][1]), Image.ANTIALIAS)
            out.save("/golem/input/output/resize/square"+str(processedImages)+"."+"JPEG", "JPEG")
            processedImages += 1
        for i in range(0, len(sizes)):
            out = im.resize((int(ratios[i]*im.size[0]),int(ratios[i]*im.size[1])), Image.ANTIALIAS)
            out.save("/golem/input/output/resize/ratio"+str(processedImages)+"."+"JPEG", "JPEG")
            processedImages += 1

def zip():
    with py7zr.SevenZipFile('/golem/input/target.7z', 'w') as archive:
        archive.writeall('/golem/input/output/', 'base')

addfilter(1)
rotate(1)
resize(1)
zip()
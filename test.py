from PIL import Image
def mains(readthis, readthis2, saveas):
    img1 = Image.open(readthis2).convert("RGBA")
    img2 = Image.open(readthis)
    '''
    baseheight = 219
    hpercent = (baseheight / float(img1.size[1]))
    wsize = int((float(img1.size[0]) * float(hpercent)))
    img1 = img1.resize((wsize, baseheight), Image.ANTIALIAS)
    '''
    '''
    num1 = numpy.array(img1)
    num2 = numpy.array(img2)
    num2 = num2[:,:512, :]

    num3 = num2 + num1

    for x in range(219):
        for y in range(511):
            if num2[x][y][0] == 0 and num2[x][y][1] == 0 and num2[x][y][2] == 0:
                num3 = num1
            else:
                num3 = num2
    '''
    img1.paste(img2, (0, 0), img2)
    img1.save(saveas)
    # img1.show()

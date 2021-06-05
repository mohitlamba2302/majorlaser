import cv2
from PIL import Image, ImageEnhance

'''
def __init__(self):
    self.numDownSamples = 1
    self.numBilateralFilters = 7
'''

numDownSamples = 2
numBilateralFilters = 10

def render(img_rgb):

    # downsample image using Gaussian pyramid
    img_color = img_rgb
    for _ in range(numDownSamples):
        img_color = cv2.pyrDown(img_color)
    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
    # upsample image to original size
    for _ in range(numDownSamples):
        img_color = cv2.pyrUp(img_color)
    # convert to grayscale and apply bilateral blur
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    for _ in range(numBilateralFilters):
        img_gray_blur = cv2.bilateralFilter(img_gray, 9, 9, 7)
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(img_gray_blur, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 9, 5)
    # convert back to color so that it can be bit-ANDed with color image
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    #Ensure that img_color and img_edge are the same size, otherwise bitwise_and will not work
    height = min(len(img_color), len(img_edge))
    width = min(len(img_color[0]), len(img_edge[0]))
    img_color = img_color[0:height, 0:width]
    img_edge = img_edge[0:height, 0:width]
    return cv2.bitwise_and(img_color, img_edge)


def mains(readas, saveas):
    img = cv2.imread(readas)
    img2 = render(img)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img2 = cv2.convertScaleAbs(img2, alpha = 0.7, beta=1)

    img2_pil = Image.fromarray(img2)
    img2_en = ImageEnhance.Contrast(img2_pil)
    img2_en = img2_en.enhance(2)

    img2_en.save(saveas)
    #cv2.imwrite("Cartoon_test8.png", img2_pil)

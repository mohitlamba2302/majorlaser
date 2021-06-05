import cv2
import os.path
def main():
    save_path = "/folder"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pth = dir_path + save_path
    vidcap = cv2.VideoCapture('SampleVideo.mp4')
    success, image = vidcap.read()
    count = 0
    while success:
        os.chdir(pth)
        cv2.imwrite("%d.jpg" % count, image)     # save frame as JPEG file
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
    return count

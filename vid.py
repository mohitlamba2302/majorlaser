import cv2
import os
import natsort

image_folder = 'result'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
# print(os.listdir(image_folder))
# print(images)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, 0, 40, (width, height))
print(images)
# images = sorted(images)
images = natsort.natsorted(images)
# images.sort(key=lambda f: int(filter(str.isdigit, f)))
# print(images)
for image in images:
    # print(image)
    video.write(cv2.imread(os.path.join(image_folder, image)))
cv2.destroyAllWindows()
video.release()

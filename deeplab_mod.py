import os
from io import BytesIO
import tarfile
import tempfile
from six.moves import urllib

from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import file1
import tensorflow as tf
import toon
import test
from im_txt2 import im_txt

class DeepLabModel(object):
  """Class to load deeplab model and run inference."""
  INPUT_TENSOR_NAME = 'ImageTensor:0'
  OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
  INPUT_SIZE = 513
  FROZEN_GRAPH_NAME = 'frozen_inference_graph'

  def __init__(self, tarball_path):
    """Creates and loads pretrained deeplab model."""
    self.graph = tf.Graph()

    graph_def = None
    # Extract frozen graph from tar archive.
    tar_file = tarfile.open(tarball_path)
    for tar_info in tar_file.getmembers():
      if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
        file_handle = tar_file.extractfile(tar_info)
        graph_def = tf.GraphDef.FromString(file_handle.read())
        break

    tar_file.close()

    if graph_def is None:
      raise RuntimeError('Cannot find inference graph in tar archive.')

    with self.graph.as_default():
      tf.import_graph_def(graph_def, name='')

    self.sess = tf.Session(graph=self.graph)

  def run(self, image):
    """Runs inference on a single image.

    Args:
      image: A PIL.Image object, raw input image.

    Returns:
      resized_image: RGB image resized from original input image.
      seg_map: Segmentation map of `resized_image`.
    """
    width, height = image.size
    resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
    resize_ratio = 1
    target_size = (int(resize_ratio * width), int(resize_ratio * height))
    resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
    batch_seg_map = self.sess.run(
        self.OUTPUT_TENSOR_NAME,
        feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
    seg_map = batch_seg_map[0]
    return resized_image, seg_map


def create_pascal_label_colormap():
  """Creates a label colormap used in PASCAL VOC segmentation benchmark.

  Returns:
    A Colormap for visualizing segmentation results.
  """
  colormap = np.zeros((256, 3), dtype=int)
  ind = np.arange(256, dtype=int)

  for shift in reversed(range(8)):
    for channel in range(3):
      colormap[:, channel] |= ((ind >> channel) & 1) << shift
    ind >>= 3

  return colormap


def label_to_color_image(label):
  """Adds color defined by the dataset colormap to the label.

  Args:
    label: A 2D array with integer type, storing the segmentation label.

  Returns:
    result: A 2D array with floating type. The element of the array
      is the color indexed by the corresponding element in the input label
      to the PASCAL color map.

  Raises:
    ValueError: If label is not of rank 2 or its value is larger than color
      map maximum entry.
  """
  if label.ndim != 2:
    raise ValueError('Expect 2-D input label')

  colormap = create_pascal_label_colormap()

  if np.max(label) >= len(colormap):
    raise ValueError('label value too large.')

  return colormap[label]


def vis_segmentation(image, seg_map, count):

  """Visualizes input image, segmentation map and overlay view."""
  plt.figure(figsize=(15, 5))
  grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

  plt.subplot(grid_spec[0])
  # plt.imshow(image)
  plt.axis('off')
  plt.title('input image')

  plt.subplot(grid_spec[1])
  seg_image = label_to_color_image(seg_map).astype(np.uint8)

  #start
  # height, width = seg_image.size()
  loc = []
  # pixel_col = seg_image.load()
  pixel_col = seg_image

  # print(pixel_col[128, 267][0])

  height = np.shape(pixel_col)[0]
  width = np.shape(pixel_col)[1]

  print(np.shape(pixel_col))
  print("Height: ", height)
  print("Width: ", width)
  j = 0
  for x in range(height):
      for y in range(width):
            if pixel_col[x][y][0] == 192 and pixel_col[x][y][1] == 128 and pixel_col[x][y][2] == 128:
                loc.append([x, y])
                j = j + 1

  # print(loc)
  color_seg = np.zeros([height, width, 4], dtype = int)
  i = 0
  pix = np.array(image)
  '''
  print(pix.shape)
  print(color_seg.shape)
  '''
  for x in range(height):
      for y in range(width):
          if [x, y] in loc:
              color_seg[x][y][0] = pix[x][y][0]
              color_seg[x][y][1] = pix[x][y][1]
              color_seg[x][y][2] = pix[x][y][2]
              color_seg[x][y][3] = 255
              i = i + 1
          else:
              color_seg[x][y][0] = 255
              color_seg[x][y][1] = 255
              color_seg[x][y][2] = 255
  '''

  print("i: ", i)
  print("j: ", j)
  print("X: ", x)
  print("Y: ", y)
  '''

  # plt.imshow(color_seg, interpolation='nearest')
  x = str(count)
  x = x + '.png'
  plt.imsave("C:/Users/VAIBHAV/Downloads/majorlaser/deeplab/subject/" + x, color_seg)

  # plt.imshow(color_seg)
  #end

  #plt.imshow(seg_image)
  # plt.imshow(color_seg)
  plt.axis('off')
  plt.title('segmentation map')

  plt.subplot(grid_spec[2])
  # plt.imshow(image)
  # plt.imshow(seg_image, alpha=0.7)
  plt.axis('off')
  plt.title('segmentation overlay')

  unique_labels = np.unique(seg_map)
  ax = plt.subplot(grid_spec[3])
    # plt.imshow(
    #   FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
  ax.yaxis.tick_right()
  plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
  plt.xticks([], [])
  ax.tick_params(width=0.0)
  plt.grid('off')
  # plt.show()


LABEL_NAMES = np.asarray([
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
    'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
])

FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)


# In[4]:


#@title Select and download models {display-mode: "form"}

MODEL_NAME = 'mobilenetv2_coco_voctrainaug'  # @param ['mobilenetv2_coco_voctrainaug', 'mobilenetv2_coco_voctrainval', 'xception_coco_voctrainaug', 'xception_coco_voctrainval']

_DOWNLOAD_URL_PREFIX = 'http://download.tensorflow.org/models/'
_MODEL_URLS = {
    'mobilenetv2_coco_voctrainaug':
        'deeplabv3_mnv2_pascal_train_aug_2018_01_29.tar.gz',
    'mobilenetv2_coco_voctrainval':
        'deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz',
    'xception_coco_voctrainaug':
        'deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval':
        'deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}
_TARBALL_NAME = 'deeplab_model.tar.gz'

model_dir = tempfile.mkdtemp()
tf.gfile.MakeDirs(model_dir)

download_path = os.path.join(model_dir, _TARBALL_NAME)
print('downloading model, this might take a while...')
urllib.request.urlretrieve(_DOWNLOAD_URL_PREFIX + _MODEL_URLS[MODEL_NAME],
                   download_path)
print('download completed! loading DeepLab model...')

MODEL = DeepLabModel(download_path)
print('model loaded successfully!')


# ## Run on sample images
#
# Select one of sample images (leave `IMAGE_URL` empty) or feed any internet image
# url for inference.
#
# Note that we are using single scale inference in the demo for fast computation,
# so the results may slightly differ from the visualizations in
# [README](https://github.com/tensorflow/models/blob/master/research/deeplab/README.md),
# which uses multi-scale and left-right flipped inputs.

# In[9]:


#@title Run on sample images {display-mode: "form"}

SAMPLE_IMAGE = 'image1'  # @param ['image1', 'image2', 'image3']
IMAGE_URL = 'http://www3.pictures.zimbio.com/fp/Alexandra+Daddario+Alexandra+Daddario+Set+vG6YfzknEkrl.jpg'  #@param {type:"string"}
#IMAGE_URL = 'https://cdn.soccerladuma.co.za/cms2/image_manager/uploads/News/278367/7/1504001501_eece3.jpg'



def run_visualization(openthis):
  original_im = ""
  try:
    original_im = Image.open(openthis)
  except IOError:
    print('Cannot retrieve image')

  print('running deeplab on image...')
  resized_im, seg_map = MODEL.run(original_im)
  vis_segmentation(resized_im, seg_map, i)



countx = file1.main()

print(countx)
for i in range(countx):
    print("in the loop")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    '''
    saveas = dir_path + "/toon/" + str(i) + ".png"
    subject = dir_path + "/subject/" + str(i) + ".png"
    y = dir_path + "/folder/" + str(i) + ".jpg"
    savefinal = dir_path + "/result/" + str(i) + ".png"
    '''
    saveas = 'C:/Users/VAIBHAV/Downloads/majorlaser/deeplab/toon/' + str(i) + ".png"
    subject = 'C:/Users/VAIBHAV/Downloads/majorlaser/deeplab/subject/'+str(i) + ".png"
    y = 'C:/Users/VAIBHAV/Downloads/majorlaser/deeplab/folder/'+ str(i) + ".jpg"
    savefinal = 'C:/Users/VAIBHAV/Downloads/majorlaser/deeplab/result/' + str(i) + ".png"
    run_visualization(y)
    toon.mains(y, saveas)
    test.mains(subject, saveas, savefinal)

    if i == 1 or i % 24 == 0:
        im_txt("Result\\" + i + ".png")

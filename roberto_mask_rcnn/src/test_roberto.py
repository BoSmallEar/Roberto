# In[1]:

import os
import sys
import random
import math
import re
import time
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
import pdb
from PIL import Image
# Root directory of the project
ROOT_DIR = os.path.abspath("../")
# Root directory of the dataset
DATA_DIR = '../images/trash_test/'
DATA_NUM = 40 

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log

# get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


# ## Configurations

# In[2]:


class TrashConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "objects"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 32

    # Number of classes (including background)
    NUM_CLASSES = 1 + 2  # background + 3 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_MIN_DIM = 256
    IMAGE_MAX_DIM = 256

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 32

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 100

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 5
    
config = TrashConfig()
config.display()


# ## Notebook Preferences

# In[3]:


def get_ax(rows=1, cols=1, size=8):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Change the default size attribute to control the size
    of rendered images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

# In[4]:
    
# ## preprocess the ground truth label
'''
file_clothes = open(DATA_DIR+'clothes.txt','r')
data_clothes = []
for i in range(DATA_NUM):
    data_clothes.append([int(j) for j in file_clothes.readline().split()])

file_paperball = open(DATA_DIR+'paperball.txt','r')
data_paperball = []
for i in range(DATA_NUM):
    data_paperball.append([int(j) for j in file_paperball.readline().split()])
'''

data_clothes = []
for i in range(DATA_NUM):
    data_clothes.append([0, 0, 0, 0])

data_paperball = []
for i in range(DATA_NUM):
    data_paperball.append([0, 0, 0, 0])
    
# ## Dataset
# 
# Create a synthetic dataset
# 
# Extend the Dataset class and add a method to load the shapes dataset, `load_objects()`, and override the following methods:
# 
# * load_image()
# * load_mask()
# * image_reference()

# In[4]:

class TrashDataset(utils.Dataset):
    """Generates the shapes synthetic dataset. The dataset consists of simple
    shapes (triangles, squares, circles) placed randomly on a blank surface.
    The images are generated on the fly. No file access required.
    """

    def load_objects(self, start, end, height, width):
        """Generate the requested number of synthetic images.
        count: number of images to generate.
        height, width: the size of the generated images.
        """
        # Add classes
        self.add_class("objects", 1, "clothes")
        self.add_class("objects", 2, "paperball")

        # Add images
        # Generate random specifications of images (i.e. color and
        # list of shapes sizes and locations). This is more compact than
        # actual images. Images are generated on the fly in load_image().
        
        for i in range(start,end):
            objects = []
            data_clothes_line = data_clothes[i]
            data_paperball_line = data_paperball[i]
            for k in range(len(data_clothes_line)//4):
                objects.append(('clothes', tuple(data_clothes_line[4*k:4*(k+1)])))
            for k in range(len(data_paperball_line)//4):
                objects.append(('paperball', tuple(data_paperball_line[4*k:4*(k+1)])))    
      
            # bg_color, shapes = self.random_image(height, width)
            self.add_image("objects", image_id=i, path=DATA_DIR + str(i) + '.png',
                           width=width, height=height, objects=objects)

    def load_image(self, image_id):
        assert image_id < len(self.image_info)
        image_path = self.image_info[image_id]['path']
        image = Image.open(image_path)
        return np.array(image)

    def image_reference(self, image_id):
        """Return the shapes data of the image."""
        info = self.image_info[image_id]
        if info["source"] == "shapes":
            return info["shapes"]
        else:
            super(self.__class__).image_reference(self, image_id)

    def load_mask(self, image_id):
        """Generate instance masks for shapes of the given image ID.
        """
        info = self.image_info[image_id]
        objects = info['objects']
        count = len(objects)

        mask = np.zeros([info['height'], info['width'], count], dtype=np.uint8)
        for i, (shape, pos) in enumerate(info['objects']):
            x1,y1,width,height = pos
            mask[y1:y1+height, x1:x1+width, i] = 1
        # Handle occlusions
        # occlusion = np.logical_not(mask[:, :, -1]).astype(np.uint8)
        # for i in range(count-2, -1, -1):
            # mask[:, :, i] = mask[:, :, i] * occlusion
            # occlusion = np.logical_and(occlusion, np.logical_not(mask[:, :, i]))
        # Map class names to class IDs.
        class_ids = np.array([self.class_names.index(s[0]) for s in objects])
        return mask.astype(np.bool), class_ids.astype(np.int32)

    def draw_shape(self, image, shape, dims, color):
        """Draws a shape from the given specs."""
        # Get the center x, y and the size s
        x, y, s = dims
        if shape == 'square':
            cv2.rectangle(image, (x-s, y-s), (x+s, y+s), color, -1)
        elif shape == "circle":
            cv2.circle(image, (x, y), s, color, -1)
        elif shape == "triangle":
            points = np.array([[(x, y-s),
                                (x-s/math.sin(math.radians(60)), y+s),
                                (x+s/math.sin(math.radians(60)), y+s),
                                ]], dtype=np.int32)
            cv2.fillPoly(image, points, color)
        return image

    def random_shape(self, height, width):
        """Generates specifications of a random shape that lies within
        the given height and width boundaries.
        Returns a tuple of three valus:
        * The shape name (square, circle, ...)
        * Shape color: a tuple of 3 values, RGB.
        * Shape dimensions: A tuple of values that define the shape size
                            and location. Differs per shape type.
        """
        # Shape
        shape = random.choice(["square", "circle", "triangle"])
        # Color
        color = tuple([random.randint(0, 255) for _ in range(3)])
        # Center x, y
        buffer = 20
        y = random.randint(buffer, height - buffer - 1)
        x = random.randint(buffer, width - buffer - 1)
        # Size
        s = random.randint(buffer, height//4)
        return shape, color, (x, y, s)

    def random_image(self, height, width):
        """Creates random specifications of an image with multiple shapes.
        Returns the background color of the image and a list of shape
        specifications that can be used to draw the image.
        """
        # Pick random background color
        bg_color = np.array([random.randint(0, 255) for _ in range(3)])
        # Generate a few random shapes and record their
        # bounding boxes
        shapes = []
        boxes = []
        N = random.randint(1, 4)
        for _ in range(N):
            shape, color, dims = self.random_shape(height, width)
            shapes.append((shape, color, dims))
            x, y, s = dims
            boxes.append([y-s, x-s, y+s, x+s])
        # Apply non-max suppression wit 0.3 threshold to avoid
        # shapes covering each other
        keep_ixs = utils.non_max_suppression(np.array(boxes), np.arange(N), 0.3)
        shapes = [s for i, s in enumerate(shapes) if i in keep_ixs]
        return bg_color, shapes


# In[5]:
# Test dataset
dataset_test = TrashDataset()
dataset_test.load_objects(0, DATA_NUM, config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1])
dataset_test.prepare()

# ## Detection

# In[11]:
class InferenceConfig(TrashConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 32

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)

model_path = model.find_last()

# Load trained weights
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)


# In[12]:
for pos_ids in range(5):
    # Test on random images
    original_images = []
    image_ids = range(8)
    for image_id in image_ids:
        original_image, image_meta, gt_class_id, gt_bbox, gt_mask =    modellib.load_image_gt(dataset_test, inference_config, 
                                   image_id+pos_ids*8, use_mini_mask=False)
        
        for j in range(4):
            original_images.append(original_image)
        
        '''
        log("original_image", original_image)
        log("image_meta", image_meta)
        log("gt_class_id", gt_class_id)
        log("gt_bbox", gt_bbox)
        log("gt_mask", gt_mask)
        
        
        visualize.display_instances(original_image, gt_bbox, gt_mask, gt_class_id, 
                                    dataset_train.class_names, figsize=(8, 8))
        '''
    
    results = model.detect(original_images, verbose=1)
    
    for i in range(8):
        image_id = i * 4
        r = results[image_id]
        img_save_path = DATA_DIR+'pos_'+str(pos_ids)+'_'+str(i)+'_out.png'
        visualize.display_instances(original_images[image_id], r['rois'], r['masks'], r['class_ids'], 
                                    dataset_test.class_names, r['scores'], ax=get_ax(), img_save_path=img_save_path)



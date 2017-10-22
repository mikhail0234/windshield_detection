import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import glob
import cv2


def read_image(image_path):
    """Reads and returns image."""
    return mpimg.imread(image_path)

def read_image_and_print_dims(image_path):
    """Reads and returns image.
    Helper function to examine how an image is represented.
    """
    image = mpimg.imread(image_path)
    plt.imshow(image)  #call as plt.imshow(gray, cmap='gray') to show a grayscaled image
    return image

def read_images(path):
    images = []

    for imagePath in glob.glob(path+ "/*.jpg"):
        image = cv2.imread(imagePath)

        images.append(image)
        #print('This image is:', type(image), 'with dimensions:', image.shape)

    return images
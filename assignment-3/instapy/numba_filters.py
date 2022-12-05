"""numba-optimized filters"""
from numba import jit 
import numpy as np

@jit(nopython = True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Numba will generate a machine code version of this function and optimize it such that
    the runtime will be faster than usual python. With the use of the decarator "jit" then 
    the numba magic will do its thing. 

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform
    for height in range(image.shape[0]):
        for width in range(image.shape[1]):
            # The gray value to be applied for each channel
            weighted = image[height][width][0]*0.21 + image[height][width][1]*0.72 + image[height][width][2]*0.07
            gray_image[height][width][0] = weighted 
            gray_image[height][width][1] = weighted
            gray_image[height][width][2] = weighted
    grayscale_image = gray_image.astype("uint8") 
    return grayscale_image

@jit(nopython = True)
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Matrix used for representing the color values for each respective channel
    sepia_matrix = [[ 0.393 , 0.769 , 0.189], # red
                    [ 0.349 , 0.686 , 0.168], # green
                    [ 0.272 , 0.534 , 0.131]] # blue
    # Iterate through the pixels
    for height in range(sepia_image.shape[0]):
        for width in range(sepia_image.shape[1]):
            # get each channel
            red_channel = image[height][width][0]
            green_channel = image[height][width][1]
            blue_channel = image[height][width][2]
            # apply weigth to each channel
            red = red_channel*sepia_matrix[0][0] + green_channel*sepia_matrix[0][1] + blue_channel*sepia_matrix[0][2]
            green = red_channel*sepia_matrix[1][0] + green_channel*sepia_matrix[1][1] + blue_channel*sepia_matrix[1][2]
            blue = red_channel*sepia_matrix[2][0] + green_channel*sepia_matrix[2][1] + blue_channel*sepia_matrix[2][2]
            # Assign the correct pixel values for the sepia_image. Important to assure for overflow by using min()
            sepia_image[height][width][0] = min(255,red)
            sepia_image[height][width][1] = min(255, green)
            sepia_image[height][width][2] = min(255, blue)
    # Return image
    # don't forget to make sure it's the right type!
    sepia_image = sepia_image.astype("uint8")
    return sepia_image
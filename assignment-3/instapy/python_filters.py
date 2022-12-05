"""pure Python implementation of image filters"""

from itertools import count
import numpy as np

def python_color2gray(image: np.array) -> np.array:
    """
    Convert rgb pixel array to grayscale
    
    We got to iterate through the shape of the gray_image which represents the dimension of the array in order 
    to iterate through all the pixels of the array. Furthermore, get the gray value from the sum of the weighted 
    value to each channel respectively and apply that gray value to each pixel. 

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform
    for height in range(image.shape[0]):
        for width in range(image.shape[1]):
            # The gray value
            weighted = image[height][width][0]*0.21 + image[height][width][1]*0.72 + image[height][width][2]*0.07
            # Apply to each channel
            gray_image[height][width][0] = weighted 
            gray_image[height][width][1] = weighted
            gray_image[height][width][2] = weighted
    grayscale_image = gray_image.astype("uint8") 
    return grayscale_image


def python_color2sepia(image: np.array) -> np.array:
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
            # get channels which is the arrays of R,G,B
            red_channel = image[height][width][0] 
            green_channel = image[height][width][1]
            blue_channel = image[height][width][2]
            # apply weight to each channel
            red = red_channel*sepia_matrix[0][0] + green_channel*sepia_matrix[0][1] + blue_channel*sepia_matrix[0][2]
            green = red_channel*sepia_matrix[1][0] + green_channel*sepia_matrix[1][1] + blue_channel*sepia_matrix[1][2]
            blue = red_channel*sepia_matrix[2][0] + green_channel*sepia_matrix[2][1] + blue_channel*sepia_matrix[2][2]
            # Assign the correct pixel values for the sepia_image Important to assure for overflow by using min()
            sepia_image[height][width][0] = min(255,red)
            sepia_image[height][width][1] = min(255, green)
            sepia_image[height][width][2] = min(255, blue)
    # Return image
    # don't forget to make sure it's the right type!
    sepia_image = sepia_image.astype("uint8")
    return sepia_image

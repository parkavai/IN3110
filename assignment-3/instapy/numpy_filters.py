"""numpy implementation of image filters"""

from typing import Optional
import numpy as np

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)

    # Hint: use numpy slicing in order to have fast vectorized code
    gray_image = image[:, :, 0]*0.21 + image[:, :, 1]*0.72 + image[:, :, 2]*0.07
    grayscale_image = gray_image.astype("uint8")
    # Return image (make sure it's the right type!)
    return grayscale_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    # Matrix used for representing the color values for each respective channel
    sepia_matrix = [[ 0.393 , 0.769 , 0.189], # red
                    [ 0.349 , 0.686 , 0.168], # green
                    [ 0.272 , 0.534 , 0.131]] # blue

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter
    sepia_image = np.empty_like(image)

    # get channels which is the arrays of R,G,B
    red_channel = image[:,:,0] # red
    green_channel = image[:,:,1] # green 
    blue_channel = image[:,:,2] # blue

    # apply weight to each channel
    red = red_channel*sepia_matrix[0][0] + green_channel*sepia_matrix[0][1] + blue_channel*sepia_matrix[0][2]
    green = red_channel*sepia_matrix[1][0] + green_channel*sepia_matrix[1][1] + blue_channel*sepia_matrix[1][2]
    blue = red_channel*sepia_matrix[2][0] + green_channel*sepia_matrix[2][1] + blue_channel*sepia_matrix[2][2]

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255.
    # With the use of "np.where", we can search through an entire array and change the display values wether it is bigger 
    # than 255 or not. 
    red = np.where(red > 255, 255, red)
    green = np.where(green > 255, 255, green)
    blue = np.where(blue > 255, 255, blue)

    # Assign the correct pixel values for the sepia_image
    sepia_image[:,:,0] = red
    sepia_image[:,:,1] = green
    sepia_image[:,:,2] = blue

    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8")
    return sepia_image

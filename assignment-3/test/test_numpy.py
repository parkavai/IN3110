from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
import random 
import numpy as np


def test_color2gray(image, reference_gray):
    test_image = numpy_color2gray(image)
    # check that the result has the right shape, type
    assert test_image.shape[0] == reference_gray.shape[0]
    assert test_image.shape[1] == reference_gray.shape[1]
    assert isinstance(test_image, np.ndarray) == True
    assert test_image.dtype == reference_gray.dtype
    # assert uniform r,g,b values
    for x in range(0, 20):
        height = random.randint(0, test_image.shape[0]-1)
        width = random.randint(0, test_image.shape[1]-1)
        weighted_sum = int((image[height][width][0] * 0.21) + (0.72 * image[height][width][1]) + (0.07 * image[height][width][2]))
        assert test_image[height, width] == weighted_sum

def test_color2sepia(image, reference_sepia):
    # run color2sepia
    test_image = numpy_color2sepia(image)
    # check that the result has the right shape, type
    assert test_image.shape[0] == reference_sepia.shape[0]
    assert test_image.shape[1] == reference_sepia.shape[1]
    assert isinstance(test_image, np.ndarray) == True
    assert type(test_image) == type(reference_sepia)
    # verify some individual pixel samples
    # according to the sepia matrix
    # Matrix used for representing the color values for each respective channel
    sepia_matrix = [[ 0.393 , 0.769 , 0.189], # red
                    [ 0.349 , 0.686 , 0.168], # green
                    [ 0.272 , 0.534 , 0.131]] # blue

    # Iterate through the pixels
    for x in range(0, 20):
        height = random.randint(0, image.shape[0]-1)
        width = random.randint(0, image.shape[1]-1)
        r_c = image[height][width][0]
        g_c = image[height][width][1]
        b_c = image[height][width][2]
        # apply weigth to each channel
        red = int(r_c*sepia_matrix[0][0] + g_c*sepia_matrix[0][1] + b_c*sepia_matrix[0][2])
        green = int(r_c*sepia_matrix[1][0] + g_c*sepia_matrix[1][1] + b_c*sepia_matrix[1][2])
        blue = int(r_c*sepia_matrix[2][0] + g_c*sepia_matrix[2][1] + b_c*sepia_matrix[2][2])
        assert test_image[height, width, 0] == min(255, red)
        assert test_image[height, width, 1] == min(255, green)
        assert test_image[height, width, 2] == min(255, blue)
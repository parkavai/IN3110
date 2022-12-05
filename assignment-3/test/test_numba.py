from instapy.numba_filters import numba_color2gray, numba_color2sepia
import numpy.testing as nt
import numpy as np


def test_color2gray(image, reference_gray):
    # run color2gray
    test_image = numba_color2gray(image)
    # check that the result has the right shape, type
    assert test_image.shape[0] == image.shape[0]
    assert test_image.shape[1] == image.shape[1]
    assert test_image.shape[2] == 3
    assert isinstance(test_image, np.ndarray) == True
    assert type(test_image) == type(reference_gray)
    # Using 'assert_allclose' to compare both arrays
    nt.assert_allclose(test_image, reference_gray)

def test_color2sepia(image, reference_sepia):
    # run color2sepia
    test_image = numba_color2sepia(image)
    # check that the result has the right shape, type
    assert test_image.shape[0] == image.shape[0]
    assert test_image.shape[1] == image.shape[1]
    assert test_image.shape[2] == 3
    assert isinstance(test_image, np.ndarray) == True
    assert type(test_image) == type(reference_sepia)
    # Using 'assert_allclose' to compare both arrays
    nt.assert_allclose(test_image, reference_sepia)

"""
Tests for our array class
"""

from socketserver import ThreadingUnixDatagramServer
from array_class import Array

# 1D tests (Task 4)

def test_str_1d():

    # Test string 
    arr_1 = Array((3,), 1,2,3)
    assert arr_1.__str__() == f"Array: {[1,2,3]}"

    arr_2 = Array((3,), True,True,False)
    assert arr_2.__str__() == f"Array: {[True,True,False]}"

    arr_3 = Array((3,), 2.3,2.1,3.3)
    assert arr_3.__str__() == f"Array: {[2.3,2.1,3.3]}"


def test_add_1d():

    # Test Boolean
    bool_arr = Array((4,), True, False, True, False)
    arr_1 = Array((4,), 1,2,3,4)
    assert bool_arr.__add__(arr_1) == NotImplemented
    assert arr_1.__add__(bool_arr) == NotImplemented

    # Test Scalar Int
    other = 10
    assert other.__add__(arr_1) == NotImplemented
    assert other + arr_1 == [11, 12, 13, 14]

    # Test Scalar Float
    other = 2.5
    float_arr = Array((2,), 1.6, 3.6)
    assert other.__add__(float_arr) == NotImplemented
    assert float_arr.__radd__(other) == [4.1, 6.1]

    # Test Array Int
    arr_2 = Array((4,), 5,6,7,8)
    arr_3 = Array((6, ), 3,2,1,5,4,6)
    assert arr_1.__add__(arr_2) == [16, 18, 20, 22]
    assert arr_1.__add__(arr_3) == NotImplemented

    # Test Array Float 
    float_arr_2 = Array((2,), 1.2, 2.0)
    assert float_arr.__add__(float_arr_2) == [5.3, 8.1]


def test_sub_1d():

    # Test Boolean
    bool_arr = Array((4,), True, False, True, False)
    arr_1 = Array((4,), 1,2,3,4)
    assert bool_arr.__sub__(arr_1) == NotImplemented
    assert arr_1.__sub__(bool_arr) == NotImplemented

    # Test Scalar Int
    other = 10
    assert other.__sub__(arr_1) == NotImplemented
    assert other - arr_1 == [-9, -8, -7, -6]

    # Test Scalar Float
    other = 2.5
    float_arr = Array((2,), 3.0, 3.6)
    assert other.__sub__(float_arr) == NotImplemented
    assert float_arr.__rsub__(other) == [0.5, 1.1]

    # Test Array Int
    arr_2 = Array((4,), 5,6,7,8)
    arr_3 = Array((6, ), 3,2,1,5,4,6)
    assert arr_1.__sub__(arr_2) == [-14, -14, -14, -14]
    assert arr_1.__sub__(arr_3) == NotImplemented

    # Test Array Float
    float_arr_2 = Array((2,), 1.2, 3.0)
    assert float_arr.__sub__(float_arr_2) == [-0.7, -1.9]

def test_mul_1d():

    # Test Boolean
    bool_arr = Array((4,), True, False, True, False)
    arr_1 = Array((4,), 1,2,3,4)
    assert bool_arr.__mul__(arr_1) == NotImplemented
    assert arr_1.__mul__(bool_arr) == NotImplemented

    # Test Scalar Int
    other = 10
    assert other.__mul__(arr_1) == NotImplemented
    assert other * arr_1 == [10, 20, 30, 40]

    # Test Scalar Float
    other = 2.5
    float_arr = Array((2,), 1.1, 3.1)
    assert other.__mul__(float_arr) == NotImplemented
    assert float_arr.__rmul__(other) == [2.75, 7.75]

    # Test Array Int
    arr_2 = Array((4,), 5,6,7,8)
    arr_3 = Array((6,), 3,2,1,5,4,6)
    assert arr_1.__mul__(arr_2) == [50, 120, 210, 320]
    assert arr_1.__mul__(arr_3) == NotImplemented

    # Test Array Float
    float_arr_2 = Array((2,), 1.2, 3.0)
    assert float_arr.__mul__(float_arr_2) == [3.3, 23.25]


def test_eq_1d():

    # Test type
    bool_arr = Array((4,), True, False, True, False)
    arr_1 = Array((4,), 1,2,3,4)
    assert arr_1.__eq__(bool_arr) == False

    # Test shape 
    arr_2 = Array((5,), 5,1,2,3,5)
    assert arr_1.__eq__(arr_2) == False 

    # Test identical
    arr_3 = Array((4,), 5,6,7,8)
    arr_4 = Array((4,), 5,6,7,8)
    assert arr_1.__eq__(arr_4) == False
    assert arr_3.__eq__(arr_4) == True 


def test_same_1d():

    # Test value
    arr_1 = Array((4,), 1,2,3,4)
    arr_2 = Array((5,), 5,1,2,3,5)
    arr_1.is_equal(arr_2)

    # Test type
    string = "test"
    assert arr_1.is_equal(string)

    # Test scalar
    arr_3 = Array((2,), 1, 1)
    other = 1
    assert arr_3.is_equal(other) == True

    # Test array
    arr_4 = Array((4,), 1,3,2,4)
    arr_5 = Array((4,), 1,2,3,4)
    assert arr_1.is_equal(arr_4) == [True, False, False, True]
    assert arr_1.is_equal(arr_5) == [True, True, True, True]   

def test_smallest_1d():
    
    # Test type
    bool_arr = Array((4,), True, False, True, False)
    assert bool_arr.min_element()

    # Test array 
    arr_1 = Array((5,), 5,1,2,3,5)
    assert arr_1.min_element() == 1


def test_mean_1d():

    # Test type
    bool_arr = Array((4,), True, False, True, False)
    assert bool_arr.mean_element()

    # Test array 
    arr_1 = Array((3,), 3,1,2)
    assert arr_1.mean_element() == 2

# 2D tests (Task 6)


def test_add_2d():

    # Test Boolean 
    bool_arr = Array((2, 2), True, True, False, False)
    arr_1 = Array((2, 2), 1,2,3,4)
    arr_2 = Array((4, 1), 5,6,7,8)
    assert bool_arr.__add__(arr_1) is NotImplemented
    assert arr_1.__add__(bool_arr) is NotImplemented
    assert arr_1.__add__(arr_2) is NotImplemented

    # Test Scalar Int
    other = 10
    assert other.__add__(arr_1) is NotImplemented
    assert other + arr_1 == [[11, 12], [13, 14]]

    # Test Scalar Float
    other = 2.5
    float_arr = Array((1,2), 1.6, 3.6)
    assert other.__add__(float_arr) is NotImplemented
    assert float_arr.__radd__(other) == [[4.1, 6.1]]

    # Test Array Int
    arr_3 = Array((2, 2), 3,2,1,5)
    assert arr_1.__add__(arr_3) == [[14, 14], [14, 19]]

    # Test Array Float 
    float_arr_2 = Array((1,2), 1.2, 2.0)
    assert float_arr.__add__(float_arr_2) == [[5.3, 8.1]]

def test_mult_2d():

    # Test Boolean 
    bool_arr = Array((2, 2), True, True, False, False)
    arr_1 = Array((2, 2), 1,2,3,4)
    arr_2 = Array((4, 1), 5,6,7,8)
    assert bool_arr.__mul__(arr_1) is NotImplemented
    assert arr_1.__mul__(bool_arr) is NotImplemented
    assert arr_1.__mul__(arr_2) is NotImplemented

    # Test Scalar Int
    other = 10
    assert other.__mul__(arr_1) is NotImplemented
    assert other * arr_1 == [[10, 20], [30, 40]]

    # Test Scalar Float
    other = 2.5
    float_arr = Array((1,2), 1.6, 3.6)
    assert other.__mul__(float_arr) is NotImplemented
    assert float_arr.__rmul__(other) == [[4.0, 9.0]]

    # Test Array Int
    arr_3 = Array((2, 2), 3,2,1,5)
    assert arr_1.__mul__(arr_3) == [[30, 40], [30, 200]]

    # Test Array Float 
    float_arr_2 = Array((1,2), 1.2, 2.0)
    assert float_arr.__mul__(float_arr_2) == [[4.8, 18.0]]


def test_same_2d():

    # Test value
    arr_1 = Array((3,2), 1,2,3,4,5,6)
    arr_2 = Array((1,5), 5,1,2,3,5)
    assert arr_1.is_equal(arr_2)

    # Test type
    string = "test"
    assert arr_1.is_equal(string)

    # Test scalar
    arr_3 = Array((2,1), 1, 1)
    other = 1
    assert arr_3.is_equal(other) == True

    # Test array
    arr_4 = Array((3,2), 6,2,3,1,4,5)
    arr_5 = Array((1,5), 5,1,2,3,8)
    assert arr_1.is_equal(arr_4) == [False, True, True, False, False, False]
    assert arr_2.is_equal(arr_5) == [True, True, True, True, False]


def test_mean_2d():
    # Test type
    bool_arr = Array((2,2), True, False, True, False)
    assert bool_arr.mean_element() # Gives valueError

    # Test array 
    arr_1 = Array((4,2), 20,15,10,5,1,3,1,5) # Should give 7.5
    assert arr_1.mean_element() == 7.5


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()

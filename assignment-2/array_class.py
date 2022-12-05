"""
Array class for assignment 2
"""

from multiprocessing.sharedctypes import Value
from typing import Type
from itertools import chain

# Mean method
from statistics import mean


class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Check if the values are of valid types
        if not (isinstance(values[0], (bool, int, float))):
            raise(TypeError("Values are of wrong type"))
        
        if not (isinstance(shape, tuple)):
            raise(TypeError("Shape is of wrong type"))
        
        for val in values:
            if not (isinstance(val, type(values[0]))):
                raise(ValueError("Not all values are of the same type"))

        # Check that the amount of values corresponds to the shape
        # For both 1-D and 2-D
        if (len(shape) > 1):
            if (shape[0]*shape[1] != len(values)):
                raise(ValueError("Number of values doesn´t fit with the shape"))
        else:
            if (shape[0] != len(values)):
                raise(ValueError("Number of values doesn´t fit with the shape"))
 
        # Set class-variables
        self.shape = shape
        self._values = values
        self.type = type(values[0])
        if (len(shape) > 1):
            self._array = self.create_2d()
            self.is2d = True
        else:
            self._array = list(values)
            self.is2d = False
        self.flat = self.flat_array()

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        return f"Array: {self._array}"

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        # check that the method supports the given arguments (check for data type and shape of array)
        # if the array is a boolean you should return NotImplementet

        # Check if self._array or "other" is of a boolean type
        if (self.type == bool) or (isinstance(other, Array) and other.type == bool) or type(other) == bool or type(self) == bool:
            return NotImplemented
        
        # Check if "other" is an Array and if they have the same shape
        if (isinstance(other, (int, float))):
            self.operation_other_number(other, "+")
        else:
            if (other.shape != self.shape):
                return NotImplemented
            else:
                self.operation_other_array(other.flat, "+")
        return self._array
            
    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if (self.type == bool) or (isinstance(other, Array) and other.type == bool) or type(other) == bool or type(self) == bool:
            return NotImplemented
        
        if (isinstance(other, (int, float))):
                self.operation_other_number(other, "-")
        else:
            if (other.shape != self.shape):
                return NotImplemented
            else:
                self.operation_other_array(other.flat, "-")
        
        return self._array

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return self.__sub__(other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if (self.type == bool) or (isinstance(other, Array) and other.type == bool) or type(other) == bool or type(self) == bool:
            return NotImplemented
        
        if (isinstance(other, (int, float))):
                self.operation_other_number(other, "*")
        else:
            if (other.shape != self.shape):
                return NotImplemented
            else:
                self.operation_other_array(other.flat, "*")
        
        return self._array

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        # Check type
        if (isinstance(other, Array) and other.type != self.type):
            return False 

        # Check shape
        if(isinstance(other, Array) and other.shape != self.shape):
            return False
    
        # Check if they are identical
        if (other != self._array):
            return False 

        return True 
    
    def __getitem__(self, index):
        return self._array[index]

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        try: 
            if not (isinstance(other, (Array, int, float))):
                raise(TypeError("Argument isn't an array, int or float"))
        except TypeError as e:
            return e
        
        if (isinstance(other, (float, int))):
            for x in range(len(self.flat)):
                if(self.flat[x] != other):
                    return False 
            return True 
        
        try: 
            # Check shape
            if(other.shape != self.shape):
                raise(ValueError("The two arrays shape does not match"))
        except ValueError as e:
            return e

        bool_arr = []
        for x in range(len(self.flat)):
            if(self.flat[x] != other.flat[x]):
                bool_arr.append(False)
            else: 
                bool_arr.append(True)
        return bool_arr

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        try:
            if (self.type == bool):
                raise(TypeError("Array must be of an int or float type, not boolean"))
        except TypeError as e:
            return e
        return min(self.flat)

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """
        try:
            if (self.type == bool):
                raise(TypeError("Array must be of an int or float, not boolean"))
        except TypeError as e:
            return e
        return mean(self.flat)
    
    # Helper private method for creating 2-D array
    def create_2d(self):
        x = 0
        array = []
        broke = False
        for i in range(0, self.shape[0]):
            tmp = []
            for j in range(self.shape[1]):
                if(x >= len(self._values)):
                    broke = True 
                    break 
                tmp.append(self._values[x])
                x += 1
            array.append(tmp)
            if(broke):
                break
        return array

    def operation_other_number(self, other, operation):
        for x in range(len(self.flat)):
            if(operation == "+"):
                self.flat[x] = self.flat[x] + other 
            elif(operation == "-"):
                self.flat[x] = -(other - self.flat[x])
            else:
                self.flat[x] = self.flat[x] * other 
        if(self.is2d):
            self.operation_flat()
        else:
            self._array = self.flat
    
    def operation_other_array(self, other, operation):
        for x in range(len(self.flat)):
            if(operation == "+"):
                self.flat[x] = self.flat[x] + other[x]
            elif(operation == "-"):
                self.flat[x] = self.flat[x] - other[x]
            else:
                self.flat[x] = self.flat[x] * other[x] 
        if(self.is2d):
            self.operation_flat()
        else:
            self._array = self.flat

    def operation_flat(self):
        index = 0
        broke = False
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if(index == len(self.flat)):
                    broke = True
                    break 
                self._array[x][y] = self.flat[index]
                index += 1
            if(broke):
                break 
    
    def flat_array(self):
        """Flattens the N-dimensional array of values into a 1-dimensional array.
        Returns:
            list: flat list of array values.
        """
        flat_array = self._array
        for _ in range(len(self.shape[1:])):
            flat_array = list(chain(*flat_array))
        return flat_array

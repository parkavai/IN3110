"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
from typing import Callable
from webbrowser import get
import matplotlib.pyplot as plt
from . import get_filter, io

def get_average_time(filter_function: Callable, arguments):
    """
    Helper method used for calculating average time from calling a filter function

    Args:
        filter_function (callable):
            The function which we measure time 
        arguments: 
            np_array passed to filter_function
    
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    start_timer = time.perf_counter()
    filter_function(arguments)
    end_timer = time.perf_counter()
    return end_timer - start_timer

def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    average_time = 0
    for x in range(calls):
        average_time += get_average_time(filter_function, arguments[x])
    return average_time/calls

def make_reports(filename: str = "rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """
    # create file "timing-report.txt"
    f = open("timing-report.txt", "x")

    # load the image
    copy = io.read_image(filename)

    # print the image name, width, height
    write_to_file = f"Timing performed using test/{filename}:{copy.shape[0]}x{copy.shape[1]} \n \n"
    print(f"Timing performed using test/{filename}:{copy.shape[0]}x{copy.shape[1]} \n")

    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"] 
    for filter_name in filter_names:
        # get the reference filter function
        if(filter_name == "color2gray"):
            reference_filter = get_filter()
        else:
            reference_filter = get_filter("color2sepia", "python")
        # time the reference implementation
        reference_time = time_one(reference_filter, copy, copy, copy)
        write_to_file += f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=}) \n"
        print(
                f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
            )
        # iterate through the implementations
        implementations = ["numpy", "numba"]
        for implementation in implementations:
            if(filter_name == "color2gray"):
                if(implementation == "numpy"):
                    filter = get_filter("color2gray", "numpy")
                else:
                    filter = get_filter("color2gray", "numba")
            else:
                if(implementation == "numpy"):
                    filter = get_filter("color2sepia", "numpy")
                else:
                    filter = get_filter("color2sepia", "numba")
            # time the filter
            filter_time = time_one(filter, copy, copy, copy)
            # compare the reference time to the optimized time
            speedup = reference_time - filter_time 
            write_to_file += f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x) \n"
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )
        print("")
        write_to_file += f" \n"
    f.write(write_to_file)

if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()

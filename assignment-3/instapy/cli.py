"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import get_filter, io
import time 

def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
    runtime: bool = False,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    im = Image.open(file)
    image = io.read_image(file)
    if scale != 1:
        # Resize image, if needed
        image = np.asarray(im.resize((im.width // 2, im.height // 2)))
    # Apply the filter
    filter_function = ""
    # Check which implementation was passed as argument
    if(implementation == "python"):
        if(filter == "color2gray"):
            filter_function = get_filter()
        else:
            filter_function = get_filter("color2sepia")
    elif(implementation == "numpy"):
        if(filter == "color2gray"):
            filter_function = get_filter("color2gray", "numpy")
        else:
            filter_function = get_filter("color2sepia", "numpy")
    elif(implementation == "numba"):
        if(filter == "color2gray"):
            filter_function = get_filter("color2gray", "numba")
        else:
            filter_function = get_filter("color2sepia", "numba")
    filtered = filter_function(image)
    if(runtime):
        for x in range(3):
            start_timer = time.perf_counter()
            filter_function(image)
            end_timer = time.perf_counter()
        runtime = (end_timer-start_timer)/3
        print(f"Average time over 3 runs: {runtime}s")
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)

def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", type=str, help="The filename to apply filter to")
    parser.add_argument("-o", "--out", type=str, metavar="OUT", help="The output filename")

    # Add required arguments
    # By having empty metavars in some cases, we ensure that the 'displayed' name is empty.
    # Except the flags 'scale', 'out' and 'implementation' in which we want to 'display' their names as shown in the assignment example
    parser.add_argument('-g', '--gray', action="store_true", help='Select gray filter')
    parser.add_argument('-se', '--sepia', action="store_true", help='Select sepia filter')
    parser.add_argument('-sc', '--scale', type=int, metavar='SCALE', help='Scale factor to resize image')
    parser.add_argument('-i', '--implementation', type=str, metavar='{python,numba,numpy,cython}', help='The implementation')
    parser.add_argument('-r', '--runtime', action="store_true", help='Shows average runtime on chosen implementation')

    # parse arguments and call run_filter
    args = parser.parse_args()
    isRuntime = False
    scale = 1
    # If the runtime flag is on, then the average_time is shown
    if(args.runtime):
        isRuntime = True 
    # If the scale flag is on, then the we send a value other than '1' to indicate resizing of image
    if(args.scale != None):
        scale = 2
    # It doesn´t say what to do if both gray and sepia flags are on so i just choose the gray_version
    if(args.gray and args.sepia):
        run_filter(args.file, args.out, args.implementation, "color2gray", scale, isRuntime)
    elif(args.gray):
        run_filter(args.file, args.out, args.implementation, "color2gray", scale, isRuntime)
    elif(args.sepia):
        run_filter(args.file, args.out, args.implementation, "color2sepia", scale, isRuntime)


    




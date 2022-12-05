<h1>Instapy</h1>

Summary: <br />
This package´s responsibility is to change the color of certain pictures to either 
gray or sepia depending on the flags which the users pass through the command-line 
interface. It also shows a report on the fastest implementation between pure python,
numpy and numba. 

Instructions for installing package: 
* Install the package through "python3 -m pip install ." 
* Install all the packages used in the assignment: "pip install numpy pillow line-profiler"

Instructions for running package: 
* Option 1: python3 -m instapy 
* Option 2: instapy 

Examples for running with flags:
* out_file: instapy rain.jpg -o test_instapy.jpg -se -i numba
* display: instapy rain.jpg -g -i numpy
* scale: instapy rain.jpg -g -sc 2 -i numpy
* runtime: instapy rain.jpg -g -sc 2 -i numpy -r


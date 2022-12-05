import re
from typing import Tuple

from requesting_urls import get_html

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = "\d{4}"
    # month should accept month names or month numbers
    month = "(?:January|February|March|April|May|June|July|August|September|October|November|December|"
    month_abbreviation = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    # Include regex for full-names aswell as abbreviation
    month = month + month_abbreviation  
    # day should be a number, which may or may not be zero-padded
    day = "\d{1,2}"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        # Still got to check wether we have a single digit in which we zero pad it. 
        if(len(str(s)) == 1):
            return zero_pad(s)
        return s 

    # Convert to number as string
    for x in range(len(month_names)):
        if(s == month_names[x]):
            x += 1
            if(x < 10):
                return zero_pad(str(x))
            return str(x)

def check_day(s: str) -> str:
    """Checks if day needs to be sent to zero_pad or not

    arguments:
        s (str) : day number as a string
    returns:
        s : day number as zero-padded string
    """
    if(len(str(s)) == 1):
            return zero_pad(s)
    return s 

def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    return "0" + n    

def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    # Have adjusted the range for month and day
    ISO = r"(\d{4}-[0-1]?[0-9]-[0-3]?[0-9])"

    # Date on format DD/MM/YYYY
    DMY = r"\d{1,2} " + month + " \d{4}"

    # Date on format MM/DD/YYYY
    MDY = month + r" [0-3]?[0-9]" + ", " + year

    # Date on format YYYY/MM/DD
    YMD = r'\d{4} ' + month + ' [0-3]?[0-9]'

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

    for x in range(len(formats)):
        # find all dates in any format in text
        matches = re.findall(formats[x], text)
        for string in matches:
            # We may get empty matches so we ignore them should they occur
            if(string == None):
                continue
            # ISO
            # 2020-10-13
            if(x == 0):
                string = string.split("-")
                year = string[0]
                month = convert_month(string[1])
                day = check_day(string[2])
                date = year+"/"+month+"/"+day
                dates.append(date)
            # DMY
            # 13 October 2020
            elif(x == 1):
                string = string.split(" ")
                day = check_day(string[0])
                month = convert_month(string[1])
                year = string[2]
                date = year+"/"+month+"/"+day
                dates.append(date)
            # MDY
            # October 13, 2020
            elif(x == 2):
                string = string.split(" ")
                day = check_day(string[1].replace(",", ""))
                month = convert_month(string[0])
                year = string[2]
                date = year+"/"+month+"/"+day
                dates.append(date)
            # YMD
            # 2020 October 13
            else:
                string = string.split(" ")
                day = check_day(string[2])
                month = convert_month(string[1])
                year = string[0]
                date = year+"/"+month+"/"+day
                dates.append(date)

    # Write to file if wanted
    if output:
        f = open(output, "w")
        # Filter out duplicates
        dates = set(dates)
        for date in dates:
            string = date + "\n"
            f.write(string)
        f.close()
    return dates

if __name__ == "__main__":
    html = get_html("https://en.wikipedia.org/wiki/Serena_Williams")
    find_dates(html, "output.txt")

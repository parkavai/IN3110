import re
from copy import copy
from dataclasses import dataclass

import bs4
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import false
from requesting_urls import get_html

## --- Task 5, 6, and 7 ---- ##

# Dict over all types of events
event_types = {
    "DH": "Downhill",
    "SL": "Slalom",
    "GS": "Giant Slalom",
    "SG": "Super Giant slalom",
    "AC": "Alpine Combined",
    "PG": "Parallel Giant Slalom",
}


def time_plan(url: str) -> str:
    """Parses table from html text and extract desired information
    and saves in betting slip markdown file

    arguments:
        url (str) : URL for page with calendar table
    return:
        markdown (str) : string containing the markdown schedule
    """
    # Get the page
    html = get_html(url)
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # locate the table
    men = soup.find(id="Men")
    soup_table = men.find_next("table").find_next("table")
    # extract events into pandas data frame
    df = extract_events(soup_table)
    # Write the schedule markdown
    return render_schedule(df)


@dataclass
class TableEntry:
    """Data class representing a single entry in a table

    Records text content, rowspan, and colspan attributes
    """

    text: str
    rowspan: int
    colspan: int


def extract_events(table: bs4.element.Tag) -> pd.DataFrame:
    """Gets the events from the table
    arguments:
        table (bs4.element.Tag) : Table containing data
    return:
        df (DataFrame) : DataFrame containing filtered and parsed data
    """
    # Gets the table headers and saves their labels in `keys`
    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]
    data = []

    # Extracts the data in table, keeping track of colspan and rowspan
    rows = table.find_all("tr")
    rows = rows[1:]
    for row in rows:
        cells = row.find_all(["td"])
        if not cells:
            continue
        row = []
        for cell in cells:
            rowspan = 1
            # If there is no rowspan, then it is set to "1" 
            if(cell.has_attr("rowspan")):
                rowspan = int(cell["rowspan"])
            colspan = 1
            # If there is no colspan, then it is set to "1" 
            if(cell.has_attr("colspan")):
                colspan = int(cell["colspan"])
            text = strip_text(cell.get_text(strip=True))
            row.append(
                        TableEntry(
                            text=text,
                            rowspan=rowspan,
                            colspan=colspan,
                        )
                    )
        data.append(row)

    # at this point `data` should be a table (list of lists)
    # where each item is a TableEntry with row/colspan properties
    # expand TableEntries into a dense table
    all_data = expand_row_col_span(data)

    # List of desired columns
    wanted = ["Date", "Venue", "Type"]

    # Filter data and create pandas dataframe
    filtered_data = ""
    # If length is under at least 5 then we are working with the uio part
    if(len(data[0]) < 5):
        filtered_data = filter_data_uio(labels, all_data, wanted)
    else:
        filtered_data = filter_data(labels, all_data, wanted)
    df = pd.DataFrame(filtered_data, columns=wanted)
    return df

def expand_event_type(type_key):
        """Expand event type key (SL) to full name (Slalom)

        Useful with pandas Series.apply
        """
        return event_types.get(type_key[:2], type_key)

def render_schedule(data: pd.DataFrame) -> str:
    """Render the schedule data to markdown

    arguments:
        data (DataFrame) : DataFrame containing table to write
    return:
        markdown (str): the rendered schedule as markdown
    """
    return data.to_markdown()

def strip_text(text: str) -> str:
    """Gets rid of cruft from table cells, footnotes and setting limit to 20 chars

    It is not required to use this function,
    but it may be useful.

    arguments:
        text (str) : string to fix
    return:
        text (str) : the string fixed
    """

    text = text[:20]  # 20 char limit
    text = re.sub(r"\[.*\]", "", text)
    return text

def filter_data_uio(keys: list, data: list, wanted: list):
    """Filters away the columns not specified in wanted argument

    Used for UiO only since there is differences between how 
    the UiO is structured and the wiki page. Because of this,
    i had to create a separate function in order to get the 
    values correctly sorted for the UiO part.  

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (list of lists) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """
    event = {}
    for key in wanted:
        event[key] = []
    # Date, Venue and Type is the order
    for row in data:
        i = 0
        for element in row:
            # The first element of the row is always a date in the uio
            if(i == 0):
                event["Date"].append(element)
            # After date comes venue
            elif(i == 1):
                event["Venue"].append(element)
            # In the end is a type
            elif(i == 2):
                event["Type"].append(element)   
            i += 1
    return event


def filter_data(keys: list, data: list, wanted: list):
    """Filters away the columns not specified in wanted argument

    It is not required to use this function,
    but it may be useful.

    I have set regular expressions for both date and type in order to properly
    check wether the element is a date or type. Also have a "isVenue" which 
    is used for deciding wether the element is a venue. 

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (list of lists) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """
    event = {}
    pattern_date = r'\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{0,4}'
    pattern_type = r'(DH|SL|GS|SG|AC|PG)'
    isVenue = False 
    for key in wanted:
        event[key] = []
    for row in data:
        for element in row:
            # Check if is date
            if(re.search(pattern_date, str(element))):
                event["Date"].append(element)
                # Right after date, then there is a "venue", so we set the value to true
                isVenue = True 
            elif(isVenue):
                event["Venue"].append(element)
                # Set the value to false in order to restart the process for venue 
                isVenue = False
            elif(re.search(pattern_type, str(element[:2]))):
                # Using the helper method given in order to properly get the type value
                event["Type"].append(expand_event_type(element[:2])) 
    return event

def expand_row_col_span(data):
    """Applies row/colspan to tabular data

    It is not required to use this function,
    but it may be useful.

    - Copies cells with colspan to columns to the right
    - Copies cells with rowspan to rows below
    - Returns raw data (removing TableEntry wrapper)

    arguments:
        data_table (list) : data with rows and cols
            Table of the form:

            [
                [ # row
                    TableEntry(text='text', rowspan=2, colspan=1),
                ]
            ]
    return:
        new_data_table (list): list of lists of strings
            [
                [
                    "text",
                    "text",
                    ...
                ]
            ]

            This should be a dense matrix (list of lists) of data,
            where all rows have the same length,
            and all values are `str`.
    """

    # first, apply colspan by duplicating across the column(s)
    new_data = []
    for row in data:
        new_row = []
        new_data.append(new_row)
        for entry in row:
            for _ in range(entry.colspan):
                new_entry = copy(entry)
                new_entry.colspan = 1
                new_row.append(new_entry)

    # apply row span by inserting copies in subsequent rows
    # in the same column
    for row_idx, row in enumerate(new_data):
        for col_idx, entry in enumerate(row):
            for offset in range(1, entry.rowspan):
                # copy to row(s) below
                target_row = new_data[row_idx + offset]
                new_entry = copy(entry)
                new_entry.rowspan = 1
                target_row.insert(col_idx, new_entry)
            entry.rowspan = 1

    # now that we've applied col/row span,
    # replace the table with the raw entries,
    # instead of the TableEntry objects
    return [[entry.text for entry in row] for row in new_data]


if __name__ == "__main__":
    # test the script on the past few years by running it:
    for year in range(20, 23):
        url = (
            f"https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup"
        )
        print(url)
        md = time_plan(url)
        print(md)

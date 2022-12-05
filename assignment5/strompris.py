#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Make sure to document arguments and return value

    arguments:
        - date (str): Represents a date
        - location (str): Represents a location in Norway
    return:
        - df (Dataframe) : Dataframe containing "NOK_per_kWh" and "time_start" 
    """
    # Optional must be handled where date is set to current_date
    if date is None:
        date = datetime.date.today()

    # Testing the assumption as mentioned in the assignment
    after = datetime.date(2022, 10, 2)
    assert (date >= after)

    # Add an extra "0" should day be less than 10
    if(date.day < 10):
        url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.month}-0{date.day}_{location}.json"
    else:
        url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.month}-{date.day}_{location}.json"

    r = requests.get(url)

    # Check that the url is found and succesfull
    assert (200 <= r.status_code < 300)

    data = r.json()
    new = {"NOK_per_kWh": [], 
            "time_start": []}
    for dictionary in data:
        new["NOK_per_kWh"].append(float(dictionary["NOK_per_kWh"]))
        d = dictionary["time_start"]
        new["time_start"].append(d)

    # Important to convert dates to datetime
    df = pd.DataFrame.from_dict(new)
    df["time_start"] = pd.to_datetime(df["time_start"])
    return df



# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"
}

# task 1:

def create_df(date: datetime.date, location: str):
    """
    A helper method for creating a dataframe. This is specifically used for the function "fetch_prices"

    arguments:
        - date (str): Represents a date
        - location (str): Represents a location in Norway
    return:
        - df (Dataframe) : Dataframe containing "NOK_per_kWh" and "time_start" 
    """
    df = fetch_day_prices(date, location)
    df["location_code"] = location
    df["location"] = LOCATION_CODES[location]
    return df

def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Make sure to document arguments and return value
    arguments:
        - end_date (str): Represents a date or if null is set to the current_date
        - days (int): Specifies amount of days which we wil fetch data
        - location (str): Represents a location in Norway
    return:
        - df (Dataframe) : Dataframe containing "NOK_per_kWh" and "time_start" 
    """
    # Optional must be handled where end_date is set to current_date
    if end_date is None:
        end_date = datetime.date.today()

    length_location = len(locations)
    if(days == 1):
        date = datetime.date(2022, int(end_date.month), end_date.day)
        location = locations[0]
        df = create_df(date, location)
    else:
        x = 1
        locations_index = 0
        pdList = []
        while x != days:
            if(locations_index == length_location):
                locations_index = 0
            date = datetime.date(2022, int(end_date.month), end_date.day)
            location = locations[locations_index]
            pdList.append(create_df(date, location))
            x += 1
            locations_index += 1
        df = pd.concat(pdList, names=["NOK_per_kWh", "time_start", "location_code", "location"])

    return df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value...
    """
    df = str(df["time_start"])
    chart = alt.Chart(df).mark_line().encode(
        y="NOK_per_kWh",
        x="time_start",
    )
    chart.show()
    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()

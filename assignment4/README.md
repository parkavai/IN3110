<h1>Assignment4</h1>

The assignment was solved using macOs

## Version: <br />
Python 3.9.12

## Dependencies: <br />
* requests: Installed through "python3 -m pip install requests"
* beautifoulsoup4: Installed through "python3 -m pip install beautifulsoup4"

## How to run: <br />
Task 1: <br />
    To validify if the "requesting_url" works as it should, run the test script located in the "test_requesting_urls.py".
    Important that you are in the assignment4 folder, if so then type the following command: "pytest -v tests/test_requesting_urls.py"
    to test the "requesting_url.py" script. 

Task 2 and 3: <br />
    Run the test script located in the "test_filter_urls.py". Important that you are in the assignment4 folder, if so then type the following command: "pytest -v tests/test_filter_urls.py" to test the "filter_url.py" script. 

Task 4: <br />
    For quick testing, run the command "python collect_dates.py" which will run the functions in the script and create 
    an "output.txt" file which consists of date in the format as mentioned in the assignment. Or run the test script 
    through the command: "pytest -v tests/test_collect_dates.py".

Task 5, 6 and 7: <br />
    Run the test script located in the "test_time_planner.py". Important that you are in the assignment4 folder, if so then type the following command: "pytest -v tests/test_time_planner.py" to test the "time_planner.py" script. For quick testing to check 
    wether the functions properly work or not, you could also run "python time_planner.py". 

Task 8, 9 and 10: <br />
    For quick testing, run the command "python fetch_player_statstics.py" which will run the functions in the script and create 
    the ".png" files which individually, shows a graph for a specific stat. For example: "points.png" shows the points for the top 3 NBA_players from each team with colours for each bar which represents the team colour. This applies to the other ".png"´s aswell. Or just run the test script through the command: "pytest -v tests/test_fetct_player_statistics.py".

## Comments to the grader: <br />
I haven´t done the wiki race challenge. I have also used the helper methods given within the files for each task and
left the print statements which was in the files. 


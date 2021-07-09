# WORK IN PROGRESS
This project is still in development. \
The files are still full of debug logs and commented out test code.

# Youless-LS120

## Examples:
- run liveview_allgraphs.py and a flask webserver will start on http://127.0.0.1:80 that displays all available graphs
	- plots live, daily, monthly and yearly Electricity and GAS usage and automatically updates the database
	- webpage is hosted on ip that is set in settings.py and based on debug setting	
- run test_view.py and a flask webserver will start on http://127.0.0.1:80 that displays the graphs set in that same file under the callback and multi_output function
	- this file is for testing purposes
	- webpage is hosted on ip that is set in settings.py and based on debug setting

## Functions:
 - Dash text is available in Dutch and English (set settings.py)
 - Realtime view with about 2 minutes history, updates every 5 seconds (not stored in database)
 - Live view per minute up to 10 hours history, updates every minute (not stored in database)
 - Import and process Energy (Electricity and Gas) data from Youless LS120 into SQLite3 database 
	- All data is stored as text and converted when read from the database
	- *Appends and overwrites data if needed*
 - Read data back from SQLite3 database
 - Convert read data to list based on wanted items
 - Convert list to Pandas DataFrame based on wanted items
 - Create dash based website with graphs
 
## Files:
 - settings.py contains all settings and libraries, no need to edit the other files
 - create_database.py creates youless.db if needed or appends tables if needed
 - import_data.py reads static data from Youless LS120 and writes it to the database
 - read_data.py reads data from the database and returns lists with data
 - plot_data.py converts lists with data and returns plotly figures 
 - read_live.py reads live data fro the Youless LS120 and returns lists with data
 - plot_live.py converts lists with live data and returns plotly figures
 - web_elements.py contains pre defined settings for both view files 

## requirements.txt
 - Contains all needed libraries/modules
 - Install them with: python -m pip install -r requirements.txt

## Usage:
 - 

## To Do:
 - Add explanatory usage
 - Create interactive Dash website with:
	- Separate webpage from plot script
	- Automatic view of available data
	- Buttons that click to available data
	- Custom graphs based on available data. e.g. average electricity usage on wednesdays
 - Add quick tutorial to create a linux service that always runs
	- Examples available in startupscript.txt (No explanation yet)
 - Add extra notations for more clarity
 - Convert read database data to Pandas DataFrame directly
 - ~~Remove commented out code~~
 - ~~Add quick tutorial on how to install requirements.txt~~
 - ~~Live usage view~~
 - ~~Combine reused code to importable class methods~~
 - ~~Add GAS usage~~
 - ~~Check if existing data in database matches retrieved data from Youless, if so then do nothing, else append~~
 - ~~Create automatic readout from LS120~~
 - ~~Make webpage available on linux server~~
 
 
## Some example views
![Realtime view](docs/liverealtime.png)\
![Live per minute](docs/liveminutes10hrs.png)\
![Day overview](docs/day.png)\
![Month overview](docs/month.png)\
![Year per day overview](docs/yeardays.png)\
![Year per month overview](docs/yearmonths.png)

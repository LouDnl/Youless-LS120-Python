# WORK IN PROGRESS
This project is still in development.

# Youless-LS120

## Package
This package is for importing data from a YouLess LS120 datalogger that is connected to a smart electricity and gas meter.
The data is stored in an SQLite3 database and displayed on a dash webpage using pandas and plotly.
I created this package for stand-alone usage and not with a setup.py for installing.
While I oriented this on Dash it is ofcourse possible to use the data retrieved from the YouLess and the plotly figures created in any other webpage.

## Functions:
- Dash text is available in Dutch and English (set in settings.py)
- Realtime view with about 2 minutes history, updates every 5 seconds (not stored in database)
- Live view per minute up to 10 hours history, updates every minute (not stored in database)
- Import and process Energy (Electricity and Gas) data from Youless LS120 into SQLite3 database 
	- All data is stored as text and converted when read from the database
	- *Appends and overwrites data if needed*
- Read data back from SQLite3 database
- Convert read data to list based on wanted items
- Convert list to Pandas DataFrame based on wanted items
- Create dash based website with graphs

## requirements.txt
- Contains all needed libraries/modules
- Install them with: python -m pip install -r requirements.txt

## Usage:
- git clone the repository
	```
	git clone https://github.com/LouDnl/Youless-LS120.git
	cd Youless-LS120
	```
- Run either example files to get an idea of what is possible. \
	dash_allgraphs_live can run with settings from dash_settings.py: \
	`python3 dash_allgraphs_live.py default` \
	or with command line arguments where:\
	IP = the ip to host dash on \
	PORT = the port to host dash on \
	DEBUG = either True or False to see Dash errors and callbacks \
	`python3 dash_allgraphs_live.py IP PORT DEBUG` \
	or run dash_test_view that uses settings from dash_settings.py\
	`python3 dash_test_view.py`
- Or use any of the package funtions in your own code. Every function \
	has it's own description, go check them out :)


## Example files:
- dash_allgraphs_live.py starts a flask webserver that displays all available graphs
	- updates the database on start and while active
	- plots live, daily, monthly and yearly Electricity and GAS usage
	- webpage is hosted on ip that is set in dash_settings.py and based on debug setting \
	or the webpage is hosted on settings given as command line arguments and ignores dash_settings.py.
- dash_test_view.py starts a flask webserver that displays the graphs set in that same file under the callback and multi_output function
	- this file is for testing purposes
	- webpage is hosted on ip that is set in dash_settings.py and based on debug setting
- dash_settings.py contains the IP settings for the dash webserver.
- dash_web_elements.py contains pre defined settings for both example files \
 they can also be used for your own dash page.
- **when running default and if DASH_DEBUG in dash_settings.py is set to True the webserver will be hosted on local_ip,** \
**if set to False the webserver will be hosted on remote_ip**

## Package files:
- `LS120/settings.py` contains user changeable settings like language, database name \
	and path and the IP address for the Youless, this file has no external functions
- `LS120/constants.py` contains all constant variables etc for the package. \
 this file has no external functions
- `LS120/ls120_logger_config.yaml` contains the logger settings.\
 by default the logger level is set to INFO under root. Set this to DEBUG to see what is happening behind the scenes.	
- `LS120/create_database.py` creates youless.db if needed or appends tables if needed \
 run this file to create the initial database file inside the LS120 folder \
 `python3 LS120.create_database`
- `LS120/import_data.py` reads static data from Youless LS120 and writes it to the database \
 run this file to automatically import new data to the database `python3 LS120.import_data` \
 available functions are:
	- `parse_data().retrieve_days(etype)`
		```
		Function to retrieve all Electricity and Gas hour values from Youless 120
		with a maximum history of 70 days back (youless max).
		returns a list with tuples of data.

		:retrieve_days(etype)
		:etype is 'E' or 'G' for Electricity or Gas		
		```
	- `parse_data().retrieve_months(etype)`
		```
		Function to retrieve days per month from Youless 120
		up to 11 months back for Electricity and Gas.
		returns a list with tuples of data.

		:retrieve_months(etype)
		:etype is 'E' or 'G' for Electricity or Gas		
		```
	- `parse_data().parse_days(etype, data)`
		```
		Function to parse the information retrieved by retrieve_days

		:parse_days(etype, data)
		:etype is 'E' or 'G' for Electricity or Gas
		:data is a list with tuples retrieved by retrieve_days		
		```
	- `parse_data().parse_months(etype, data)`
		```
		Function to parse the information retrieved by retrieve_months

		:parse_months(etype, data)
		:etype is 'E' or 'G' for Electricity or Gas
		:data is a list with tuples retrieved by retrieve_months		
		```
	- `parse_data().insert_dayhours(conn, insertion, table, type)`
		```
		Internal function to store values in sqlite3 database in the following format (all strings):
		date, year, week, month, monthname, day, yearday, values per hour
		example:
		('2021-04-03', 2021, 13, 4, 'April', 3, 93, '[428.0, 385.0, 400.0, 391.0, 386.0, 398.0, 403.0, 485.0, 759.0, 611.0, 650.0, 1225.0, 626.0, 940.0, 534.0, 630.0, 751.0, 630.0, 1194.0, 951.0, 934.0, 893.0, 628.0, 581.0]')
		```
	- `parse_data().insert_yeardays(conn, insertion, table, type)`
		```
		Internal function to store values in sqlite3 database in the following format (all strings):
		date, year, month, monthname, values per day
		example return:
		('2020-12-01', 2020, 12, 'December',
		'[18.85, 15.12, 19.72, 13.76, 13.93, 20.7, 17.66, 18.57, 14.14, 13.23, 12.72, 15.38, 16.89, 16.06,
		15.39, 22.16, 15.0, 15.34, 12.61, 17.17, 18.85, 15.25, 20.22, 13.51, 15.35, 13.49, 12.99, 21.87, 14.2, 16.7, 15.45]')	
		```
	- `parse_data().create_connection(db_file)`
		```
		Internal function to create a connection to the database		
		```
- `LS120/read_data.py` reads data from the database and returns lists with data \
 available functions are:
 	- `read_data().retrieve_hours(table, year, month, startday, starthour, *args)`
		```
        Retrieve data from table dayhours_X and return list with items.
        Retrieve hour data for given year, month and days with a minimum of 1 hour and a maximum of 24 hours in a list with hours and values.
        Since we dont know if the end day/hour is the same as the start day/hour we use *args to accept this.
        When only startday and starthour is given, only that single hour will be retrieved
        Examples:
            retrieve_hours('dayhours_g', 2021, 3, 2, 3, 3, 6) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
            retrieve_hours('dayhours_e', 2020, 10, 1, 12) # year: 2020, month: 10, startday: 1, starthour: 12
            retrieve_hours('dayhours_e', 2020, 11, 2, 11, 18) # year: 2020, month: 11, startday: 2, starthour: 11, endhour: 18
        table as string
        year as integer
        month as integer (min is 1, max is 12)
        startday as integer (min is 1, max is 30)
        endday as integer (min is 2, max is 31)
        starthour as integer (min is 0 (00:00), max is 23 (23:00))
        endhour as integer (min is 1 (01:00), max is 24 (24:00))		
		```
	- `read_data().retrieve_day(year, month, day, table)`
		```
        Retrieve data from table dayhours_X and return list with items.
        Retrieves day data for given year, month and day in a list with hours and values.
        retrieve_day(2021, 1, 19, 'dayhours_e')
        year as integer
        month as integer
        day as integer
        table as string		
		```
	- `read_data().retrieve_month(year, month, table)`
		```
        Retrieve data from table yeardays_X and return list.
        Retrieves monthdata for given month of given year in a list with days and values
        retrieve_month(2021, 1, 'yeardays_e')
        year as integer
        month as integer
        table as string		
		```
	- `read_data().retrieve_year(year, totals, table)`
		```
        Retrieve data from table yeardays_X and return list with items.
        Retrieves available data for given year per month and day in values
        Returns either month totals or day totals for the entire year.
        retrieve_year(2021, 2, 'yeardays_g')
        year as integer
        totals as integer (1 is month totals, 2 is day totals)
        table as string		
		```
- `LS120/read_live.py` reads live data from the Youless LS120 and returns lists with data \
available functions are:
	- `read_live_data().read_live()`
		```
        read live energy data from Youless 120
        returns a dictionary with data
        example return: {'cnt': ' 29098,470', 'pwr': 581, 'lvl': 0, 'dev': '', 'det': '', 'con': 'OK', 'sts': '(48)', 'cs0': ' 0,000', 'ps0': 0, 'raw': 0}		
		```
	- `read_live_data().read_minutes()`
		```
        read per minute energy data from Youless 120
        data is always 1 minute behind live
        returns a dictionary with 2 lists consisting of time values and watts values
        example return:
        {'time': ['value', 'value'], 'watts': ['value', 'value']}		
		```
	- ~~`read_live_data().read_ten_minutes()`~~ This function does not yet work
- `LS120/plotly_graphs/plot_data.py` converts lists with data and returns plotly figures  \
 available functions are:
	- `plot_data().plot_hours(*args)`
		```
		Reads from table dayhours_X and return figure
		Plot hours from given starthour up to endhour.
		Plot spans a max of 2 days with a minimum of 1 hour and a maximum of 24 hours.
		Minimum arguments is 5, maximum is 7 in this order:
			energytype: 'E', year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
			energytype: 'E', year: 2021, month: 3, startday: 2, starthour: 5, endhour: 6
			energytype: 'E', year: 2021, month: 3, startday: 2, starthour: 5
		plot_hours(arguments) examples:
			plot_hours("E", 2021, 3, 2, 12, 3, 11)
			plot_hours("E", 2021, 3, 2, 12, 11)
			plot_hours("E", 2021, 3, 2, 12)
		```
	- `plot_data().plot_day_hour(year, month, day, etype)`
		```
		Reads from table dayhours_X and return figure
		Plot one day of the year into a graph with hourly totals.
		plot_day_hour(2021, 1, 19, 'E') or plot_day_hour(2021, January, 19, 'G')
		year as integer
		month as integer or string
		day as integer
		etype as string ('E' for Electricity, 'G' for Gas)
		```
	- `plot_data().plot_month_day(year, month, etype)`
		```
		Reads from table yeardays_X and returns figure
		plot one month of the year into a graph with daily totals.
		plot_month_day(2021, 1, 'E') or plot_month_day(2021, January, 'G')
		year as integer
		month as integer or string
		etype as string ('E' for Electricity, 'G' for Gas)
		```
	- `plot_data().plot_year_day(year, etype)`
		```
		Reads from table yeardays_X and returns figure
		plot the year with daily totals into a graph
		plot_year_day(2021, 'E')
		year as integer
		etype as string ('E' for Electricity, 'G' for Gas)
		```
	- `plot_data().plot_year_month(year, etype)`
		```
        Reads from table yeardays_X and returns figure
        plot the year with month totals into a graph
        plot_year(2021, 'E')
        year as integer
        etype as string ('E' for Electricity, 'G' for Gas)		
		```
- `LS120/plotly_graphs/plot_live.py` converts lists with live data and returns plotly figures
available functions are:
	- `plot_live().plot_live()` \
		returns plotly figure with current live information read directly from the Youless. \
		starts with current usage and doesnt have history.
	- `plot_live().plot_minutes()` \
		returns plotly figure with live usage including history until 10 hours back. 
	- ~~`plot_live().plot_ten_minutes()`~~ This function does not yet work

## To Do:
- Create interactive Dash website with:
	- Separate webpage from plot script
	- Automatic view of available data
	- Buttons that click to available data
	- Custom graphs based on available data. e.g. average electricity usage on wednesdays
- Add quick tutorial to create a linux service that always runs
	- Examples available in docs/startupscript.txt (No explanation yet)
- Split import_data into read and return and write to database
- Convert read database data to Pandas DataFrame directly
- ~~Add explanatory usage per package file method~~
- ~~Add extra notations for more clarity~~
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

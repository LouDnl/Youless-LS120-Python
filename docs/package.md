## Package files:
- `LS120/settings.py` contains user changeable settings like language, database name and path and the IP address for the Youless. \
 this file has no user functions
- `LS120/constants.py` contains all constant variables etc for the package. \
 this file has no user functions
- `LS120/ls120_logger.py` configures and starts the logger for the package.
- `LS120/ls120_logger_config.yaml` contains the logger settings.\
 by default the logger level is set to INFO under root. Set this to DEBUG to see what is happening behind the scenes.
- `LS120/db_create.py` creates youless.db if needed or appends tables if needed \
 run this file to create the initial database file inside the LS120 folder \
 `python3 LS120.db_create`
- `LS120/db_auto_import.py` automatically imports data provided by read_youless.py and writes it the database with db_write_data.py \
run this file to automatically import new data to the database `python3 LS120.db_auto_import` \
- `LS120/db_connect.py` this file provides a database connector for the package.
- `LS120/db_write_data.py` this file parses data read from the youless and writes it to the database. \
 available functions are:
    - `parse_data().parse_tenminutes(etype, data)`
        ```
        Function to parse the information retrieved by read_ten_minutes

        example:
        parse_tenminutes(etype, data)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        :data is a list with tuples retrieved by read_ten_minutes
        ```
    - `parse_data().parse_days(etype, data)`
        ```
        Function to parse the information retrieved by retrieve_days

        example:
        parse_days(etype, data)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        :data is a list with tuples retrieved by retrieve_days
        ```
    - `parse_data().parse_months(etype, data)`
        ```
        Function to parse the information retrieved by retrieve_months

        example:
        parse_months(etype, data)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        :data is a list with tuples retrieved by retrieve_months
        ```
    - `write_data().write_tenminutes(conn, insertion, table, type)`
        ```
        Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, week, month, monthname, day, yearday, values per hour

        example insertion:
            ('2021-07-16', [('2021', '28', '07', 'July', '16', '197'), [{'23:50': 264}, {'23:40': 432}, {'23:30': 600}, {'23:20': 648}, {'23:10': 540}]])
        example converted_insertion:
            ('2021-07-16', '2021', '28', '07', 'July', '16', '197', "[{'23:50': 264}, {'23:40': 432}]")
        ```
    - `write_data().write_dayhours(conn, insertion, table, type)`
        ```
        Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, week, month, monthname, day, yearday, values per hour

        example insertion:
            ('2021-04-03', 2021, 13, 4, 'April', 3, 93, '[428.0, 385.0, 400.0, 391.0, 386.0, 398.0, 403.0, 485.0, 759.0, 611.0, 650.0, 1225.0, 626.0, 940.0, 534.0, 630.0, 751.0, 630.0, 1194.0, 951.0, 934.0, 893.0, 628.0, 581.0]')
        ```
    - `write_data().write_yeardays(conn, insertion, table, type)`
        ```
        Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, month, monthname, values per day

        example insertion:
            ('2020-12-01', 2020, 12, 'December',
            '[18.85, 15.12, 19.72, 13.76, 13.93, 20.7, 17.66, 18.57, 14.14, 13.23, 12.72, 15.38, 16.89, 16.06,
            15.39, 22.16, 15.0, 15.34, 12.61, 17.17, 18.85, 15.25, 20.22, 13.51, 15.35, 13.49, 12.99, 21.87, 14.2, 16.7, 15.45]')
        ```
- `LS120/db_retrieve_data.py` tis file retrieves data from youless sqlite3 database and returns it. \
 available functions are:
    - `retrieve_data().retrieve_hours(table, year, month, startday, starthour, *args)`
        ```
        Retrieve data from table dayhours_X and return list with items.
        Retrieve hour data for given year, month and days with a minimum of 1 hour and a maximum of 24 hours in a list with hours and values.
        Since we dont know if the end day/hour is the same as the start day/hour we use *args to accept this.
        When only startday and starthour is given, only that single hour will be retrieved.

        Examples:
            retrieve_hours('dayhours_g', 2021, 3, 2, 3, 3, 6) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6\n
            retrieve_hours('dayhours_e', 2020, 10, 1, 12) # year: 2020, month: 10, startday: 1, starthour: 12\n
            retrieve_hours('dayhours_e', 2020, 11, 2, 11, 18) # year: 2020, month: 11, startday: 2, starthour: 11, endhour: 18\n

        args:
        :table as string
        :year as integer
        :month as integer (min is 1, max is 12)
        :startday as integer (min is 1, max is 30)
        :endday as integer (min is 2, max is 31)
        :starthour as integer (min is 0 (00:00), max is 23 (23:00))
        :endhour as integer (min is 1 (01:00), max is 24 (24:00))
        ```
    - `retrieve_data().retrieve_day(year, month, day, table)`
        ```
        Retrieve data from table dayhours_X and return list with items.
        Retrieves day data for given year, month and day in a list with hours and values.

        example:
        retrieve_day(2021, 1, 19, 'dayhours_e')

        args:
        :year as integer
        :month as integer
        :day as integer
        :table as string
        ``` 
    - `retrieve_data().retrieve_month(year, month, table)`
        ```
        Retrieve data from table yeardays_X and return list.
        Retrieves monthdata for given month of given year in a list with days and values

        example:
        retrieve_month(2021, 1, 'yeardays_e')

        args:
        :year as integer
        :month as integer
        :table as string
        ```
    - `retrieve_data().retrieve_year(year, totals, table)`
        ```
        Retrieve data from table yeardays_X and return list with items.
        Retrieves available data for given year per month and day in values.
        Returns either month totals or day totals for the entire year.

        example:
        retrieve_year(2021, 2, 'yeardays_g')

        args:
        :year as integer
        :totals as integer (1 is month totals, 2 is day per month totals)
        :table as string
        ```
    - `retrieve_custom_data().check_existence(**kwargs)`
        ```
        function to check if item exists in sqlite database.\n
        returns 1 if row exists and 0 if not.

        :table= str
        :column= str
        :item= str/int (int gets transformed to str in process)
        ```
    - `retrieve_custom_data().get_item(**kwargs)`
        ```
        returns item from database corresponding to the given query and kwargs

        examples:
            retrieve_custom_data().get_item(query='select_one_and',
                                            select=('*'),
                                            table='dayhours_e',
                                            id='year',
                                            item='2021',
                                            id2='yearday',
                                            item2='44')
            retrieve_custom_data().get_item(query='select_one',
                                            select='yearday,watt',
                                            table='dayhours_e',
                                            id='year',
                                            item='2021')

        kwargs:
        :query= str
        :select= str
        :table= str
        :id= str
        :item= str
        :id2= str (optional)
        :item2= str (optional)
        ```
    - `retrieve_custom_data().get_yeardays(**kwargs)`
        ```
        returns list of all occuring day numbers (zero padded).
            given a weekday in a date period\n
            given a date period

        examples:
            get_yeardays(start=datetime(2021,1,1), end=datetime(2021,12,31), day='wednesday')\n
            get_yeardays(start=datetime(2021,3,1), end=datetime(2021,3,31))

        kwargs:
        :start= datetime(year,month,day)
        :end= datetime(year,month,day)
        :day= str e.g. 'monday'
        ```
    - `retrieve_custom_data().get_date_range_from_week(**kwargs)`
        ```
        returns start and enddate fomr given weeknumber in given year.
            source: http://mvsourcecode.com/python-how-to-get-date-range-from-week-number-mvsourcecode/

        example:
            get_date_range_from_week(year=2020,week=24)

        kwargs:
        :year= int
        :week= int
        ```
    - `retrieve_custom_data().get_dayhours_average(**kwargs)`
        ```
        gets data from table dayhours_X based on yearday numbers and return average for:
            :specified weekday in a year,
            :specified week in a year,
            :specified month in a year,
            :specified weekday in a month in a year.

        kwargs:
        :year= int: 2021
        :day= dayname
        :month= monthname
        :etype= 'E' or 'G'
        ```
- `LS120/read_youless.py` this file reads data from the youless returns it as a list \
 available functions are:
    - `read_youless().read_live()`
        ```
        read live energy data from Youless 120, only works with electricity.
        returns a json dictionary with data.

        example return:
            {'cnt': ' 29098,470', 'pwr': 581, 'lvl': 0, 'dev': '', 'det': '', 'con': 'OK', 'sts': '(48)', 'cs0': ' 0,000', 'ps0': 0, 'raw': 0}
        ```
    - `read_youless().read_minutes()`
        ```
        read per minute energy data from Youless 120, data is always 1 minute behind live.
        returns a dictionary with 2 lists consisting of time values and watts values.

        example return:
            {'time': ['value', 'value'], 'watts': ['value', 'value']}
        ```
    - `read_youless().read_ten_minutes(etype)`
        ```
        Read per ten minute data from Youless 120.
        Returned data is always 10 minutes behind last occuring rounded 10 minute interval.
            e.g. at 18.58hours the newest entry is 18.40hours and at 19.00hours it will be 18.50hours
        Returns dictionary with date as key containing a lists with time:value key/value dictionaries\n

        example:
            read_ten_minutes(etype)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        ```
    - `read_youless().read_days(etype)`
        ```
        read all Electricity or Gas hour values from Youless 120 with a maximum history of 70 days back (youless max).
        returns a list with tuples of data.

        example:
            read_days(etype)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        ```
    - `read_youless().read_months(etype)`
        ```
        Function to retrieve days per month from Youless 120 up to 11 months back for Electricity and Gas.
        returns a list with tuples of data.

        eaxmple:
            read_months(etype)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        ```
- `LS120/plotly_graphs/plot_data.py` this file converts data received in list form from db_retrieve_data.py and read_youless.py into a pandas dataframe and returns a plotly figure \
 available functions are:
    - `plot_dbdata().plot_hours(*args)`
        ```
        Reads from table dayhours_X and return figure.
            Plot hours from given starthour up to endhour.
            Plot spans a max of 2 days with a minimum of 1 hour and a maximum of 24 hours.

            Minimum arguments is 5, maximum is 7 in this order:
                :energytype: 'E', year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
                :energytype: 'E', year: 2021, month: 3, startday: 2, starthour: 5, endhour: 6
                :energytype: 'E', year: 2021, month: 3, startday: 2, starthour: 5

            plot_hours(arguments) examples:
                :plot_hours("E", 2021, 3, 2, 12, 3, 11)
                :plot_hours("E", 2021, 3, 2, 12, 11)
                :plot_hours("E", 2021, 3, 2, 12)
        ```
    - `plot_dbdata().plot_day_hour(year, month, day, etype)`
        ```
        Reads from table dayhours_X and return figure.
            Plot one day of the year into a graph with hourly totals.

            examples:
            :plot_day_hour(2021, 1, 19, 'E')
            :plot_day_hour(2021, January, 19, 'G')

            args:
            :year as integer
            :month as integer or string
            :day as integer
            :etype as string ('E' for Electricity, 'G' for Gas)
        ```
    - `plot_dbdata().plot_month_day(year, month, etype)`
        ```
        Reads from table yeardays_X and returns figure.
            plot one month of the year into a graph with daily totals.

            examples:
            :plot_month_day(2021, 1, 'E')
            :plot_month_day(2021, 'January', 'G')

            args:
            :year as integer
            :month as integer or string
            :etype as string ('E' for Electricity, 'G' for Gas)
        ```
    - `plot_dbdata().plot_year_day(year, etype)`
        ```
        Reads from table yeardays_X and returns figure.
            plot the year with daily totals into a graph.

            example:
            :plot_year_day(2021, 'E')

            args:
            :year as integer
            :etype as string ('E' for Electricity, 'G' for Gas)
        ```
    - `plot_dbdata().plot_year_month(year, etype)`
        ```
        Reads from table yeardays_X and returns figure.
            plot the year with month totals into a graph.

            example:
            :plot_year(2021, 'E')

            args:
            :year as integer
            :etype as string ('E' for Electricity, 'G' for Gas)
        ```
    - `plot_live().plot_live()`
        ```
        returns plotly graph with live information.

            example:
            :plot_live()
        ```
    - `plot_live().plot_live_minutes()`
        ```
        returns plotly graph with minute information up to 10 hours back.

            example:
            :plot_live_minutes()
        ```
    - `plot_live().plot_live_ten_minutes(**kwargs)`
        ```
        returns plotly graph with ten minute information up to 10 days back.
            :when supplied it returns a graph from date start=

            examples:
            :plot_live_ten_minutes(etype='E')
            :plot_live_ten_minutes(etype='G', start=datetime.datetime(2020, 1, 31, 0, 0))

            kwargs:
                :etype= str 'E' or 'G' (mandatory)
                :start= datetime.datetime object with date
                    example: datetime.datetime(2020, 1, 31, 0, 0)
        ```

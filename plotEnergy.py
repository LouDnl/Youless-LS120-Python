import sys, os, datetime, re, time
import calendar
import sqlite3 as sl
from sqlite3 import IntegrityError

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

DEBUG = True
def log(s):
    """
    Usage:
    log(lambda: "TEXT")
    log(lambda: "TEXT and %s" % variable)
    """
    if DEBUG:
        print(s())

dt = datetime.datetime.today() # get current datetime

# global variables
months = (range(1,13,1)) # url months
weeks = (range(1,54,1))  # url weeks
days = (range(1,32,1))   # url days
hours = (range(1,25,1))  # url hours
years = (range(2020, 2031, 1)) # years
date_now = dt
current_date = ("{:4d}{:02d}{:02d}".format(dt.year,dt.month,dt.day))
current_time = ("{:02d}{:02d}{:02d}".format(dt.hour,dt.minute,dt.second))
today = ("{:4d},{:02d},{:02d}".format(dt.year,dt.month,dt.day))
yesterday = ("{:4d},{:02d},{:02d}".format(dt.year,dt.month,dt.day-1))
day_now = date_now.day
month_now = date_now.month
year_now = date_now.year #% 100 # last two digits
last_year = date_now.year-1 # last year

class retrieveData:
    # global class variables
    # __cwd = os.getcwd() # get current working directory
    __path = "t:\\workspaces\\Atom\\Youless\\" # fixed path for now
    __dbname = "youless.db"

    def __init__(self):
        """
        Automatic database connection when called
        """
        self.__db_file = retrieveData.__path+retrieveData.__dbname
        log(lambda: "Starting database connection...")
        self.conn = None
        try:
            self.conn = sl.connect(self.__db_file)
            log(lambda: "Connected to: %s" % self.__db_file)
        except Error as e:
            log(lambda: e)

    def retrieve_day(self, year, month, day):
        """
        retrieve_day(2021, 1, 19) year as integer, month as integer and day as integer
        Retrieve day data for given year, month and day in a list with hours and kWh
        """
        self.year = year
        self.month = month
        self.day = day
        log(lambda: "Starting day retrieval %d %d %d" % (self.year, self.month, self.day))

        self.cur = self.conn.cursor()
        with self.conn:
            self.query = ("SELECT * FROM dayhours_e WHERE year = %s AND month = %s AND day = %s" % (str(self.year), str(self.month), str(self.day)))
            data = self.cur.execute(self.query)
            rows = len(self.cur.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query) # execute query again because fetchall() mangles the data to a list of tuples with strings
                for row in data:
                    tmp = row[7]
                    tmp = tmp.replace(" ", "")
                    tmp = tmp.replace("[", "")
                    tmp = tmp.replace("]", "")
                    tmp = tmp.split(',')
                    for v, n in enumerate(tmp):
                        tmp[v] = float(tmp[v])
            else:
                return 0

        self.conn.close()

        self.values = tmp[:]
        self.lst = [self.year,self.month,self.day,self.values]
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_month(self, year, month):
        """
        retrieve_month(2021, 1) year as integer and month as integer
        Retrieve monthdata for given year and month in a list with days and kWh
        """
        self.year = year
        self.month = month
        log(lambda: "Starting month retrieval %d %d" % (self.year, self.month))

        self.cur = self.conn.cursor()
        with self.conn:
            self.query = ("SELECT * FROM yeardays_e WHERE year = %s AND month = %s" % (str(self.year), str(self.month)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.conn.execute(self.query)
                for row in data:
                    tmp = row[4]
                    tmp = tmp.replace(" ", "")
                    tmp = tmp.replace("[", "")
                    tmp = tmp.replace("]", "")
                    tmp = tmp.split(',')
                    for v, n in enumerate(tmp):
                        tmp[v] = float(tmp[v])
            else:
                return 0

        self.conn.close()

        self.values = tmp[:] # copy tmp list to values list
        self.lst = [self.year,self.month,self.values]
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_year(self, year, type):
        """
        retrieve_year(2021, 1 or 2) year as integer, type as integer
        Retrieve available data for given year per month and day in kWh
        return either month totals or day totals for the entire year.
        1 is month totals
        2 is day totals
        """
        self.year = year
        self.type = type
        if (self.type != 1 and self.type != 2):
            log(lambda: "error: type can only be 1 or 2")
            return "error: type can only be 1 or 2"
        log(lambda: "Starting year retrieval %d" % (self.year))

        self.cur = self.conn.cursor()
        with self.conn:
            self.query = ("SELECT * FROM yeardays_e WHERE year = %s ORDER BY date" % (str(self.year)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)

            if (rows >= 1):
                data = self.conn.execute(self.query)
                self.lst = []
                for row in data:
                    tmp = row[4]
                    tmp = tmp.replace(" ", "")
                    tmp = tmp.replace("[", "")
                    tmp = tmp.replace("]", "")
                    tmp = tmp.split(',')
                    total = 0
                    for v, n in enumerate(tmp):
                        tmp[v] = float(tmp[v])
                        total += float(tmp[v])
                    if (self.type == 1): # month totals
                        tmplst = [[row[1], row[2], row[3], int(total)]]
                    elif (self.type == 2): # day totals
                        tmplst = [[row[1], row[2], row[3], tmp]]
                    self.lst.extend(tmplst)
                    tmplst.clear()
            else:
                return 0

        self.conn.close()

        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

class plotData:

    def __init__(self):
        self.DB = retrieveData()

    def plot_day_hour(self, year, month, day):
        """
        plot one day of the year into a graph
        plot_day_hour(2021, 1, 19) or plot_day_hour(2021, January, 19)
        year as integer, month as integer or string and day as integer
        """
        self.year = year
        self.month = month
        self.day = day
        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        # self.mNo = datetime.datetime.strftime(self.month, '%m')
        self.monthName = datetime.date(1900,self.month,1).strftime('%B')
        # log(lambda: (self.year,self.month,self.day))
        lst = self.DB.retrieve_day(self.year,self.month,self.day) # retrieve data from database
        if lst == 0:
            log(lambda: "No Data")
            return 0
        dict = {}
        high = max(lst[3]) + max(lst[3])/3
        totalWatt = 0
        for n, elem in enumerate(lst[3]):
            dict[n+1] = elem # Add watt values to dictionary with the hour as key
            totalWatt += elem

        df = pd.DataFrame(dict.items(), columns = ['Hour', 'Watt'])

        fig = px.bar(df, x=df["Hour"], y=df["Watt"], range_y=(0,high), title=("%s %d %d, total kWh: %g" % (self.monthName,self.day,self.year, float(totalWatt/1000))))
        log(lambda: "Plotting month %d day %d of year %d" % (self.month,self.day,self.year))
        # fig.show()
        return fig

    def plot_year_month(self, year, month):
        """
        plot one month of the year into a graph
        plot_year_month(2021, 1) or plot_year_mont(2021, January)
        year as integer and month as integer or string
        """
        self.year = year
        self.month = month
        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        # self.mNo = datetime.datetime.strftime(self.month, '%m')
        self.monthName = datetime.date(1900,self.month,1).strftime('%B')
        lst = self.DB.retrieve_month(self.year,self.month) # retrieve data from database
        if lst == 0:
            log(lambda: "No Data")
            return 0
        dict = {}
        high = max(lst[2]) + max(lst[2])/3
        # log(lambda: max(lst[2])
        # log(lambda: lst)
        totalkWh = 0
        for n, elem in enumerate(lst[2]):
            dict[n+1] = elem # Add kWh values to dictionary with the day as key
            totalkWh += elem

        df = pd.DataFrame(dict.items(), columns = ['Day', 'kWh'])

        fig = px.bar(df, x=df["Day"], y=df["kWh"], range_y=(0,high), title=("%s %d, total kWh: %g" % (self.monthName,self.year, totalkWh)))
        log(lambda: "Plotting month %d of year %d" % (self.month, self.year))
        # fig.show()
        return fig

    def plot_year_day(self, year):
        """
        plot the year with daily totals into a graph
        plot_year_day(2021) year as integer
        """
        self.year = year
        self.type = 2 # equals year with month totals
        lst = self.DB.retrieve_year(self.year, self.type)
        if lst == 0:
            log(lambda: "No Data")
            return 0
        # log(lambda: lst)
        dict = {}
        totalkWh = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            # log(lambda: n+1) # equals months
            self.month = int(lst[n][1])
            for y, value in enumerate(lst[n][3]):
                # log(lambda: "month %d day %d kwh %g" % (n+1, y+1, value)) # equals days
                # log(lambda: "%d-%d kwh: %g" % (y+1, n+1, value)) # equals days
                tempkey = ("%d-%d-%d" % (self.year,self.month,y+1)) # year-month-day
                dict[tempkey] = value
                totalkWh += value
                maxLst.append(value)
        # log(lambda: dict)
        high = max(maxLst) + max(maxLst)/3
        # log(lambda: totalkWh)
        # log(lambda: high)
        df = pd.DataFrame(dict.items(), columns = ['date', 'kwh'])
        # log(lambda: df["date"])
        fig = px.bar(df, x=df["date"], y=df["kwh"], range_y=(0,high), title=("year %d, total kWh: %g" % (self.year, totalkWh)))
        log(lambda: "Plotting year %d" % (self.year))
        # log(lambda: df)
        # fig.show()
        return fig

    def plot_year(self, year):
        """
        plot the year with month totals into a graph
        plot_year(2021) year as integer
        """
        self.year = year
        self.type = 1 # equals year with month totals
        lst = self.DB.retrieve_year(self.year, self.type)
        if lst == 0:
            log(lambda: "No Data")
            return 0
        dict = {}
        totalkWh = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            dict[lst[n][1]] = lst[n][3]
            totalkWh += lst[n][3]
            maxLst.append(lst[n][3])
        high = max(maxLst) + max(maxLst)/3

        df = pd.DataFrame(dict.items(), columns = ['month', 'kwh'])
        log(lambda: df)
        fig = px.bar(df, x=df["month"], y=df["kwh"], range_y=(0,high), title=("year %d, total kWh: %g" % (self.year, totalkWh)))
        log(lambda: "Plotting year %d" % (self.year))
        # fig.show()
        return fig


def dashtest():
    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    d_today = plotData().plot_day_hour(year_now,month_now,day_now)
    d_yesterday = plotData().plot_day_hour(year_now,month_now,day_now-1)
    d_currmonth = plotData().plot_year_month(2021,4)
    d_year1 = plotData().plot_year(2020)
    d_year2 = plotData().plot_year(2021)
    d_fullyear1 = plotData().plot_year_day(2020)
    d_fullyear2 = plotData().plot_year_day(2021)

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=d_today),
        dcc.Graph(figure=d_yesterday),
        dcc.Graph(figure=d_currmonth),
        dcc.Graph(figure=d_year1),
        dcc.Graph(figure=d_year2),
        dcc.Graph(figure=d_fullyear1),
        dcc.Graph(figure=d_fullyear2)
    ])

    app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

def main(*kwargs):
    dashtest()

if __name__ == '__main__':
        main()
        # main(21,22,23,24,25)


        # print("Month: %d Year: %d" % (int(self.month), int(self.year)))
        # for v, n in enumerate(self.values):
        #     print("Day: %d  kWh: %g" % (v+1, n))

        # print(lst)
        # print(dict)

        # df = pd.DataFrame([dict.keys(), dict.values()]).T
        # df.set_index('day', inplace=True)

        # df = pd.DataFrame.from_dict(dict, orient='index', columns = ['kWh'])


        # df = pd.Series(dict, name='kWh')
        # df.index.name = 'Day'
        # df.reset_index()

        # print(df)


        # fig = px.line(df, x = 'Date', y = 'kWh', title='Test Plot')
        # fig = go.Figure([go.Scatter(x = df['Date'], y = df['kWh'])])

        # fig =  go.Figure()
        # fig.add_trace(go.Bar(x=df.index,y=df["kWh"]))

        # fig.update_layout(
        #     xaxis = dict(
        #         tickmode = 'array',
        #         tickvals = df.index
        #         ticktext = df['Day']
        #     )
        # )
        # self.values = tmp[:] # copy tmp list to values list
        # self.lst = [self.year,self.month,self.values]
        # for i in self.lst:
        #     log(lambda: i)

    # def create_connection(self, db_file):
    #     """
    #     Function to create a connection to the database
    #     """
    #     log(lambda: "Starting database connection...")
    #     self.conn = None
    #     try:
    #         self.conn = sl.connect(db_file)
    #         log(lambda: "Connected to: %s" % db_file)
    #     except Error as e:
    #         log(lambda: e)
    #     return self.conn

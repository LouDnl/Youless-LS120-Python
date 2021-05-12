import sys, os, datetime, re, time, locale
import calendar
import sqlite3 as sl
from sqlite3 import IntegrityError
import ast # for converting string representation of a list to a list

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# import globals
# import globals as gl
from globals import *

# set language
locale.setlocale(locale.LC_ALL, Vars.web("LOCALE"))

class retrieveData:
    # global class variables
    __path = Vars.path + Vars.dbname

    def __init__(self):
        """
        Automatic database connection when called
        """
        self.__db_file = retrieveData.__path
        log(lambda: "Starting database connection...")
        self.conn = None
        try:
            self.conn = sl.connect(self.__db_file)
            log(lambda: "Connected to: %s" % self.__db_file)
        except Error as e:
            log(lambda: e)

    def retrieve_hours(self, table, year, month, startday, starthour, *args):
        """
        Retrieve data from table dayhours_X.
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
        """
        self.table = table
        self.year = year
        self.month = month
        self.startday = startday
        self.starthour = starthour
        self.hourlist = []
        if (len(args) == 2):
            self.endday = args[0]
            self.endhour = args[1]
            self.query = (Vars.conf("queries")["s_dayhours2"] % (self.table, self.year, self.month, self.startday, self.endday))
            self.lst = [self.year,self.month,self.startday,self.starthour,self.endday,self.endhour,self.hourlist]
        elif (len(args) == 1):
            self.endhour = args[0]
            self.query = (Vars.conf("queries")["s_dayhours"] % (self.table, self.year, self.month, self.startday))
            self.lst = [self.year,self.month,self.startday,self.starthour,self.endhour,self.hourlist]
        else:
            self.query = (Vars.conf("queries")["s_dayhours"] % (self.table, self.year, self.month, self.startday))
            self.lst = [self.year,self.month,self.startday,self.starthour,self.hourlist]

        # self.__QQ = Vars.conf("queries")["s_dayhours2"] if self.__Q == 2 else Vars.conf("queries")["s_dayhours"]

        # if (self.__Q == 2):
        #     log(lambda: self.__QQ)
        #     log(lambda: (self.__QQ % (self.table, self.year, self.month, self.startday, self.endday)))

        log(lambda: "Starting hour retrieval from table %s" % self.table)

        self.cur = self.conn.cursor()
        with self.conn:
            # self.query = (self.__QQ % (self.table, self.year, self.month, self.startday, self.endday)) if self.__Q == 2 else (self.__QQ % (self.table, self.year, self.month, self.startday))
            # dbg(lambda: self.query)
            data = self.cur.execute(self.query)
            rows = (len(self.cur.fetchall()))
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query) # execute query again because fetchall() mangles the data to a list of tuples with strings
                rowcount = 0
                for row in data:
                    rowcount += 1
                    # dbg(lambda: row)
                    self.values = row[7] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list

                    for n, v in enumerate(self.values):
                        self.values[n] = int(self.values[n])
                        if (rowcount == 1) and (n >= self.starthour):
                            self.hourlist.append((n, v))
                            if (len(args) == 1) and (n == self.endhour):
                                break
                        elif (rowcount == 2) and (n <= self.endhour):
                            self.hourlist.append((n, v))
                    # dbg(lambda: self.hourlist)

            else:
                return 0

        self.conn.close()
        # dbg(lambda: self.lst)
        # self.values = tmp[:]

        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_day(self, year, month, day, table):
        """
        Retrieve data from table dayhours_X.
        Retrieves day data for given year, month and day in a list with hours and values.
        retrieve_day(2021, 1, 19, 'dayhours_e')
        year as integer
        month as integer
        day as integer
        table as string
        """
        self.year = year
        self.month = month
        self.day = day
        self.table = table
        log(lambda: "Starting day retrieval %d %d %d from table %s" % (self.year, self.month, self.day, self.table))

        self.cur = self.conn.cursor()
        with self.conn:
            #self.query = ("SELECT * FROM dayhours_e WHERE year = %s AND month = %s AND day = %s" % (str(self.year), str(self.month), str(self.day)))
            self.query = (Vars.conf("queries")["s_dayhours"] % (self.table, str(self.year), str(self.month), str(self.day)))
            data = self.cur.execute(self.query)
            rows = len(self.cur.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query) # execute query again because fetchall() mangles the data to a list of tuples with strings
                for row in data:
                    self.values = row[7] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list
                #     tmp = row[7]
                #     tmp = tmp.replace(" ", "")
                #     tmp = tmp.replace("[", "")
                #     tmp = tmp.replace("]", "")
                #     tmp = tmp.split(',')
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
            else:
                return 0

        self.conn.close()

        # self.values = tmp[:]
        self.lst = [self.year,self.month,self.day,self.values]
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_month(self, year, month, table):
        """
        Retrieve data from table yeardays_X.
        Retrieves monthdata for given month of given year in a list with days and values
        retrieve_month(2021, 1, 'yeardays_e')
        year as integer
        month as integer
        table as string
        """
        self.year = year
        self.month = month
        self.table = table
        log(lambda: "Starting month retrieval %d %d from table %s" % (self.year, self.month, self.table))

        self.cur = self.conn.cursor()
        with self.conn:
            #self.query = ("SELECT * FROM yeardays_e WHERE year = %s AND month = %s" % (str(self.year), str(self.month)))
            self.query = (Vars.conf("queries")["s_yeardays"] % (self.table, str(self.year), str(self.month)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.conn.execute(self.query)
                for row in data:
                    self.values = row[4] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list
                    # tmp = row[4]
                    # tmp = tmp.replace(" ", "")
                    # tmp = tmp.replace("[", "")
                    # tmp = tmp.replace("]", "")
                    # tmp = tmp.split(',')
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
            else:
                return 0

        self.conn.close()

        # self.values = tmp[:] # copy tmp list to values list
        self.lst = [self.year,self.month,self.values]
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_year(self, year, totals, table):
        """
        Retrieve data from table yeardays_X.
        Retrieves available data for given year per month and day in values
        Returns either month totals or day totals for the entire year.
        retrieve_year(2021, 2, 'yeardays_g')
        year as integer
        totals as integer (1 is month totals, 2 is day totals)
        table as string
        """
        self.year = year
        self.totals = totals
        self.table = table

        if (self.totals != 1 and self.totals != 2):
            log(lambda: "error: type can only be 1 or 2")
            return "error: type can only be 1 or 2"
        log(lambda: "Starting year retrieval %d" % (self.year))

        self.cur = self.conn.cursor()
        with self.conn:
            # self.query = ("SELECT * FROM yeardays_e WHERE year = %s ORDER BY date" % (str(self.year)))
            self.query = (Vars.conf("queries")["so_yeardays"] % (self.table, str(self.year)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)

            if (rows >= 1):
                data = self.conn.execute(self.query)
                self.lst = []
                for row in data:
                    self.values = row[4] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list
                    # tmp = row[4]
                    # tmp = tmp.replace(" ", "")
                    # tmp = tmp.replace("[", "")
                    # tmp = tmp.replace("]", "")
                    # tmp = tmp.split(',')
                    total = 0
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
                        total += float(self.values[v])
                    if (self.totals == 1): # month totals
                        self.tmplst = [[row[1], row[2], row[3], int(total)]]
                    elif (self.totals == 2): # day totals
                        self.tmplst = [[row[1], row[2], row[3], self.values]]
                    self.lst.extend(self.tmplst)
                    self.tmplst.clear()
            else:
                return 0

        self.conn.close()

        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

class plotData:

    def __init__(self):
        self.DB = retrieveData()

    def plot_hours(self, *args):
        """
        Reads from table dayhours_X.
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
        """
        if (len(args) > 7):
            return log(lambda: "Maximum arguments of 7 exceeded")
        elif (len(args) < 5):
            return log(lambda: "Minimum arguments is 5")

        self.etype = args[0]
        self.table = Vars.conf("dbtables")[self.etype][1]
        self.year = args[1]
        self.month = args[2]
        self.startday = args[3]
        self.starthour = args[4]
        if (len(args) == 7):
            self.endday = args[5]
            self.endhour = args[6]
            lst = self.DB.retrieve_hours(self.table,self.year,self.month,self.startday,self.starthour,self.endday,self.endhour) # retrieve data from database
        elif (len(args) == 6):
            self.endhour = args[5]
            lst = self.DB.retrieve_hours(self.table,self.year,self.month,self.startday,self.starthour,self.endhour) # retrieve data from database
        else:
            lst = self.DB.retrieve_hours(self.table,self.year,self.month,self.startday,self.starthour) # retrieve data from database

        if lst == 0:
            log(lambda: "No Data")
            return 0

        self.columns = [Vars.lang("U"), Vars.lang("W"), Vars.lang("KWH")] if self.etype == 'E' else [Vars.lang("U"), Vars.lang("L"), Vars.lang("M3")] if self.etype == 'G' else None

        self.hours = lst[-1]
        data = {}
        highlst = []
        total = 0
        for n, v in enumerate(self.hours):
            data[self.hours[n][0]] = int(self.hours[n][1])
            highlst.append(self.hours[n][1])
            total += int(self.hours[n][1])
            # dbg(lambda: self.hours[n])
        high = int(max(highlst) + max(highlst)/3)

        df = pd.DataFrame(data.items(), columns = self.columns[:2])
        dbg(lambda: df)

        self.month = datetime.date(1900,int(self.month),1).strftime('%B')

        self.title = (
            Vars.lang('dayhourtitle') % (self.month, self.startday, self.year, self.columns[1], int(total/1000), self.columns[2])
            if (self.endday in locals())
            else Vars.lang('customhourtitle') % (self.month, self.startday, self.endday, self.year, self.columns[1], int(total/1000), self.columns[2]))

        fig = px.bar(
            df,
            x = df[self.columns[0]],
            y = df[self.columns[1]],
            range_y = (0,high),
            title = (self.title),
        )
        fig.update_layout(
            xaxis_type = 'category' # change x axis type so that plotly does not arrange overlapping day hours
        )
        # log(lambda: "Plotting month %d day %d of year %d from table %s" % (self.month, self.day, self.year, self.table))
        fig.show()

        dbg(lambda: fig)
        return fig

    def plot_day_hour(self, year, month, day, etype):
        """
        Reads from table dayhours_X
        Plot one day of the year into a graph with hourly totals.
        plot_day_hour(2021, 1, 19, 'E') or plot_day_hour(2021, January, 19, 'G')
        year as integer
        month as integer or string
        day as integer
        etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.month = month
        self.day = day
        self.etype = etype
        self.table = Vars.conf("dbtables")[self.etype][1]
        self.columns = [Vars.lang("U"), Vars.lang("W"), Vars.lang("KWH")] if self.etype == 'E' else [Vars.lang("U"), Vars.lang("L"), Vars.lang("M3")] if self.etype == 'G' else None

        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        # self.mNo = datetime.datetime.strftime(self.month, '%m')
        self.monthName = datetime.date(1900,self.month,1).strftime('%B')
        # log(lambda: (self.year,self.month,self.day))
        lst = self.DB.retrieve_day(self.year,self.month,self.day,self.table) # retrieve data from database
        if lst == 0:
            log(lambda: "No Data")
            return 0
        data = {}
        high = max(lst[3]) + max(lst[3])/3
        totalWatt = 0
        for n, elem in enumerate(lst[3]):
            data[n+1] = elem # Add watt values to dictionary with the hour as key
            totalWatt += elem

        df = pd.DataFrame(data.items(), columns = self.columns[:2])

        fig = px.bar(
            df,
            x = df[self.columns[0]],
            y = df[self.columns[1]],
            range_y = (0,high),
            title = (Vars.lang('dayhourtitle') % (self.monthName, self.day, self.year, self.columns[1], float(totalWatt/1000), self.columns[2])),
            # labels = {
            #     "Hour": Vars.lang('U'),
            #     "Watt": Vars.lang('WH')
            # }
        )
        log(lambda: "Plotting month %d day %d of year %d from table %s" % (self.month, self.day, self.year, self.table))
        # fig.show()
        return fig

    def plot_month_day(self, year, month, etype):
        """
        Reads from table yeardays_X
        plot one month of the year into a graph with daily totals.
        plot_year_month(2021, 1, 'E') or plot_year_month(2021, January, 'G')
        year as integer
        month as integer or string
        etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.month = month
        self.etype = etype
        self.table = Vars.conf("dbtables")[self.etype][0]
        self.columns = [Vars.lang("D"), Vars.lang("KH"), Vars.lang("KWH")] if self.etype == 'E' else [Vars.lang("D"), Vars.lang("KM"), Vars.lang("M3")] if self.etype == 'G' else None

        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        # self.mNo = datetime.datetime.strftime(self.month, '%m')
        self.monthName = datetime.date(1900,self.month,1).strftime('%B')
        lst = self.DB.retrieve_month(self.year, self.month, self.table) # retrieve data from database
        if lst == 0:
            log(lambda: "No Data")
            return 0
        data = {}
        high = max(lst[2]) + max(lst[2])/3
        # log(lambda: max(lst[2])
        # log(lambda: lst)
        totalkWh = 0
        for n, elem in enumerate(lst[2]):
            data[n+1] = elem # Add kWh values to dictionary with the day as key
            totalkWh += elem

        df = pd.DataFrame(data.items(), columns = self.columns[:2])#['Day', 'kWh'])

        # lendf = len(df['Day'])
        # firstdf =df['Day'][0]
        lastdf = df[self.columns[0]][len(df[self.columns[0]]) - 1]
        # log(lambda: last)
        # log(lambda: type(df["Day"]))

        fig = px.bar(
            df,
            x = df[self.columns[0]],
            y = df[self.columns[1]],
            range_y = (0, high),
            # range_x = (0, lastdf),

            title=(Vars.lang('yearmonthtitle') % (self.monthName, self.year, self.columns[1], totalkWh, self.columns[2])),
            # labels = {
            #     "Day": Vars.lang('D'),
            #     "kWh": Vars.lang('KH')
            # }
        )
        log(lambda: "Plotting month %d of year %d" % (self.month, self.year))
        # fig.show()
        return fig

    def plot_year_day(self, year, etype):
        """
        Reads from table yeardays_X
        plot the year with daily totals into a graph
        plot_year_day(2021, 'E')
        year as integer
        etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.etype = etype
        self.table = Vars.conf("dbtables")[self.etype][0]
        self.columns = [Vars.lang("D"), Vars.lang("KH"), Vars.lang("KWH")] if self.etype == 'E' else [Vars.lang("D"), Vars.lang("KM"), Vars.lang("M3")] if self.etype == 'G' else None
        self.type = 2 # equals year with month totals
        lst = self.DB.retrieve_year(self.year, self.type, self.table)
        if lst == 0:
            log(lambda: "No Data")
            return 0
        # log(lambda: lst)
        data = {}
        totalkWh = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            # log(lambda: n+1) # equals months
            self.month = int(lst[n][1])
            for y, value in enumerate(lst[n][3]):
                # log(lambda: "month %d day %d kwh %g" % (n+1, y+1, value)) # equals days
                # log(lambda: "%d-%d kwh: %g" % (y+1, n+1, value)) # equals days
                tempkey = ("%d-%d-%d" % (self.year,self.month,y+1)) # year-month-day
                data[tempkey] = value
                totalkWh += value
                maxLst.append(value)
        # log(lambda: dict)
        high = max(maxLst) + max(maxLst)/3
        # log(lambda: totalkWh)
        # log(lambda: high)
        df = pd.DataFrame(data.items(), columns = self.columns[:2])
        # log(lambda: df["date"])
        fig = px.bar(
            df,
            x = df[self.columns[0]],
            y = df[self.columns[1]],
            range_y = (0,high),
            # title = (Items.lang('yeardaytitle') % (self.year, totalkWh)),
            title = (Vars.lang('yeardaytitle') % (self.year, self.columns[1], totalkWh, self.columns[2])),
            # labels = {
            #     "date": Items.lang('DT'),
            #     "kwh": Items.lang('KH')
            # }
        )
        log(lambda: "Plotting year %d" % (self.year))
        # log(lambda: df)
        # fig.show()
        return fig

    def plot_year_month(self, year, etype):
        """
        plot the year with month totals into a graph
        plot_year(2021) year as integer
        """
        self.year = year
        self.etype = etype
        self.table = Vars.conf("dbtables")[self.etype][0]
        self.columns = [Vars.lang("M"), Vars.lang("KH"), Vars.lang("KWH")] if self.etype == 'E' else [Vars.lang("M"), Vars.lang("KM"), Vars.lang("M3")] if self.etype == 'G' else None
        self.type = 1 # equals year with month totals
        lst = self.DB.retrieve_year(self.year, self.type, self.table)
        if lst == 0:
            log(lambda: "No Data")
            return 0
        data = {}
        months = {}
        totalkWh = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            data[lst[n][1]] = lst[n][3]
            months[lst[n][1]] = datetime.date(1900,int(lst[n][1]),1).strftime('%B')
            totalkWh += lst[n][3]
            maxLst.append(lst[n][3])
        high = max(maxLst) + max(maxLst)/3
        # dbg(lambda: months.items())
        df = pd.DataFrame(data.items(), columns = (self.columns[:2]))
        # df = pd.DataFrame(data, columns = (self.columns[:2]))
        # dbg(lambda: df)
        fig = px.bar(
            df,
            x = df[self.columns[0]],
            y = df[self.columns[1]],
            range_y = (0,high),
            # title = (Vars.lang('yeartitle') % (self.year, totalkWh)),
            title = (Vars.lang('yeartitle') % (self.year, self.columns[1], totalkWh, self.columns[2])),
            # labels = {
            #     "month": Vars.lang('M'),
            #     "kwh": Vars.lang('KH')
            # }
        )
        # mn = []
        # for n in df[self.columns[0]]:
        #                 n = datetime.date(1900,int(n),1).strftime('%B')
        #                 mn.append(n)
        # dbg(lambda: mn)
        # dbg(lambda: list(months.values()))
        fig.update_layout(
            # xaxis_tickformat = '%b'
            xaxis=dict(
                tickmode = 'array',
                tickvals = list(months.keys()),
                ticktext = list(months.values())
            )
        )
        log(lambda: "Plotting year %d" % (self.year))
        # fig.show()
        return fig


# def DashDebug():
#     import dash
#     import dash_core_components as dcc
#     import dash_html_components as html
#
#     # d_today = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now)
#     # d_yesterday = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now-1)
#     d_currmonth = plotData().plot_year_month(Runtime.year_now, Runtime.month_now)
#     # d_lastmonth = plotData().plot_year_month(Runtime.year_now, Runtime.last_month)
#     # d_year1 = plotData().plot_year(Runtime.year_now)
#     # d_year2 = plotData().plot_year(Runtime.last_year)
#     # d_fullyear1 = plotData().plot_year_day(Runtime.year_now)
#     # d_fullyear2 = plotData().plot_year_day(Runtime.last_year)
#
#     app = dash.Dash()
#     app.layout = html.Div([
#         # dcc.Graph(figure=d_today),
#         # dcc.Graph(figure=d_yesterday),
#         dcc.Graph(figure=d_currmonth),
#         # dcc.Graph(figure=d_lastmonth),
#         # dcc.Graph(figure=d_year1),
#         # dcc.Graph(figure=d_year2),
#         # dcc.Graph(figure=d_fullyear1),
#         # dcc.Graph(figure=d_fullyear2)
#     ])
#
#     app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

def main():#*kwargs):
    # retrieveData().retrieve_day(2021,2,27)
    # retrieveData().retrieve_year(2021, 2, "yeardays_e")
    # DashDebug()
    # retrieveData().retrieve_hours('dayhours_g', 2021, 3, 2, 3, 3, 6) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
    # retrieveData().retrieve_hours('dayhours_e', 2021, 2, 1, 12) # year: 2020, month: 10, startday: 1, starthour: 12
    # retrieveData().retrieve_hours('dayhours_e', 2021, 3, 2, 11, 18) # year: 2020, month: 11, startday: 2, starthour: 11, endhour: 18
    # plotData().plot_hours('G', 2021, 3, 2, 3, 3, 6) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
    plotData().plot_hours('E', 2021, 4, 18, 18, 19, 23) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
    # plotData().plot_hours('E', 2021, 2, 1, 12) # year: 2020, month: 10, startday: 1, starthour: 12
    # plotData().plot_hours('E', 2021, 3, 2, 11, 18) # year: 2020, month: 11, startday: 2, starthour: 11, endhour: 18
    # plotData().plot_hours(1,2,3,4,5,6,7,8)
    # plotData().plot_hours(1,2,3,4)
    # plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now,"G")
    # plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now,"E")
    # plotData().plot_month_day(2021,4,'E')
    # plotData().plot_month_day(2021,4,'G')
    # plotData().plot_year_day(2020,'E')
    # plotData().plot_year_day(2020,'G')
    # plotData().plot_year_month(2020,'G')
    # plotData().plot_year_month(2021,'E')
    log(lambda: "I function...")

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

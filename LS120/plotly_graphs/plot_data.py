#!/usr/bin/env python3
"""
    File name: plot_data.py
    Author: LouDFPV
    Date created: 15/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    This file converts data received in list form from db_retrieve_data.py and read_youless.py into a pandas dataframe and returns a plotly figure
"""
import datetime
# initialize logging
import logging

# pandas dataframe
import pandas as pd
# plotly figure
import plotly.express as px

# Youless setup
from LS120 import Runtime, Youless, read_youless, retrieve_data

logger = logging.getLogger(__name__)
logger.debug("plot_data loaded")

# set language
Youless.youless_locale()

livedict = Youless.live_dict  # dictionary for temporary storage of live values


class plot_dbdata:
    """class to convert retrieved data from the youless database to plotly figures."""

    def __init__(self) -> None:
        self.data = retrieve_data()

    def plot_hours(self, *args):
        """Reads from table dayhours_X and return figure.
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
        """
        if (len(args) > 7):
            return logger.warning("Maximum arguments of 7 exceeded")
        elif (len(args) < 5):
            return logger.warning("Minimum arguments is 5")

        self.etype = args[0]
        self.table = Youless.sql("dbtables")[self.etype][1]
        self.year = args[1]
        self.month = args[2]
        self.startday = args[3]
        self.starthour = args[4]
        if (len(args) == 7):
            self.endday = args[5]
            self.endhour = args[6]
            lst = self.data.retrieve_hours(self.table, self.year, self.month, self.startday, self.starthour, self.endday, self.endhour)  # retrieve data from database
        elif (len(args) == 6):
            self.endhour = args[5]
            lst = self.data.retrieve_hours(self.table, self.year, self.month, self.startday, self.starthour, self.endhour)  # retrieve data from database
        else:
            lst = self.data.retrieve_hours(self.table, self.year, self.month, self.startday, self.starthour)  # retrieve data from database

        if lst == 0:
            logger.error("No Data")
            return 0

        self.columns = [Youless.lang("U"), Youless.lang("W"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("U"), Youless.lang("L"), Youless.lang("M3")] if self.etype == 'G' else None

        self.hours = lst[-1]
        data = {}
        highlst = []
        total = 0
        for n, v in enumerate(self.hours):
            data[self.hours[n][0]] = int(self.hours[n][1])
            highlst.append(self.hours[n][1])
            total += int(self.hours[n][1])
        high = int(max(highlst) + max(highlst)/3)

        df = pd.DataFrame(data.items(), columns=self.columns[:2])
        logger.debug(df)

        self.month = datetime.date(1900, int(self.month), 1).strftime('%B')

        self.title = (
            Youless.lang('dayhourtitle') % (self.month, self.startday, self.year, self.columns[1], int(total/1000), self.columns[2])
            if ('endday' not in dir(self))
            else Youless.lang('customhourtitle') % (self.startday, self.endday, self.month, self.year, self.columns[1], int(total/1000), self.columns[2]))

        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),
            title=(self.title),
            height=500,
        )
        fig.update_layout(
            xaxis_type='category'  # change x axis type so that plotly does not arrange overlapping day hours
        )

        logger.debug(fig)
        return fig

    def plot_day_hour(self, year, month, day, etype):
        """Reads from table dayhours_X and return figure.
        Plot one day of the year into a graph with hourly totals.

        examples:
        :plot_day_hour(2021, 1, 19, 'E')
        :plot_day_hour(2021, January, 19, 'G')

        args:
        :year as integer
        :month as integer or string
        :day as integer
        :etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.month = month
        self.day = day
        self.etype = etype
        self.table = Youless.sql("dbtables")[self.etype][1]
        self.columns = [Youless.lang("U"), Youless.lang("W"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("U"), Youless.lang("L"), Youless.lang("M3")] if self.etype == 'G' else None

        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        self.monthName = datetime.date(1900, self.month, 1).strftime('%B')
        lst = self.data.retrieve_day(self.year, self.month, self.day, self.table)  # retrieve data from database
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        high = max(lst[3]) + max(lst[3])/3
        totalWatt = 0
        for n, elem in enumerate(lst[3]):
            data[n+1] = elem  # Add watt values to dictionary with the hour as key
            totalWatt += elem

        df = pd.DataFrame(data.items(), columns=self.columns[:2])

        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),
            title=(Youless.lang('dayhourtitle') % (self.monthName, self.day, self.year, self.columns[1], float(totalWatt/1000), self.columns[2])),
        )
        logger.debug("Plotting month %d day %d of year %d from table %s" % (self.month, self.day, self.year, self.table))
        return fig

    def plot_month_day(self, year, month, etype):
        """Reads from table yeardays_X and returns figure.
        plot one month of the year into a graph with daily totals.

        examples:
        :plot_month_day(2021, 1, 'E')
        :plot_month_day(2021, 'January', 'G')

        args:
        :year as integer
        :month as integer or string
        :etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.month = month
        self.etype = etype
        self.table = Youless.sql("dbtables")[self.etype][0]
        self.columns = [Youless.lang("D"), Youless.lang("KH"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("D"), Youless.lang("KM"), Youless.lang("M3")] if self.etype == 'G' else None

        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        self.monthName = datetime.date(1900, self.month, 1).strftime('%B')
        lst = self.data.retrieve_month(self.year, self.month, self.table)  # retrieve data from database
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        high = max(lst[2]) + max(lst[2])/3
        totalUsage = 0
        for n, elem in enumerate(lst[2]):
            data[n+1] = elem  # Add kWh values to dictionary with the day as key
            totalUsage += elem

        df = pd.DataFrame(data.items(), columns=self.columns[:2])

        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),

            title=(Youless.lang('yearmonthtitle') % (self.monthName, self.year, self.columns[1], totalUsage, self.columns[2])),
        )
        logger.debug("Plotting month %d of year %d" % (self.month, self.year))
        return fig

    def plot_year_day(self, year, etype):
        """Reads from table yeardays_X and returns figure.
        plot the year with daily totals into a graph.

        example:
        :plot_year_day(2021, 'E')

        args:
        :year as integer
        :etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.etype = etype
        self.table = Youless.sql("dbtables")[self.etype][0]
        self.columns = [Youless.lang("D"), Youless.lang("KH"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("D"), Youless.lang("KM"), Youless.lang("M3")] if self.etype == 'G' else None
        self.type = 2  # equals year with month totals
        lst = self.data.retrieve_year(self.year, self.type, self.table)
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        totalUsage = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            self.month = int(lst[n][1])
            for y, value in enumerate(lst[n][3]):
                tempkey = ("%d-%d-%d" % (self.year, self.month, y+1))  # year-month-day
                data[tempkey] = value
                totalUsage += value
                maxLst.append(value)
        high = max(maxLst) + max(maxLst)/3
        df = pd.DataFrame(data.items(), columns=self.columns[:2])
        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),
            title=(Youless.lang('yeardaytitle') % (self.year, self.columns[1], totalUsage, self.columns[2])),
        )
        logger.debug("Plotting year %d" % (self.year))
        return fig

    def plot_year_month(self, year, etype):
        """Reads from table yeardays_X and returns figure.
        plot the year with month totals into a graph.

        example:
        :plot_year(2021, 'E')

        args:
        :year as integer
        :etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.etype = etype
        self.table = Youless.sql("dbtables")[self.etype][0]
        self.columns = [Youless.lang("M"), Youless.lang("KH"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("M"), Youless.lang("KM"), Youless.lang("M3")] if self.etype == 'G' else None
        self.type = 1  # equals year with month totals
        lst = self.data.retrieve_year(self.year, self.type, self.table)
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        months = {}
        totalUsage = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            data[lst[n][1]] = lst[n][3]
            months[lst[n][1]] = datetime.date(1900, int(lst[n][1]), 1).strftime('%B')
            totalUsage += lst[n][3]
            maxLst.append(lst[n][3])
        high = max(maxLst) + max(maxLst)/3
        df = pd.DataFrame(data.items(), columns=(self.columns[:2]))
        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),
            title=(Youless.lang('yeartitle') % (self.year, self.columns[1], totalUsage, self.columns[2])),
        )
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(months.keys()),
                ticktext=list(months.values())
            )
        )
        logger.debug("Plotting year %d" % (self.year))
        return fig


class plot_live:
    """class to convert retrieved data from the youless device to plotly figures."""

    def __init__(self) -> None:
        pass

    def plot_live(self):
        """returns plotly graph with live information.

        example:
        :plot_live()
        """
        date = Runtime.td('date_live')
        time = Runtime.td('secs_live')
        if (len(livedict['timelst']) == 20):
            livedict['timelst'].pop(0)
        livedict['timelst'].append(time)

        lvd = read_youless().read_live()
        live = lvd['pwr']
        if (len(livedict['wattlst']) == 20):
            livedict['wattlst'].pop(0)
        livedict['wattlst'].append(live)

        total = lvd['cnt']
        graphtitle = Youless.lang('livegraphtitle').format(live, date, time, total, Youless.lang('KWH'))
        maxusage = max(livedict['wattlst'])

        fig = px.line(
            x=livedict['timelst'],
            y=livedict['wattlst'],
            title=graphtitle,
            range_y=(0, (maxusage + (maxusage / 3))),
            width=500,  # static figure widt
            # height = (maxusage + (maxusage / 3) # calculate max figure height
            height=500,  # static figure height
            labels={
                "x": Youless.lang('T'),  # x-axis naming
                "y": Youless.lang('W')  # y-axis naming
            })
        logger.debug("Plotting live %s %s" % (date, time))
        return fig

    def plot_live_minutes(self):
        """returns plotly graph with minute information up to 10 hours back.

        example:
        :plot_live_minutes()
        """
        date = Runtime.td('date_live')
        time = Runtime.td('time_live')
        e = read_youless().read_minutes()
        live = e['watts'][-1]
        # maxusage = max(e['watts']) # variable to calculate max height of figure
        graphtitle = Youless.lang('liveminutegraphtitle').format(live, date, time)
        fig = px.line(
            x=e['time'],
            y=e['watts'],
            title=graphtitle,
            # width=1300,  # static figure width
            # height=(maxusage + (maxusage / 3)  # calculate max figure height
            height=500,  # static figure height
            labels={
                "x": Youless.lang('T'),  # x-axis naming
                "y": Youless.lang('W')  # y-axis naming
            }
        )
        logger.debug("Plotting live minutes %s %s" % (date, time))
        return fig

    def plot_live_ten_minutes(self, **kwargs):
        """returns plotly graph with ten minute information up to 10 days back.
        :when supplied it returns a graph from date start=

        examples:
        :plot_live_ten_minutes(etype='E')
        :plot_live_ten_minutes(etype='G', start=datetime.datetime(2020, 1, 31, 0, 0))

        kwargs:
             :etype= str 'E' or 'G' (mandatory)
             :start= datetime.datetime object with date
                example: datetime.datetime(2020, 1, 31, 0, 0)
        """
        if 'etype' not in kwargs:
            return None
        else:
            self.etype = kwargs.get('etype')
            self.ename = Youless.lang("W") if self.etype == 'E' else Youless.lang("L") if self.etype == 'G' else None

        if 'start' in kwargs:
            self.start_date = kwargs.get('start')  # 2021-01-01 00:00:00 <class 'datetime.datetime'>

        date_now = Runtime.td('date_live')
        time_now = Runtime.td('time_live')
        d = read_youless().read_ten_minutes(self.etype)
        today = d.get(Runtime.td('current_date'))
        live_usage = list(today[1][0].values())[0]
        graphtitle = Youless.lang('tenminutegraphtitle').format(live_usage, self.ename, date_now, time_now)

        if 'start_date' in dir(self):
            del_lst = []
            for key in d.keys():
                s_key = datetime.datetime.strptime(key, '%Y-%m-%d')  # 2021-01-01 00:00:00 <class 'datetime.datetime'>
                if self.start_date > s_key:
                    del_lst.append(key)
            for i in del_lst:
                del d[i]

        fig_dict = {}  # dictionary for storing date time, values
        date_time = []  # list for storing date time strings
        values = []  # list for storing usage values
        for key in d.keys():  # for date key in d
            for sub_key in d[key][1]:  # for every time key in the list
                date_time.append(f'{key} {list(sub_key.keys())[0]}')
                values.append(list(sub_key.values())[0])
        fig_dict['time'] = date_time
        fig_dict['usage'] = values

        fig = px.line(
            x=fig_dict['time'],
            y=fig_dict['usage'],
            title=graphtitle,
            height=500,  # static figure height
            labels={
                "x": Youless.lang('T'),  # x-axis naming
                "y": self.ename  # y-axis naming
            }
        )
        logger.debug("Plotting live ten minutes %s %s" % (date_now, time_now))
        return fig

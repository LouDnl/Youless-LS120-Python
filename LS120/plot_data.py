#!/usr/bin/env python3
"""
   plot_data.py

   This file converts data received in list form from read_data.py into a pandas dataframe and returns a plotly figure
"""
import sys
import datetime

# pandas dataframe
import pandas as pd

# plotly figure
import plotly.express as px

# Youless setup
from .settings import Youless
from .read_data import read_data

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("plot_data.py started")

# set language
Youless.youless_locale()


class plot_data:
    """
        class to convert list to plotly figure
    """

    def __init__(self):
        self.DB = read_data()

    def plot_hours(self, *args):
        """
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
        """
        if (len(args) > 7):
            return logger.info("Maximum arguments of 7 exceeded")
        elif (len(args) < 5):
            return logger.info("Minimum arguments is 5")

        self.etype = args[0]
        self.table = Youless.sql("dbtables")[self.etype][1]
        self.year = args[1]
        self.month = args[2]
        self.startday = args[3]
        self.starthour = args[4]
        if (len(args) == 7):
            self.endday = args[5]
            self.endhour = args[6]
            lst = self.DB.retrieve_hours(self.table, self.year, self.month, self.startday, self.starthour, self.endday, self.endhour)  # retrieve data from database
        elif (len(args) == 6):
            self.endhour = args[5]
            lst = self.DB.retrieve_hours(self.table, self.year, self.month, self.startday, self.starthour, self.endhour)  # retrieve data from database
        else:
            lst = self.DB.retrieve_hours(self.table, self.year, self.month, self.startday, self.starthour)  # retrieve data from database

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
            if (self.endday in locals())
            else Youless.lang('customhourtitle') % (self.month, self.startday, self.endday, self.year, self.columns[1], int(total/1000), self.columns[2]))

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
        """
        Reads from table dayhours_X and return figure
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
        self.table = Youless.sql("dbtables")[self.etype][1]
        self.columns = [Youless.lang("U"), Youless.lang("W"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("U"), Youless.lang("L"), Youless.lang("M3")] if self.etype == 'G' else None

        if (type(self.month) == str):
            self.mN = datetime.datetime.strptime(self.month, '%B')
            self.month = int(self.mN.date().strftime('%m'))
        self.monthName = datetime.date(1900, self.month, 1).strftime('%B')
        lst = self.DB.retrieve_day(self.year, self.month, self.day, self.table)  # retrieve data from database
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
        logger.info("Plotting month %d day %d of year %d from table %s" % (self.month, self.day, self.year, self.table))
        return fig

    def plot_month_day(self, year, month, etype):
        """
        Reads from table yeardays_X and returns figure
        plot one month of the year into a graph with daily totals.
        plot_year_month(2021, 1, 'E') or plot_year_month(2021, January, 'G')
        year as integer
        month as integer or string
        etype as string ('E' for Electricity, 'G' for Gas)
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
        lst = self.DB.retrieve_month(self.year, self.month, self.table)  # retrieve data from database
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        high = max(lst[2]) + max(lst[2])/3
        totalkWh = 0
        for n, elem in enumerate(lst[2]):
            data[n+1] = elem  # Add kWh values to dictionary with the day as key
            totalkWh += elem

        df = pd.DataFrame(data.items(), columns=self.columns[:2])

        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),

            title=(Youless.lang('yearmonthtitle') % (self.monthName, self.year, self.columns[1], totalkWh, self.columns[2])),
        )
        logger.info("Plotting month %d of year %d" % (self.month, self.year))
        return fig

    def plot_year_day(self, year, etype):
        """
        Reads from table yeardays_X and returns figure
        plot the year with daily totals into a graph
        plot_year_day(2021, 'E')
        year as integer
        etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.etype = etype
        self.table = Youless.sql("dbtables")[self.etype][0]
        self.columns = [Youless.lang("D"), Youless.lang("KH"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("D"), Youless.lang("KM"), Youless.lang("M3")] if self.etype == 'G' else None
        self.type = 2  # equals year with month totals
        lst = self.DB.retrieve_year(self.year, self.type, self.table)
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        totalkWh = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            self.month = int(lst[n][1])
            for y, value in enumerate(lst[n][3]):
                tempkey = ("%d-%d-%d" % (self.year, self.month, y+1))  # year-month-day
                data[tempkey] = value
                totalkWh += value
                maxLst.append(value)
        high = max(maxLst) + max(maxLst)/3
        df = pd.DataFrame(data.items(), columns=self.columns[:2])
        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),
            title=(Youless.lang('yeardaytitle') % (self.year, self.columns[1], totalkWh, self.columns[2])),
        )
        logger.info("Plotting year %d" % (self.year))
        return fig

    def plot_year_month(self, year, etype):
        """
        Reads from table yeardays_X and returns figure
        plot the year with month totals into a graph
        plot_year(2021, 'E')
        year as integer
        etype as string ('E' for Electricity, 'G' for Gas)
        """
        self.year = year
        self.etype = etype
        self.table = Youless.sql("dbtables")[self.etype][0]
        self.columns = [Youless.lang("M"), Youless.lang("KH"), Youless.lang("KWH")] if self.etype == 'E' else [Youless.lang("M"), Youless.lang("KM"), Youless.lang("M3")] if self.etype == 'G' else None
        self.type = 1  # equals year with month totals
        lst = self.DB.retrieve_year(self.year, self.type, self.table)
        if lst == 0:
            logger.error("No Data")
            return 0
        data = {}
        months = {}
        totalkWh = 0.0
        maxLst = []
        for n, elem in enumerate(lst):
            data[lst[n][1]] = lst[n][3]
            months[lst[n][1]] = datetime.date(1900, int(lst[n][1]), 1).strftime('%B')
            totalkWh += lst[n][3]
            maxLst.append(lst[n][3])
        high = max(maxLst) + max(maxLst)/3
        df = pd.DataFrame(data.items(), columns=(self.columns[:2]))
        fig = px.bar(
            df,
            x=df[self.columns[0]],
            y=df[self.columns[1]],
            range_y=(0, high),
            title=(Youless.lang('yeartitle') % (self.year, self.columns[1], totalkWh, self.columns[2])),
        )
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(months.keys()),
                ticktext=list(months.values())
            )
        )
        logger.info("Plotting year %d" % (self.year))
        return fig


if __name__ == '__main__':
    sys.exit()

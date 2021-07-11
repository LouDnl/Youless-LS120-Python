#!/usr/bin/env python3
"""
    plot_live.py

    This file converts data received in list form from read_live.py into a pandas dataframe and returns a plotly figure
"""
import sys

# plotly figure
import plotly.express as px

# Youless setup
from .constants import Runtime, Youless
from .read_live import read_live_data

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("plot_live.py started")

# set language
Youless.youless_locale()

livedict = Youless.live_dict  # dictionary for temporary storage of live values


class plot_live:

    def __init__(self):
        pass

    def plot_live(self):
        """
            create graph with live information
        """
        date = Runtime.td('date_live')
        time = Runtime.td('secs_live')
        if (len(livedict['timelst']) == 20):
            livedict['timelst'].pop(0)
        livedict['timelst'].append(time)

        lvd = read_live_data().read_live()
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
            width=500,  # static figure width
            # height = (maxusage + (maxusage / 3) # calculate max figure height
            height=500,  # static figure height
            labels={
                "x": Youless.lang('T'),  # x-axis naming
                "y": Youless.lang('W')  # y-axis naming
            }
        )
        return fig

    def plot_live_minutes(self):
        """
            create graph with minute information
        """
        date = Runtime.td('date_live')
        time = Runtime.td('time_live')
        e = read_live_data().read_minutes()
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
        return fig

    def plot_ten_minutes(self):
        """
            create graph with ten minute information
        """
        # read data function not working properly yet
        pass


if __name__ == '__main__':
    sys.exit()

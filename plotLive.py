"""
    Plot live read data from Youless LS120
"""

import sys, os, datetime, re, time, locale
import calendar
import sqlite3 as sl
from sqlite3 import IntegrityError
import ast # for converting string representation of a list to a list

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# youless specific
from globals import *
# from readData import *
from readLive import *

# set language
Vars.youlessLocale()

#
livedict = Vars.livedict #{'timelst': [], 'wattlst': []} # dictionary for storing live data

class plotLive:
    
    def __init__(self):
        pass

    def plot_live(self):
        """
            create graph with live information
        """        
        date = Runtime.td('date_live')
        time = Runtime.td('secs_live')
        if (len(livedict['timelst']) == 20):
            livedict['timelst'].pop(0) #
        livedict['timelst'].append(time)

        l = readLiveData().readLive()
        live = l['pwr']
        if (len(livedict['wattlst']) == 20):
            livedict['wattlst'].pop(0)
        livedict['wattlst'].append(live)

        total = l['cnt']
        graphtitle = Vars.lang('livegraphtitle').format(live,date,time,total,Vars.lang('KWH'))
        maxusage = max(livedict['wattlst'])

        fig = px.line(
            x = livedict['timelst'], y = livedict['wattlst'],
            title=graphtitle,
            range_y = (0, (maxusage + (maxusage / 3))),
            width = 500,
            height = 500, #(maxusage + (maxusage / 3))
            labels = {
                "x": Vars.lang('T'),
                "y": Vars.lang('W')
            }
        )
        return fig        

    def plot_live_minutes(self):
        """
            create graph with minute information
        """
        date = Runtime.td('date_live')
        time = Runtime.td('time_live')
        e = readLiveData().readMinutes()
        live = e['watts'][-1]
        maxusage = max(e['watts'])
        graphtitle = Vars.lang('liveminutegraphtitle').format(live,date,time)
        fig = px.line(
            x = e['time'], y = e['watts'],
            title=graphtitle,
            # width = 1300,
            height = 500, #(maxusage + (maxusage / 3))
            labels = {
                "x": Vars.lang('T'),
                "y": Vars.lang('W')
            }
        )
        return fig

    def plot_ten_minutes(self):
        """
            create graph with ten minute information
        """
        ## read data function not working properly yet
        pass

def main():
    log(lambda: "I do not run on my own...")

if __name__ == '__main__':
        main()    
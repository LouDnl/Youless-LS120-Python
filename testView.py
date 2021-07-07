"""
    file to test views
"""

#defaults
import sys, os, datetime, re, time, sched, locale

# web connects
import requests

# graph
import plotly.express as px

# dash webpage
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# json
import json

# youless specific
from globals import *
# from plotData import *
from webElements import *
from readLive import *
from plotLive import *
# import importData as db

# updateDB = 1
# while(updateDB): # update the database once
    # db.main() # update database always at start
    # updateDB = 0

# set language
# locale.setlocale(locale.LC_ALL, Vars.web("LOCALE"))
Vars.youlessLocale()

class allGraphsView:

    def __init__(self):
        # global updateDB
        # updateDB = -1

        self.elist = Vars.conf('energytypes')['list'] # retrieve energy types

    def createDashPage(self, ip, port):
        """
        Plot one or more graph with dash and plotly for testing purposes
        """
        self.ip = ip
        self.port = port

        # from datetime import datetime
        # dt = datetime.today() # get current datetime

        # define the app
        app = dash.Dash(
                        __name__,
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
        ) 
        
        # define tables to show on page
        dual_table = Web.dual_table(Vars.lang('TOYE'), "e_today", "e_yesterday")
        
        # define layout with defined tables
        app.layout = Web.layout_with_intervals(dual_table)

        # start the callback with update interval
        @app.callback([
            Output('e_today', 'figure'),
            Output('e_yesterday', 'figure')],
            [Input('interval-component-halfhour', 'n_intervals')
        ])
        # the callback function
        def multi_output(n):
            fig1 = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_now'), self.elist[0])
            fig2 = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_yesterday'), self.elist[0])
            return fig1, fig2
   
        # run the webserver
        app.run_server(debug=Runtime.DASHDEBUG, host=ip, port=port)

def main():
    if (Runtime.DASHDEBUG): # if True then run on 127.0.0.1
        ip = Vars.local_ip
    else: # else run on the defined external IP
        ip = Vars.external_ip

    allGraphsView().createDashPage(ip, Vars.port) # go for it

if __name__ == '__main__':
    main()
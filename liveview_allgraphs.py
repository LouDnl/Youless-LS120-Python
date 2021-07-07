"""
    Show all graphs on one page
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
from plotData import *
from webElements import *
from readLive import *
from plotLive import *
import importData as db

updateDB = 1
while(updateDB): # update the database once
    db.main() # update database always at start
    updateDB = 0

# set language
# locale.setlocale(locale.LC_ALL, Vars.web("LOCALE"))
Vars.youlessLocale()

class allGraphsView:

    def __init__(self):
        global updateDB
        updateDB = -1

        self.elist = Vars.conf('energytypes')['list'] # retrieve energy types

    def createDashPage(self, ip, port):
        """
        Plot all information with plotly and dash
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
        live_table = Web.dual_table(Vars.lang('LIVE'), "liveGraph", "minuteGraph")
        today_yesterday_table = Web.quad_table_header(Vars.lang('TOYE'), "e_today", "e_yesterday", "g_today", "g_yesterday")
        thismonth_lastmonth_table = Web.quad_table_header(Vars.lang('CMLM'), "e_currmonth", "e_lastmonth", "g_currmonth", "g_lastmonth")
        thisyear_lastyear_month_table = Web.quad_table_header(Vars.lang('TYLYM'), "e_year1", "e_year2", "g_year1", "g_year2")
        thisyear_lastyear_day_table = Web.quad_table_header(Vars.lang('TYLYD'), "e_fullyear1", "e_fullyear2", "g_fullyear1", "g_fullyear2")
        
        # define layout with defined tables 
        app.layout = Web.layout_with_intervals(live_table, today_yesterday_table, thismonth_lastmonth_table, thisyear_lastyear_month_table, thisyear_lastyear_day_table)

        # start callback with update interval
        @app.callback( # update every 15 minutes (quarter hour)
            Output('updatedb', 'children'), # database update output
            Input('interval-component-quarterhour', 'n_intervals') # interval input
        )
        # the callback function
        def quarter_hour(n):
            db.main() # update database
            return

        livedict = {'timelst': [], 'wattlst': []} # dictionary for storing live data
        # start callback with update interval
        @app.callback( # live update (every 5 seconds)
            Output('liveGraph', 'figure'), # live graph output
            Input('interval-component-live', 'n_intervals') # interval input
        )
        # the callback function
        def update_graph_live(n):
            fig = plotLive().plot_live() # plot live graph
            return fig

        # start callback with update interval
        @app.callback( # update every minute (60 seconds)
            Output('minuteGraph', 'figure'), # minute graph output
            Input('interval-component-minute', 'n_intervals') # interval input
        )
        # the callback function
        def update_minutegraph_live(n):
            fig = plotLive().plot_live_minutes() # plot live minute graph
            return fig

        # start callback with update interval
        @app.callback( # update every 30 minutes (half hour)
            Output('e_today', 'figure'), # energy today output
            Output('g_today', 'figure'), # gas today output
            Input('interval-component-halfhour', 'n_intervals') # interval input
        )
        # the callback function
        def update_halfhour(n):
            fig1 = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_now'), self.elist[0]) # plot energy today
            fig2 = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_now'), self.elist[1]) # plot gas today
            return fig1, fig2

        # start callback with update interval
        @app.callback([ # update every 360 minutes (six hours)
            Output('e_yesterday', 'figure'), # energy yesterday
            Output('g_yesterday', 'figure'), # gas yesterday
            Output('e_currmonth', 'figure'), # energy current month
            Output('e_lastmonth', 'figure'), # energy last month
            Output('g_currmonth', 'figure'), # gas current month
            Output('g_lastmonth', 'figure'), # gas last month
            Output('e_year1', 'figure'), # energy current year per month
            Output('e_year2', 'figure'), # energy last year per month
            Output('g_year1', 'figure'), # gas current year per month
            Output('g_year2', 'figure'), # gas last year per month
            Output('e_fullyear1', 'figure'), # energy current year per day
            Output('e_fullyear2', 'figure'), # energy last year per day
            Output('g_fullyear1', 'figure'), # gas current year per day
            Output('g_fullyear2', 'figure')], # gas last year per day
            [Input('interval-component-sixhours', 'n_intervals') # interval input
        ])
        # the callback function
        def update_sixhours(n):
            fig01 = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_yesterday'), self.elist[0]) # plot energy yesterday
            fig02 = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_yesterday'), self.elist[1]) # plot gas yesterday
            fig03 = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('month_now'), self.elist[0]) # plot energy current month
            fig04 = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('last_month'), self.elist[0]) # plot energy last month
            fig05 = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('month_now'), self.elist[1]) # plot gas current month
            fig06 = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('last_month'), self.elist[1]) # plot gas last month
            fig07 = plotData().plot_year_month(Runtime.td('year_now'), self.elist[0]) # plot energy current year per month
            fig08 = plotData().plot_year_month(Runtime.td('last_year'), self.elist[0]) # plot energy last year per month
            fig09 = plotData().plot_year_month(Runtime.td('year_now'), self.elist[1]) # plot gas current year per month
            fig10 = plotData().plot_year_month(Runtime.td('last_year'), self.elist[1]) # plot gas last year per month
            fig11 = plotData().plot_year_day(Runtime.td('year_now'), self.elist[0]) # plot energy current year per day
            fig12 = plotData().plot_year_day(Runtime.td('last_year'), self.elist[0]) # plot energy last year per day
            fig13 = plotData().plot_year_day(Runtime.td('year_now'), self.elist[1]) # plot gas current year per day
            fig14 = plotData().plot_year_day(Runtime.td('last_year'), self.elist[1]) # plot gas last year per day
            return fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14

        ## Display json structure in frame below graph
        # @app.callback(
        #     Output("structure", "children"),
        #     [Input("graph", "figure")])
        # def display_structure(fig_json):
        #     return json.dumps(fig_json, indent=2)

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
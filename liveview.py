#defaults
import sys, os, datetime, re, time, sched, locale
# from datetime import datetime
# dataFrame structure
# import pandas as pd

# graph
import plotly.express as px

# web connects
import requests
# from requests import get

# dash webpage
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# json
import json

# enable multithreading / asyncio
#from threading import *
#import asyncio
# from multiprocessing import Pool
# from multiprocessing import Process
# import _thread

# import globals
# import globals as gl
from globals import *
from plotEnergy import *
import importData_toDB as db
updateDB = 1
while(updateDB):
    db.main() # update database always at start
    updateDB = 0

# set language
locale.setlocale(locale.LC_ALL, Vars.web("LOCALE"))

class readLiveData:

    def __init__(self):
        self.__headers = Vars.web("HEADERS") # acceptable html headers
        self.__url = Vars.web("URL") # base url
        self.__ele = Vars.web("ELE")
        self.__gas = Vars.web("GAS")
        self.__json = Vars.web("JSON")
        self.__month = Vars.web("M")
        self.__day = Vars.web("W")
        self.__stats = Vars.web("STATS")
        self.__D = Vars.web("D")

    def readLive(self):
        """
        Import live current data from Youless 120
        No history build up
        """

        self.api = requests.get(self.__url + self.__stats + self.__json).json()

        return self.api

    def readMinutes(self):
        """
        Import per minute data from Youless 120
        Is always 1 minute behind live
        """
        self.maxPage = Vars.web("maxMinutePage")
        self.minPage = Vars.web("minMinutePage")
        self.maxMinute = Vars.web("maxMinute")
        self.minMinute = Vars.web("minMinute")
        self.counter = self.maxPage
        e = {}
        time = []
        watts = []

        while (self.counter >= self.minPage):
            self.api = requests.get(self.__url + self.__ele + self.__json + self.__D + str(self.counter)).json()
            # log(lambda: self.api)
            self.date = datetime.datetime.strptime(self.api['tm'], '%Y-%m-%dT%H:%M:%S')
            i = self.minMinute
            while (i <= self.maxMinute):
                h = self.date.hour
                m = self.date.minute + i
                if (m >= 60):
                    m -= 60
                    h += 1
                self.time = '%02d:%02d' % (h,m)# str(self.date.time())[0:5]
                self.watt = int(self.api['val'][i])
                time.append(self.time)
                watts.append(self.watt)

                dbg(lambda: 'Time: {} Usage: {} Watt'.format(self.time, self.watt))
                i += 1
            # log(lambda: self.date)
            self.counter -= 1
        e['time'] = time
        e['watts'] = watts
        # log(lambda: e)
        return e

class plotLiveData: # only plots Energy at the moment

    def __init__(self):
        global updateDB
        updateDB = -1

        self.elist = Vars.conf('energytypes')['list']

    def plotLive(self, ip, port):
        """
        Plot the live usage with plotly
        """
        self.ip = ip
        self.port = port

        from datetime import datetime
        dt = datetime.today() # get current datetime
        # dt = Runtime.dt
        # day_now = dt.day
        # month_now = dt.month
        # year_now = dt.year #% 100 # last two digits
        # last_year = dt.year-1 # last year

        # d_today = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now)
        # d_yesterday = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now-1)
        # d_currmonth = plotData().plot_year_month(Runtime.year_now, Runtime.month_now)
        # d_lastmonth = plotData().plot_year_month(Runtime.year_now, Runtime.last_month)
        # d_year1 = plotData().plot_year(Runtime.year_now)
        # d_year2 = plotData().plot_year(Runtime.last_year)
        # d_fullyear1 = plotData().plot_year_day(Runtime.year_now)
        # d_fullyear2 = plotData().plot_year_day(Runtime.last_year)

        app = dash.Dash(__name__)

        app.layout = html.Div([
            # dcc.Graph(id="graph", figure=fig),
            html.Span(id='updatedb', style={'visibility': 'hidden'}),
            dcc.Graph(id="liveGraph"),
            dcc.Graph(id="minuteGraph"),
            dcc.Graph(id="d_today"),
            dcc.Graph(id="d_yesterday"),
            dcc.Graph(id="d_currmonth"),
            dcc.Graph(id="d_lastmonth"),
            dcc.Graph(id="d_year1"),
            dcc.Graph(id="d_year2"),
            dcc.Graph(id="d_fullyear1"),
            dcc.Graph(id="d_fullyear2"),
            dcc.Interval(
                id='interval-component-live',
                interval=5*1000, # 5 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-minutes',
                interval=60*1000, # 60 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-halfhourly',
                interval=3600*1000, # 3600 seconds (1 hour) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-hourly',
                interval=1800*1000, # 1800 seconds (half hour) in milliseconds
                n_intervals=0
            )#,
            # html.Pre(
            #     id='structure',
            #     style={
            #         'border': 'thin lightgrey solid',
            #         'overflowY': 'scroll',
            #         'height': '275px'
            #     }
            # )
        ])

        @app.callback(
            # Output
            Output('updatedb', 'children'),
            Input('interval-component-halfhourly', 'n_intervals')
        )
        def updatedb(n):
            db.main()
            return

        livedict = {'timelst': [], 'wattlst': []} # dictionary for storing live data
        @app.callback(
            Output('liveGraph', 'figure'),
            Input('interval-component-live', 'n_intervals')
        )
        def update_graph_live(n):
            dt = datetime.now() # current datetime
            date = (dt.strftime("%A %d %B %Y"))
            time = (dt.strftime("%H:%M:%S"))
            if (len(livedict['timelst']) == 20):
                livedict['timelst'].pop(0) #
            livedict['timelst'].append(time)

            l = readLiveData().readLive()
            live = l['pwr']
            if (len(livedict['wattlst']) == 20):
                livedict['wattlst'].pop(0)
            livedict['wattlst'].append(live)

            total = l['cnt']
            # graphtitle = "Live verbruik: {} watt, {} {} uur ".format(live,date,time)
            graphtitle = Vars.lang('livegraphtitle').format(live,date,time)
            maxusage = max(livedict['wattlst'])
            # log(lambda: livedict)

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

        @app.callback(
            Output('minuteGraph', 'figure'),
            Input('interval-component-minutes', 'n_intervals')
        )
        def update_minutegraph_live(n):
            dt = datetime.now() # get current datetime
            date = (dt.strftime("%A %d %B %Y"))
            time = (dt.strftime("%H:%M"))
            e = readLiveData().readMinutes()
            live = e['watts'][-1]
            maxusage = max(e['watts'])
            # log(lambda: maxusage)
            graphtitle = Vars.lang('liveminutegraphtitle').format(live,date,time)
            fig = px.line(
                x = e['time'], y = e['watts'],
                title=graphtitle,
                height = 500, #(maxusage + (maxusage / 3))
                labels = {
                    "x": Vars.lang('T'),
                    "y": Vars.lang('W')
                }
            )
            return fig

        @app.callback(
            Output('d_today', 'figure'),
            Input('interval-component-halfhourly', 'n_intervals')
        )
        def d_today(n):
            fig = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now, self.elist[0])
            return fig

        @app.callback(
            Output('d_yesterday', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_yesterday(n):
            fig = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now-1, self.elist[0])
            return fig

        @app.callback(
            Output('d_currmonth', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_currmonth(n):
            fig = plotData().plot_month_day(Runtime.year_now, Runtime.month_now, self.elist[0])
            return fig

        @app.callback(
            Output('d_lastmonth', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_lastmonth(n):
            fig = plotData().plot_month_day(Runtime.year_now, Runtime.last_month, self.elist[0])
            return fig

        @app.callback(
            Output('d_year1', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_year1(n):
            fig = plotData().plot_year_month(Runtime.year_now, self.elist[0])
            return fig

        @app.callback(
            Output('d_year2', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_year2(n):
            fig = plotData().plot_year_month(Runtime.last_year, self.elist[0])
            return fig

        @app.callback(
            Output('d_fullyear1', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_fullyear1(n):
            fig = plotData().plot_year_day(Runtime.year_now, self.elist[0])
            return fig

        @app.callback(
            Output('d_fullyear2', 'figure'),
            Input('interval-component-hourly', 'n_intervals')
        )
        def d_fullyear2(n):
            fig = plotData().plot_year_day(Runtime.last_year, self.elist[0])
            return fig


        ## Display json structure in frame below graph
        # @app.callback(
        #     Output("structure", "children"),
        #     [Input("graph", "figure")])
        # def display_structure(fig_json):
        #     return json.dumps(fig_json, indent=2)

        app.run_server(debug=True, host=ip, port=port)

# def updateDB_nonworking(text):
#     log(lambda: text)
#     # while (1):
#     # for _
#     dt = datetime.datetime.now() # get current datetime
#     uTime = (dt.strftime("%H:%M:%S")) # time in format hours:minutes:seconds
#     mins = int(dt.strftime("%M"))
#     quarters = (0,15,30,45)
#     if (mins in quarters):
#         log(lambda: "The time is {}".format(uTime))
#         time.sleep(65) # 65 second wait so it doesn't get repeated
#         updateDB("Restarting updateDB from quarters")
#     time.sleep(65)
#     updateDB("Restarting updateDB")
#
# count = 0
# def updateDB():
#     global count
#     if (count == 0):
#         count += 1
#         log(lambda: "Starting static data import from main %d" % count)
#         import importEnergy_toDB
#         importEnergy_toDB.main()

def main():
    # Process(target=updateDB("Starting updateDB")).start()
    # Process(target=plotLiveData().plotLive).start()
    # _thread.start_new_thread(plotLiveData().plotLive())
    # _thread.start_new_thread(updateDB("Starting updateDB thread"), ())


    # updateDB() # disable auto update database on start for now
    plotLiveData().plotLive(Vars.ip, Vars.port)

if __name__ == '__main__':
    main()

# url = "http://192.168.0.40/V?f=j&h=1" # goes up to 20
# time watt website is http://192.168.0.40/V?h=1 and goes up to 20 aswell
# displays live Watt usage per minute
# un equals watt
# tm equals date and time format: 2021-04-10T08:05:00
# dt ???
# val has the minute values from 0 to 30 where 30 is null
# 0 equals the same minute as given in the Time minute value


# response = urllib.urlopen(url) # python 2
# response = requests.get(url)

# data2 = json.loads(response.content) # json from json library
# data = response.json() # json from requests.get



# log(lambda: data)
# log(lambda: type(data2))
# log(lambda: data['val'][0])
# log(lambda: type(data['val'][0]))
# myInt = int(data['val'][0])
# log(lambda: "%d" % int(data['val'][0]))
# log(lambda: type(myInt))

# for n, elem in enumerate(data['val']):
#     log(lambda: elem)

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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

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
        self.__H = Vars.web("H")

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
        data = {}
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
        data['time'] = time
        data['watts'] = watts
        # log(lambda: e)
        return data

    # def readTenMinutes(self):
    #     """
    #     Import per ten minute data from Youless 120
    #     Is always 1 minute behind live
    #     """
    #     self.maxPage = Vars.web("maxTenMinPage")
    #     self.minPage = Vars.web("minTenMinPage")
    #     self.maxEntry = Vars.web("maxTen")
    #     self.minEntry = Vars.web("minTen")
    #     self.counter = self.minPage
    #     data = {}
    #     time = []
    #     watts = []
    #
    #     while (self.counter <= self.maxPage):
    #         self.api = requests.get(self.__url + self.__ele + self.__json + self.__H + str(self.counter)).json()
    #         # log(lambda: self.api)
    #         self.date = datetime.datetime.strptime(self.api['tm'], '%Y-%m-%dT%H:%M:%S')
    #         i = self.minEntry
    #         while (i <= self.maxEntry):
    #             h = self.date.hour
    #             m = self.date.minute + (10 * i)
    #             if (m == 60):
    #                 h += 1
    #                 m = 0
    #             self.time = '%02d:%02d' % (h,m)# str(self.date.time())[0:5]
    #             self.watt = int(self.api['val'][i])
    #             time.append(self.time)
    #             watts.append(self.watt)
    #             dbg(lambda: 'Time: {} Usage: {} Watt'.format(self.time, self.watt))
    #             i += 1
    #         # log(lambda: self.date)
    #         self.counter += 1
    #     data['time'] = time
    #     data['watts'] = watts
    #     log(lambda: data)
    #     # return data

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

        # e_today = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now)
        # e_yesterday = plotData().plot_day_hour(Runtime.year_now,Runtime.month_now,Runtime.day_now-1)
        # e_currmonth = plotData().plot_year_month(Runtime.year_now, Runtime.month_now)
        # e_lastmonth = plotData().plot_year_month(Runtime.year_now, Runtime.last_month)
        # e_year1 = plotData().plot_year(Runtime.year_now)
        # e_year2 = plotData().plot_year(Runtime.last_year)
        # e_fullyear1 = plotData().plot_year_day(Runtime.year_now)
        # e_fullyear2 = plotData().plot_year_day(Runtime.last_year)

        # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(
                        __name__,
                        # external_stylesheets=external_stylesheets
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
        ) 
        
        # app.scripts.config.serve_locally = Runtime.SERVE # enable/disables local serving of the scripts

        # live_table = html.Div([
        #     dbc.Row([
        #         dbc.Col(html.Div("LIVE TEST"))
        #     ], style={'text-align':'center'}),
        #     dbc.Row([
        #         dbc.Col(dcc.Graph(id="liveGraph")),
        #         dbc.Col(dcc.Graph(id="minuteGraph"))
        #     ])
        # ])
        
        
        live_table = dbc.Table([
            html.Tr([
               html.Th(Vars.lang('LIVE'), colSpan=2, scope="col") 
            ], style=Vars.css('row_title')),
            html.Tr([
                html.Td(dcc.Graph(id="liveGraph"), style=Vars.css('column_css')),
                html.Td(dcc.Graph(id="minuteGraph"), style=Vars.css('column_css'))
            ]),
        ], style=Vars.css('table_css'), borderless=True)

        today_yesterday_table = Vars.default_table(Vars.lang('TOYE'), "e_today", "e_yesterday", "g_today", "g_yesterday")
        thismonth_lastmonth_table = Vars.default_table(Vars.lang('CMLM'), "e_currmonth", "e_lastmonth", "g_currmonth", "g_lastmonth")
        thisyear_lastyear_month_table = Vars.default_table(Vars.lang('TYLYM'), "e_year1", "e_year2", "g_year1", "g_year2")
        thisyear_lastyear_day_table = Vars.default_table(Vars.lang('TYLYD'), "e_fullyear1", "e_fullyear2", "g_fullyear1", "g_fullyear2")
         
        app.layout = html.Div([
            # dcc.Graph(id="graph", figure=fig),
            html.Span(id='updatedb', style={'visibility': 'hidden'}),
            live_table,
            today_yesterday_table,
            thismonth_lastmonth_table,
            thisyear_lastyear_month_table,
            thisyear_lastyear_day_table,
            dcc.Interval(
                id='interval-component-live',
                interval=5*1000, # 5 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-minute',
                interval=60*1000, # 60 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-quarterhour',
                interval=900*1000, # 900 seconds (15 minutes) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-halfhour',
                interval=1800*1000, # 1800 seconds (1 hour) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-hour',
                interval=3600*1000, # 3600 seconds (half hour) in milliseconds
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
        ], style=Vars.css('page_css'))
        
        # app.css.append_css({
        #     #'external_url': Vars.path + Vars.cssname
        #     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css' # plotly css
        # })

        @app.callback(
            # Output
            Output('updatedb', 'children'),
            Input('interval-component-quarterhour', 'n_intervals')
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
            graphtitle = Vars.lang('livegraphtitle').format(live,date,time,total,Vars.lang('KWH'))
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
            Input('interval-component-minute', 'n_intervals')
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
                # width = 1300,
                height = 500, #(maxusage + (maxusage / 3))
                labels = {
                    "x": Vars.lang('T'),
                    "y": Vars.lang('W')
                }
            )
            return fig

        @app.callback(
            Output('e_today', 'figure'),
            Input('interval-component-halfhour', 'n_intervals')
        )
        def e_today(n):
            fig = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_now'), self.elist[0])
            return fig

        @app.callback(
            Output('e_yesterday', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_yesterday(n):
            fig = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_yesterday'), self.elist[0])
            return fig

        @app.callback(
            Output('g_today', 'figure'),
            Input('interval-component-halfhour', 'n_intervals')
        )
        def g_today(n):
            fig = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_now'), self.elist[1])
            return fig

        @app.callback(
            Output('g_yesterday', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_yesterday(n):
            fig = plotData().plot_day_hour(Runtime.td('year_now'),Runtime.td('month_now'),Runtime.td('day_yesterday'), self.elist[1])
            return fig

        @app.callback(
            Output('e_currmonth', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_currmonth(n):
            fig = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('month_now'), self.elist[0])
            return fig

        @app.callback(
            Output('e_lastmonth', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_lastmonth(n):
            fig = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('last_month'), self.elist[0])
            return fig

        @app.callback(
            Output('g_currmonth', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_currmonth(n):
            fig = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('month_now'), self.elist[1])
            return fig

        @app.callback(
            Output('g_lastmonth', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_lastmonth(n):
            fig = plotData().plot_month_day(Runtime.td('year_now'), Runtime.td('last_month'), self.elist[1])
            return fig

        @app.callback(
            Output('e_year1', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_year1(n):
            fig = plotData().plot_year_month(Runtime.td('year_now'), self.elist[0])
            return fig

        @app.callback(
            Output('e_year2', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_year2(n):
            fig = plotData().plot_year_month(Runtime.td('last_year'), self.elist[0])
            return fig

        @app.callback(
            Output('g_year1', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_year1(n):
            fig = plotData().plot_year_month(Runtime.td('year_now'), self.elist[1])
            return fig

        @app.callback(
            Output('g_year2', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_year2(n):
            fig = plotData().plot_year_month(Runtime.td('last_year'), self.elist[1])
            return fig

        @app.callback(
            Output('e_fullyear1', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_fullyear1(n):
            fig = plotData().plot_year_day(Runtime.td('year_now'), self.elist[0])
            return fig

        @app.callback(
            Output('e_fullyear2', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def e_fullyear2(n):
            fig = plotData().plot_year_day(Runtime.td('last_year'), self.elist[0])
            return fig

        @app.callback(
            Output('g_fullyear1', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_fullyear1(n):
            fig = plotData().plot_year_day(Runtime.td('year_now'), self.elist[1])
            return fig

        @app.callback(
            Output('g_fullyear2', 'figure'),
            Input('interval-component-hour', 'n_intervals')
        )
        def g_fullyear2(n):
            fig = plotData().plot_year_day(Runtime.td('last_year'), self.elist[1])
            return fig

        ## Display json structure in frame below graph
        # @app.callback(
        #     Output("structure", "children"),
        #     [Input("graph", "figure")])
        # def display_structure(fig_json):
        #     return json.dumps(fig_json, indent=2)

        app.run_server(debug=Runtime.DASHDEBUG, host=ip, port=port)

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

    if (Runtime.DASHDEBUG):
        ip = Vars.local_ip
    else:
        ip = Vars.external_ip

    plotLiveData().plotLive(ip, Vars.port)

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

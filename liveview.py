#defaults
import sys, os, datetime, re, time, sched

# dataFrame structure
# import pandas as pd

# graph
import plotly.express as px

# web connects
import requests
# from requests import get

# json
import json

# enable multithreading / asyncio
from threading import *
import asyncio

# enable debug messages
DEBUG = True
def log(s):
    """
    Usage:
    log(lambda: "TEXT")
    log(lambda: "TEXT and %s" % variable)
    """
    if DEBUG:
        print(s())

# global variables
cheeky = 0

class readLiveData:
    def __init__(self):
        self.__headers = { "Accept-Language": "en-US, en;q=0.5"} # acceptable html headers
        self.__url = "http://192.168.0.40" # base url
        self.__stats = "/a?"
        self.__ele = "/V?" # url year, week, day, hour
        # self.__gas = "/W?" # url year, week, day
        self.__json = "f=j&"
        self.__D = "h=" # url represented in 20 parts of half an hour counting back from the current moment

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
        self.maxPage = 20
        self.minPage = 1
        self.maxMinute = 29
        self.minMinute = 0
        self.counter = self.maxPage
        e = {}
        time = []
        watts = []

        while (self.counter >= self.minPage):
            self.api = requests.get(self.__url + self.__ele + self.__json + self.__D + str(self.counter)).json()
            # log(lambda: self.api)
            self.date = datetime.datetime.strptime(self.api['tm'], '%Y-%d-%mT%H:%M:%S')
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
                # log(lambda: 'Time: {} Usage: {} Watt'.format(self.time, self.watt))
                i += 1
            # log(lambda: self.date)
            self.counter -= 1
        e['time'] = time
        e['watts'] = watts
        # log(lambda: e)
        return e

class plotLiveData:

    def __init__(self):
        pass

    def plotLive(self):
        """
        Plot the live usage with plotly
        """
        import dash
        import dash_core_components as dcc
        import dash_html_components as html
        from dash.dependencies import Input, Output

        from datetime import datetime
        dt = datetime.today() # get current datetime
        day_now = dt.day
        month_now = dt.month
        year_now = dt.year #% 100 # last two digits
        last_year = dt.year-1 # last year

        import locale

        import plotEnergy

        d_today = plotEnergy.plotData().plot_day_hour(year_now,month_now,day_now)
        d_yesterday = plotEnergy.plotData().plot_day_hour(year_now,month_now,day_now-1)
        d_currmonth = plotEnergy.plotData().plot_year_month(2021,4)
        d_year1 = plotEnergy.plotData().plot_year(2020)
        d_year2 = plotEnergy.plotData().plot_year(2021)
        d_fullyear1 = plotEnergy.plotData().plot_year_day(2020)
        d_fullyear2 = plotEnergy.plotData().plot_year_day(2021)

        locale.setlocale(locale.LC_ALL, 'nl_NL')

        app = dash.Dash(__name__)

        app.layout = html.Div([
            # dcc.Graph(id="graph", figure=fig),
            dcc.Graph(id="liveGraph"),
            dcc.Graph(id="minuteGraph"),
            dcc.Graph(figure=d_today),
            dcc.Graph(figure=d_yesterday),
            dcc.Graph(figure=d_currmonth),
            dcc.Graph(figure=d_year1),
            dcc.Graph(figure=d_year2),
            dcc.Graph(figure=d_fullyear1),
            dcc.Graph(figure=d_fullyear2),
            dcc.Interval(
                id='interval-component-live',
                interval=5*1000, # 5 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-minutes',
                interval=60*1000, # 60 seconds in milliseconds
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
            graphtitle = "Live verbruik: {} watt, {} {} uur ".format(live,date,time)

            maxusage = max(livedict['wattlst'])
            # log(lambda: livedict)

            fig = px.line(
                x = livedict['timelst'], y = livedict['wattlst'],
                title=graphtitle,
                range_y = (0, (maxusage + (maxusage / 3))),
                width = 500,
                height = 500, #(maxusage + (maxusage / 3))
                labels = {
                    "x": "Time",
                    "y": "Watts"
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
            graphtitle = "Live verbruik per minuut: {} watt, {} {} uur ".format(live,date,time)
            fig = px.line(
                x = e['time'], y = e['watts'],
                title=graphtitle,
                height = 500, #(maxusage + (maxusage / 3))
                labels = {
                    "x": "Time",
                    "y": "Watts"
                }
            )
            return fig


        ## Display json structure in frame below graph
        # @app.callback(
        #     Output("structure", "children"),
        #     [Input("graph", "figure")])
        # def display_structure(fig_json):
        #     return json.dumps(fig_json, indent=2)

        app.run_server(debug=True, host='192.168.0.5')

def updateDB():
    # date = (dt.strftime("%A %d %B %Y"))
    # dt = datetime.now() # current datetime
    # time = (dt.strftime("%H:%M:%S"))
    s = sched.scheduler(time.time, time.sleep)
    def run_update(sc):
        log(lambda: "Updating the database")
        # print("TEST")
        s.enter(60, 1, run_update, (sc,))
    log(lambda: "Starting the scheduler")
    s.enter(60, 1, run_update, (s,))
    s.run()

def main():
    # readLiveData().readHours()
    # readLiveData().readLive()
    plot = Thread(target=plotLiveData().plotLive())
    # update = Thread(target=updateDB())
    # asyncio.run(updateDB())
    # asyncio.run(plotLiveData().plotLive())
    updateDB()
    plot.start()





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

#!/usr/bin/env python3
"""
    File name: dash_allgraphs_live.py
    Author: LouDFPV
    Date created: 15/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    this is an example file that starts a dash/flask webserver:
    - run the file for command line arguments
    - shows all available graphs on one page
    - graphs get updated by a scheduler
    - database gets updated by a scheduler
"""
import datetime
import sys

# dash webpage
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Youless setup
from LS120 import Runtime, Youless
from LS120.plotly_graphs import plot_live, plot_dbdata
import LS120.db_auto_import as db

# Dash setup
from dash_settings import Dash_Settings, ip_validation
from dash_web_elements import web_elements  # dash web page elements

# initialize logging
# from LS120 import logger
import logging
logger = logging.getLogger(__name__)
logger.debug("dash_allgraphs_live.py started")

# set language
Youless.youless_locale()

# database variable
update_db = 1


class all_graphs_view:
    """class to create dash page with all graphs from LS120.plotly_graphs.plot_data"""

    def __init__(self) -> None:
        global update_db
        update_db = -1

        self.elist = Youless.sql('energytypes')['list']  # retrieve energy types

    def create_dash_page(self, ip, port, debug, reloader):
        """Plot all information with plotly and dash"""
        self.ip = ip
        self.port = port
        self.debug = debug
        self.reloader = reloader

        # define the app
        app = dash.Dash(
                        __name__,
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

        # define tables to show on page
        live_table = web_elements.dual_table(Youless.lang('LIVE'), "liveGraph", "minuteGraph")
        live_ten_minutes_e_table = web_elements.table_header(Youless.lang('LIVE_TEN_E'), "e_tenMinuteGraph")
        live_ten_minutes_g_table = web_elements.table_header(Youless.lang('LIVE_TEN_G'), "g_tenMinuteGraph")
        today_yesterday_table = web_elements.quad_table_header(Youless.lang('TOYE'), "e_today", "e_yesterday", "g_today", "g_yesterday")
        thismonth_lastmonth_table = web_elements.quad_table_header(Youless.lang('CMLM'), "e_currmonth", "e_lastmonth", "g_currmonth", "g_lastmonth")
        thisyear_lastyear_month_table = web_elements.quad_table_header(Youless.lang('TYLYM'), "e_year1", "e_year2", "g_year1", "g_year2")
        thisyear_lastyear_day_table = web_elements.quad_table_header(Youless.lang('TYLYD'), "e_fullyear1", "e_fullyear2", "g_fullyear1", "g_fullyear2")

        # define layout with defined tables
        app.layout = web_elements.layout_with_intervals(live_table, live_ten_minutes_e_table, live_ten_minutes_g_table, today_yesterday_table, thismonth_lastmonth_table, thisyear_lastyear_month_table, thisyear_lastyear_day_table)

        # start callback with update interval
        @app.callback(  # update every 15 minutes (quarter hour)
            Output('updatedb', 'children'),  # database update output
            Input('interval-component-quarterhour', 'n_intervals')  # interval input
        )
        # the callback function
        def quarter_hour(n):
            db.main()  # update database
            return

        # start callback with update interval
        @app.callback(  # live update (every 5 seconds)
            Output('liveGraph', 'figure'),  # live graph output
            Input('interval-component-live', 'n_intervals')  # interval input
        )
        # the callback function
        def update_graph_live(n):
            fig = plot_live().plot_live()  # plot live graph
            return fig

        # start callback with update interval
        @app.callback(  # update every minute (60 seconds)
            Output('minuteGraph', 'figure'),  # minute graph output
            Input('interval-component-minute', 'n_intervals')  # interval input
        )
        # the callback function
        def update_minutegraph_live(n):
            fig = plot_live().plot_live_minutes()  # plot live minute graph
            return fig

        # start callback with update interval
        @app.callback(  # update every 10 minutes (600 seconds)
            [
                Output('e_tenMinuteGraph', 'figure'),
                Output('g_tenMinuteGraph', 'figure'),
            ],
            [
                Input('interval-component-tenminutes', 'n_intervals')
            ]
        )
        def update_tenminutegraph(n):
            fig1 = plot_live().plot_live_ten_minutes(etype='E', start=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=2))  # 2 days back from today)
            fig2 = plot_live().plot_live_ten_minutes(etype='G', start=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=2))  # 2 days back from today)
            return fig1, fig2

        # start callback with update interval
        @app.callback(  # update every 30 minutes (half hour)
            Output('e_today', 'figure'),  # energy today output
            Output('g_today', 'figure'),  # gas today output
            Input('interval-component-halfhour', 'n_intervals')  # interval input
        )
        def update_halfhour(n):  # the callback function
            fig1 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_now'), self.elist[0])  # plot energy today
            fig2 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_now'), self.elist[1])  # plot gas today
            return fig1, fig2

        # start callback with update interval
        @app.callback(  # update every 360 minutes (six hours)
            [
                Output('e_yesterday', 'figure'),  # energy yesterday
                Output('g_yesterday', 'figure'),  # gas yesterday
                Output('e_currmonth', 'figure'),  # energy current month
                Output('e_lastmonth', 'figure'),  # energy last month
                Output('g_currmonth', 'figure'),  # gas current month
                Output('g_lastmonth', 'figure'),  # gas last month
                Output('e_year1', 'figure'),  # energy current year per month
                Output('e_year2', 'figure'),  # energy last year per month
                Output('g_year1', 'figure'),  # gas current year per month
                Output('g_year2', 'figure'),  # gas last year per month
                Output('e_fullyear1', 'figure'),  # energy current year per day
                Output('e_fullyear2', 'figure'),  # energy last year per day
                Output('g_fullyear1', 'figure'),  # gas current year per day
                Output('g_fullyear2', 'figure')  # gas last year per day
            ],
            [
                Input('interval-component-sixhours', 'n_intervals')  # interval input
            ]
        )
        def update_sixhours(n):  # the callback function
            fig1 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_yesterday'), self.elist[0])  # plot energy yesterday
            fig2 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_yesterday'), self.elist[1])  # plot gas yesterday
            fig3 = plot_dbdata().plot_month_day(Runtime.td('year_now'), Runtime.td('month_now'), self.elist[0])  # plot energy current month
            fig4 = plot_dbdata().plot_month_day(Runtime.td('year_now'), Runtime.td('last_month'), self.elist[0])  # plot energy last month
            fig5 = plot_dbdata().plot_month_day(Runtime.td('year_now'), Runtime.td('month_now'), self.elist[1])  # plot gas current month
            fig6 = plot_dbdata().plot_month_day(Runtime.td('year_now'), Runtime.td('last_month'), self.elist[1])  # plot gas last month
            fig7 = plot_dbdata().plot_year_month(Runtime.td('year_now'), self.elist[0])  # plot energy current year per month
            fig8 = plot_dbdata().plot_year_month(Runtime.td('last_year'), self.elist[0])  # plot energy last year per month
            fig9 = plot_dbdata().plot_year_month(Runtime.td('year_now'), self.elist[1])  # plot gas current year per month
            fig10 = plot_dbdata().plot_year_month(Runtime.td('last_year'), self.elist[1])  # plot gas last year per month
            fig11 = plot_dbdata().plot_year_day(Runtime.td('year_now'), self.elist[0])  # plot energy current year per day
            fig12 = plot_dbdata().plot_year_day(Runtime.td('last_year'), self.elist[0])  # plot energy last year per day
            fig13 = plot_dbdata().plot_year_day(Runtime.td('year_now'), self.elist[1])  # plot gas current year per day
            fig14 = plot_dbdata().plot_year_day(Runtime.td('last_year'), self.elist[1])  # plot gas last year per day
            return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14

        # Display json structure in frame below graph
        # @app.callback(
        #     Output("structure", "children"),
        #     [Input("graph", "figure")])
        # def display_structure(fig_json):
        #     return json.dumps(fig_json, indent=2)

        # run the webserver
        app.run_server(debug=self.debug, host=self.ip, port=self.port, use_reloader=self.reloader)


def run_default():
    if (Dash_Settings.DASHDEBUG):  # if True then run on 127.0.0.1
        ip = Dash_Settings.local_ip
    else:  # else run on the defined external IP
        ip = Dash_Settings.external_ip

    logger.info(f"Starting Dash on {ip}:{Dash_Settings.port} with debug: {Dash_Settings.DASHDEBUG} and reloader: {Dash_Settings.RELOADER}")
    all_graphs_view().create_dash_page(ip, Dash_Settings.port, Dash_Settings.DASHDEBUG, Dash_Settings.RELOADER)  # go for it


def main(**kwargs):
    global update_db
    while(update_db):  # update the database
        db.main()  # update database always once on loading the file
        update_db = 0
    if "default" in kwargs and kwargs.get("default") is True:  # run with dash_settings.py
        run_default()
    else:  # run with provided settings
        Dash_Settings.DASHDEBUG = kwargs.get("debug")  # overwrite settings with given argument
        Dash_Settings.RELOADER = kwargs.get("debug")  # overwrite settings with given argument
        logger.info(f"Starting Dash on {kwargs.get('ip')}:{kwargs.get('port')} with debug: {Dash_Settings.DASHDEBUG} and reloader: {Dash_Settings.RELOADER}")
        all_graphs_view().create_dash_page(kwargs.get('ip'), kwargs.get('port'), Dash_Settings.DASHDEBUG, Dash_Settings.RELOADER)

# TODO - testing todo's

if __name__ == '__main__':

    default_usage = """Usage:
    python dash_allgraphs_live.py default
    python dash_allgraphs_live.py IP PORT DEBUG

    default = run with dash_settings.py configuration
    IP = local or external ipv4 address to run on
    PORT = port to run on
    DEBUG = True or False for dash debug

    Examples:
    python dash_allgraphs_live.py default
    python dash_allgraphs_live.py 127.0.0.1 80 True
    python dash_allgraphs_live.py 192.168.0.5 8080 False
    """

    if len(sys.argv) <= 1 or len(sys.argv) >= 5:
        print(default_usage)
        sys.exit(1)

    ob = ip_validation()

    while(True):
        if ob.valid_ip_address(sys.argv[1]) == "IPv4":  # check for valid IPv4 address
            if int(sys.argv[2]) >= 1 and int(sys.argv[2]) <= 65535:  # check for valid port
                if sys.argv[3].lower() == "true":  # run if debug is true
                    main(ip=sys.argv[1], port=sys.argv[2], debug=sys.argv[3].lower().capitalize())
                    break
                elif sys.argv[3].lower() == "false":  # run if debug is false
                    main(ip=sys.argv[1], port=sys.argv[2], debug=sys.argv[3].lower().capitalize())
                    break
                else:
                    print(default_usage)
                    break
            else:
                print(default_usage)
                break
        elif ob.valid_ip_address(sys.argv[1]) == "Neither" and sys.argv[1].lower() == "default":  # run default configuration
            main(default=True)
            break
        else:
            print(default_usage)
            break

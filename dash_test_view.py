#!/usr/bin/env python3
"""
    File name: test_view.py
    Author: LouDFPV
    Date created: 15/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    this file tests views defined under graph_test.create_dash_page
    does not auto update the database
    uses settings from dash_settings.py
"""
import datetime

# dash
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Youless setup
from LS120 import Runtime, Youless  # all settings
from LS120.plotly_graphs import plot_dbdata, plot_live  # plots data from database and live reading

# Dash setup
from dash_settings import Dash_Settings
from dash_web_elements import web_elements  # dash web page elements

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("dash_test_view.py started")

# set language
Youless.youless_locale()


class graph_test:
    """class to create dash page with some of the graphs from LS120.plotly_graphs.plot_data"""

    def __init__(self) -> None:
        self.elist = Youless.sql('energytypes')['list']  # retrieve energy types

    def create_dash_page(self, ip, port):
        """Plot one or more graphs with dash and plotly for testing purposes"""
        self.ip = ip
        self.port = port

        # define the app
        app = dash.Dash(
                        __name__,
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

        # define tables to show on page
        live_table_e = web_elements.table_header(Youless.lang('LIVE_TEN_E'), "e_tenMinuteGraph")
        live_table_g = web_elements.table_header(Youless.lang('LIVE_TEN_G'), "g_tenMinuteGraph")
        dual_energy_table = web_elements.dual_table(Youless.lang('TOYE'), "e_today", "e_yesterday")
        dual_gas_table = web_elements.dual_table(Youless.lang('TOYE'), "g_today", "g_yesterday")

        # define layout with defined tables
        app.layout = web_elements.layout_with_intervals(live_table_e, live_table_g, dual_energy_table, dual_gas_table)

        # start callback with update interval
        @app.callback(  # update every minute (60 seconds)
            Output('e_tenMinuteGraph', 'figure'),  # electricity ten minute graph output
            Output('g_tenMinuteGraph', 'figure'),  # gas ten minute graph output
            Input('interval-component-quarterhour', 'n_intervals')  # interval input
        )
        # the callback function
        def update_tenminutegraph_live(n):
            fig1 = plot_live().plot_live_ten_minutes(etype='E', start=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=2))  # 2 days back from today)
            fig2 = plot_live().plot_live_ten_minutes(etype='G', start=datetime.datetime(2021, 7, 22))  # plot live minute graph
            return fig1, fig2

        # start the callback with update interval
        @app.callback(
            [
                Output('e_today', 'figure'),
                Output('e_yesterday', 'figure'),
                Output('g_today', 'figure'),
                Output('g_yesterday', 'figure')
            ],
            [
                Input('interval-component-halfhour', 'n_intervals')
            ]
        )
        def multi_output(n):  # the callback function
            fig1 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_now'), self.elist[0])
            fig2 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_yesterday'), self.elist[0])
            fig3 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_now'), self.elist[1])
            fig4 = plot_dbdata().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_yesterday'), self.elist[1])
            return fig1, fig2, fig3, fig4

        # run the webserver
        app.run_server(debug=Dash_Settings.DASHDEBUG, host=ip, port=port)


def main():
    if (Dash_Settings.DASHDEBUG):  # if True then run on 127.0.0.1
        ip = Dash_Settings.local_ip
    else:  # else run on the defined external IP
        ip = Dash_Settings.external_ip

    logger.info(f"Starting Dash on {ip}:{Dash_Settings.port} with debug: {Dash_Settings.DASHDEBUG}")
    graph_test().create_dash_page(ip, Dash_Settings.port)  # go for it


if __name__ == '__main__':
    main()

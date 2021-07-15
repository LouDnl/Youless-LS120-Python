#!/usr/bin/env python3
"""
    test_view.py

    this file tests views defined under create_dash_page
    does not auto update the database
"""

# dash
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Youless setup
from LS120 import Runtime, Youless  # all settings
from LS120.plotly_graphs import plot_data  # plots data from database
# from LS120 import read_live_data, plot_live  # read and plot live data

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

    def __init__(self):
        self.elist = Youless.sql('energytypes')['list']  # retrieve energy types

    def create_dash_page(self, ip, port):
        """
        Plot one or more graphs with dash and plotly for testing purposes
        """
        self.ip = ip
        self.port = port

        # define the app
        app = dash.Dash(
                        __name__,
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

        # define tables to show on page
        dual_energy_table = web_elements.dual_table(Youless.lang('TOYE'), "e_today", "e_yesterday")
        dual_gas_table = web_elements.dual_table(Youless.lang('TOYE'), "g_today", "g_yesterday")

        # define layout with defined tables
        app.layout = web_elements.layout_with_intervals(dual_energy_table, dual_gas_table)

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
            fig1 = plot_data().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_now'), self.elist[0])
            fig2 = plot_data().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_yesterday'), self.elist[0])
            fig3 = plot_data().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_now'), self.elist[1])
            fig4 = plot_data().plot_day_hour(Runtime.td('year_now'), Runtime.td('month_now'), Runtime.td('day_yesterday'), self.elist[1])
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

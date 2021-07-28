#!/usr/bin/env python3
"""
    File name: dash_web_elements.py
    Author: LouDFPV
    Date created: 15/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file returns web elements for both examples.
    The elements can be used and adapted for your own projects.
    It is not required.
"""
# Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Youless setup
from LS120.constants import Youless

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("web_elements.py started")

# set language
Youless.youless_locale()


class web_elements:
    """this class contains presets for the dash examples"""

    __elements = {
        "css": {
            "page_css": {'position': 'fixed', 'top': '0', 'left': '0', 'right': '0', 'bottom': '0', 'overflow': 'auto', 'width': '100%', 'height': '100%'},
            "row_title": {'text-align': 'center', 'font-size': 'x-large', 'border': 'none', 'border-collapse': 'collapse', 'margin': '0px', 'padding': '0px'},
            "subrow_title": {'text-align': 'center', 'font-size': 'large', 'border': 'none', 'border-collapse': 'collapse', 'margin': '0px', 'padding': '0px'},
            "table_css": {'margin': '0px', 'padding': '0px'},
            "column_css": {'border': 'none', 'border-collapse': 'collapse', 'margin': '0px', 'padding': '0px'}
        }
    }

    @staticmethod
    def layout_with_intervals(*args):
        """returns the webapp layout and intervals for tables as arguments"""
        return html.Div([
            html.Span(id='updatedb', style={'visibility': 'hidden'}),
            *args,
            dcc.Interval(
                id='interval-component-live',
                interval=5*1000,  # 5 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-minute',
                interval=60*1000,  # 60 seconds in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-tenminutes',
                interval=600*1000,  # 600 seconds (10 minutes) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-quarterhour',
                interval=900*1000,  # 900 seconds (15 minutes) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-halfhour',
                interval=1800*1000,  # 1800 seconds (half hour) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-hour',
                interval=3600*1000,  # 3600 seconds (one hour) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-sixhours',
                interval=21600*1000,  # 21600 seconds (six hours) in milliseconds
                n_intervals=0
            )
        ], style=web_elements.elements('css', 'page_css'))

    @staticmethod
    def table_header(head, id1):
        """returns table with single graph and with title header"""
        return dbc.Table([
            html.Tr([
                html.Th(head, colSpan=2, scope="col")
            ], style=web_elements.elements('css')['row_title']),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=web_elements.elements('css')['column_css'])
            ])
        ], style=web_elements.elements('css')['column_css'], borderless=True)

    @staticmethod
    def table_no_head(id1):
        """returns table with single graph no title header"""
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=web_elements.elements('css')['column_css'])
            ])
        ], style=web_elements.elements('css')['column_css'], borderless=True)

    @staticmethod
    def dual_table(head, id1, id2):
        """returns table with two graphs side by side and with title header"""
        return dbc.Table([
            html.Tr([
                html.Th(head, colSpan=2, scope="col")
            ], style=web_elements.elements('css')['row_title']),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=web_elements.elements('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=web_elements.elements('css', 'column_css'))
            ]),
        ], style=web_elements.elements('css')['table_css'], borderless=True)

    @staticmethod
    def dual_table_no_head(id1, id2):
        """returns table with two graphs side by side with no title header"""
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=web_elements.elements('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=web_elements.elements('css', 'column_css'))
            ]),
        ], style=web_elements.elements('css')['table_css'], borderless=True)

    @staticmethod
    def quad_table_header(head, id1, id2, id3, id4):
        """returns table with four graphs and with title header, two tables side by side and two tables below that. each row of two tables has a row header"""
        return dbc.Table([
            html.Tr([
               html.Th(head, colSpan=2, scope="col")
            ], style=web_elements.elements('css')['row_title']),
            html.Tr([
               html.Th(Youless.lang('ELE'), colSpan=2, scope="col", style=web_elements.elements('css', 'subrow_title'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=web_elements.elements('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=web_elements.elements('css', 'column_css'))
            ]),
            html.Tr([
               html.Th(Youless.lang('GAS'), colSpan=2, scope="col", style=web_elements.elements('css', 'subrow_title'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id3), style=web_elements.elements('css', 'column_css')),
                html.Td(dcc.Graph(id=id4), style=web_elements.elements('css', 'column_css'))
            ])
        ], style=web_elements.elements('css')['table_css'], borderless=True)

    @staticmethod
    def quad_table_no_head(id1, id2, id3, id4):
        """returns table with four graphs with no headers, two tables side by side and two tables below that"""
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=web_elements.elements('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=web_elements.elements('css', 'column_css'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id3), style=web_elements.elements('css', 'column_css')),
                html.Td(dcc.Graph(id=id4), style=web_elements.elements('css', 'column_css'))
            ])
        ], style=web_elements.elements('css')['table_css'], borderless=True)

    @staticmethod
    def elements(name, *args):
        """returns item from elements dictionary, add second argument to return dictionary from key

        examples:
            :web_elements.elements("keyname") -> returns its contents
            :web_elements.elements("keyname", "secondkeyname") -> returns the dictionary within the dictionary
            :web_elements.elements("keyname")["second_keyname"]["etc"] -> same as above
        """
        if (args == ()):
            return web_elements.__elements[name]
        else:
            return web_elements.__elements[name].get(args[0])  # only the first extra argument will be processed, others will be ignored

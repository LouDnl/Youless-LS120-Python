#!/usr/bin/env python3
"""
    This file returns web elements for both examples.
    The elements can be used and adapted for your own projects.
    It is not required.
"""
import sys

# Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Youless setup
from .settings import Youless

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("web_elements.py started")

# set language
Youless.youless_locale()


class web_elements:

    @staticmethod
    def layout_with_intervals(*args):
        """
            returns the webapp layout for tables as arguments
            returns intervals
        """
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
        ], style=Youless.web('css', 'page_css'))

    @staticmethod
    def table_header(head, id1):
        """
            returns table with single graph and with title header
        """
        return dbc.Table([
            html.Tr([
                html.Th(head, colSpan=2, scope="col")
            ], style=Youless.web('css', 'row_title')),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Youless.web('css')['column_css'])
            ])
        ], style=Youless.web('css')['column_css'], borderless=True)

    @staticmethod
    def table_no_head(id1):
        """
            returns table with single graph no title header
        """
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Youless.web('css')['column_css'])
            ])
        ], style=Youless.web('css')['column_css'], borderless=True)

    @staticmethod
    def dual_table(head, id1, id2):
        """
            returns table with two graphs side by side and with title header
        """
        return dbc.Table([
            html.Tr([
                html.Th(head, colSpan=2, scope="col")
            ], style=Youless.web('css', 'row_title')),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Youless.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Youless.web('css', 'column_css'))
            ]),
        ], style=Youless.web('css', 'table_css'), borderless=True)

    @staticmethod
    def dual_table_no_head(id1, id2):
        """
            returns table with two graphs side by side with no title header
        """
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Youless.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Youless.web('css', 'column_css'))
            ]),
        ], style=Youless.web('css', 'table_css'), borderless=True)

    @staticmethod
    def quad_table_header(head, id1, id2, id3, id4):
        """
            returns table with four graphs and with title header
            two tables side by side and two tables below that
            each row of two tables has a row header
        """
        return dbc.Table([
            html.Tr([
               html.Th(head, colSpan=2, scope="col")
            ], style=Youless.web('css', 'row_title')),
            html.Tr([
               html.Th(Youless.lang('ELE'), colSpan=2, scope="col", style=Youless.web('css', 'subrow_title'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Youless.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Youless.web('css', 'column_css'))
            ]),
            html.Tr([
               html.Th(Youless.lang('GAS'), colSpan=2, scope="col", style=Youless.web('css', 'subrow_title'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id3), style=Youless.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id4), style=Youless.web('css', 'column_css'))
            ])
        ], style=Youless.web('css', 'table_css'), borderless=True)

    @staticmethod
    def quad_table_no_head(id1, id2, id3, id4):
        """
            returns table with four graphs with no headers
            two tables side by side and two tables below that
        """
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Youless.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Youless.web('css', 'column_css'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id3), style=Youless.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id4), style=Youless.web('css', 'column_css'))
            ])
        ], style=Youless.web('css', 'table_css'), borderless=True)


if __name__ == '__main__':
    sys.exit()

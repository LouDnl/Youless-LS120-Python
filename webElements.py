"""
    Configuring all web elements
"""

import sys, os, datetime, time
import warnings

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# youless specific
from globals import *

class Web:

    # @staticmethod
    # def live_graphs_layout(args):
    #     return html.Div([
    #         args[0],
    #     ])

    @staticmethod
    def layout_with_intervals(*args):
        """
            returns the webapp layout and intervals with supplied tables as arguments
        """
        return html.Div([
            html.Span(id='updatedb', style={'visibility': 'hidden'}),
            *args,
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
                interval=1800*1000, # 1800 seconds (half hour) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-hour',
                interval=3600*1000, # 3600 seconds (one hour) in milliseconds
                n_intervals=0
            ),
            dcc.Interval(
                id='interval-component-sixhours',
                interval=21600*1000, # 21600 seconds (six hours) in milliseconds
                n_intervals=0
            )            
        ], style=Vars.web('css', 'page_css'))

    @staticmethod
    def table_header(head,id1): # single graph. with title header.
        return dbc.Table([
            html.Tr([
                html.Th(head, colSpan=2, scope="col") 
            ], style=Vars.web('css', 'row_title')),            
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Vars.web('css')['column_css'])
            ])
        ], style=Vars.web('css')['column_css'], borderless=True)

    @staticmethod
    def table_no_head(id1): # single graph. no header.
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Vars.web('css')['column_css'])
            ])
        ], style=Vars.web('css')['column_css'], borderless=True)

    @staticmethod
    def dual_table(head, id1, id2): # two graphs side by side. with title header
        return dbc.Table([
            html.Tr([
                html.Th(head, colSpan=2, scope="col") 
            ], style=Vars.web('css', 'row_title')),
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Vars.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Vars.web('css', 'column_css'))
            ]),
        ], style=Vars.web('css', 'table_css'), borderless=True)

    @staticmethod
    def dual_table_no_head(id1, id2): # two graphs side by side. no header
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Vars.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Vars.web('css', 'column_css'))
            ]),
        ], style=Vars.web('css', 'table_css'), borderless=True)

    @staticmethod
    def quad_table_header(head,id1,id2,id3,id4): # four graphs, two per type side by side. with title header and each type has header.
        return dbc.Table([
            html.Tr([
               html.Th(head, colSpan=2, scope="col") 
            ],style=Vars.web('css', 'row_title')),            
            html.Tr([
               html.Th(Vars.lang('ELE'), colSpan=2, scope="col", style=Vars.web('css', 'subrow_title'))
            ]),        
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Vars.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Vars.web('css', 'column_css'))
            ]),
            html.Tr([
               html.Th(Vars.lang('GAS'), colSpan=2, scope="col", style=Vars.web('css', 'subrow_title'))
            ]),                
            html.Tr([
                html.Td(dcc.Graph(id=id3), style=Vars.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id4), style=Vars.web('css', 'column_css'))
            ])
        ], style=Vars.web('css', 'table_css'), borderless=True)
        
    @staticmethod
    def quad_table_no_head(id1,id2,id3,id4): # 4 graphs, 2 per type side by side. no title and no headers
        return dbc.Table([
            html.Tr([
                html.Td(dcc.Graph(id=id1), style=Vars.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id2), style=Vars.web('css', 'column_css'))
            ]),
            html.Tr([
                html.Td(dcc.Graph(id=id3), style=Vars.web('css', 'column_css')),
                html.Td(dcc.Graph(id=id4), style=Vars.web('css', 'column_css'))
            ])
        ], style=Vars.web('css', 'table_css'), borderless=True)

def main():
    log(lambda: "I do not run on my own...")

if __name__ == '__main__':
        main()            
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import requests
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from __init__ import dash_app


# Define the layout of the dashboard using Dash Bootstrap Components
dash_app.layout = dbc.Container ([
    dbc.Row([
        dbc.Col(
            html.H1("My Beautiful Dashboard",
                    className="text-center mb-8"),
                    width=12)]
    ),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='my-graph'),
            width={'size': 8, 'offset': 2}
        )],
        style={"height": "650px"}
    ),

    dbc.Row([
        dbc.Col(
            html.Div(id='my-table'),
            width={'size': 8, 'offset': 2}
        )],
        style={"height": "650px"}
    ),

    dbc.Row([
        dbc.Col(
            dbc.Button("Refresh Data", id='refresh-button', color='primary', className='mr-2'),
            width={'size': 2, 'offset': 5}
        )]
    ),


    dcc.Interval(
        id='interval-component',
        interval=60 * 100000,  # Update every 10 minute
        n_intervals=0
    )

], fluid=True)


# Define the callback to update the graph and table
@dash_app.callback(
    [Output('my-graph', 'figure'),
     Output('my-table', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('refresh-button', 'n_clicks')]
)
def update_dashboard(n_intervals, n_clicks):
    # Fetch data from the Flask backend
    response = requests.get('http://127.0.0.1:8156/comm/dash')
    data = response.json()

    df = pd.DataFrame(data)

    # Create a graph
    # for go.scatter, use mode='lines+markers in go.Scatter
    figure = {
        'data': [
            go.Bar (
                x=df['id'],
                y=df['tag2']
            )
        ],
        'layout': go.Layout(
            title='Sample Graph',
            xaxis={'title': 'X-axis'},
            yaxis={'title': 'Y-axis'},
            height=600
        )
    }

    # Create a table
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    return figure, table


if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8050)
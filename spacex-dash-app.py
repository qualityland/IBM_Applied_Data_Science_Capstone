# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# initialize list of launch site options
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in sorted(spacex_df['Launch Site'].unique()):
    site_options.append({'label': site, 'value': site})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=site_options,
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(spacex_df[spacex_df['class'] == 1].groupby('Launch Site', as_index=False).count(),
                     values='Flight Number',
                     names='Launch Site',
                     title='Succesful launches for all sites')
        return fig
    else:
        df = spacex_df[spacex_df['Launch Site'] == site].groupby('class', as_index=False).count()
        fig = px.pie(df,
                     values='Flight Number',
                     names='class',
                     title='Launch success/failure for site ' + site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(site, payload):
    if site == 'ALL':
        df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
        figure = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return figure
    else:
        df = spacex_df[(spacex_df['Launch Site'] == site) & (spacex_df['Payload Mass (kg)'].between(payload[0], payload[1]))]
        figure = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return figure


# Run the app
if __name__ == '__main__':
    app.run_server()

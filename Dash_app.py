# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(
                                               id='site-dropdown',  # Attribute: ID for the component
                                               options=[
                                               {'label': 'All Sites', 'value': 'ALL'},
                                               {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                               {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                               {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                               {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                 ],  # Attribute: List of option objects with label and value attributes

                                                value='ALL',  # Attribute: Default dropdown value set to 'ALL'

                                                placeholder='Select a Launch Site here',  # Attribute: Placeholder text

                                                searchable=True  # Attribute: Allow for searching launch sites
                                                ),  
                                
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                id='payload-slider',  # Attribute: ID for the component
                                min=0,  # Attribute: Minimum payload value (0 Kg)
                                max=10000,  # Attribute: Maximum payload value (10,000 Kg)
                                step=1000,  # Attribute: Slider interval (1,000 Kg)
                                value=[min_payload, max_payload]  # Attribute: Initial selected range (from min_payload to max_payload)
                                  ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If 'ALL' sites are selected, use all rows in the dataframe to render a pie chart for total success launches
        fig = px.pie(
            spacex_df,
            names='class',
            title='Total Success Launches'
        )
    else:
        # If a specific launch site is selected, filter the dataframe for the selected site and render a pie chart for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs. Failure for {entered_site}'
        )

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # If 'ALL' sites are selected, render a scatter plot with all payload values, mission outcomes, and color-labeled by booster version
        fig = px.scatter(
            spacex_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Mission Outcome for All Sites'
        )
    else:
        # If a specific launch site is selected, filter the data and render a scatter plot for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Mission Outcome for {selected_site}'
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

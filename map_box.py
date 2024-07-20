import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv('data/GlobalWeatherRepository.csv')

def create_plot():

    # Create Plotly scatter mapbox plot
    fig = px.scatter_mapbox(
        df,
        lat="latitude",  # Latitude data column
        lon="longitude", # Longitude data column 
        color="temperature_celsius", # Color data for points
        color_continuous_scale=px.colors.cyclical.IceFire, # Color scale
        hover_name='location_name', # Add hover value
        size="humidity", # Based on size data will change
        size_max=7,  # Maximum size for points
        labels={ 
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'temperature_celsius' : 'Temperature (°C)',
            'humidity': 'Humidity'
        },
        height=600,
        width=1000
    )
    fig.update_layout(
        mapbox_style='open-street-map', # Map style
        title="Temperature and Humidity",  # Title of the map
        hovermode='closest',  # Hover mode for interactivity
        mapbox=dict(
            bearing=0, # Bearing of the map
            center=go.layout.mapbox.Center(
                lat=47, # Center latitude
                lon=12 # Center longitude
            ),
            pitch=0, # Map pitch
            zoom=4 # Initial map zoom level
        )
    )

    # Return the Plotly figure as HTML
    return fig.to_html(full_html=False)

def create_temperature_histogram():
    temperature_mean = df['temperature_celsius'].mean()

    df['last_updated'] = pd.to_datetime(df['last_updated'])

    last_updated = df['last_updated'].max().strftime('%Y-%m-%d %H:%M:%S')

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value= temperature_mean,
        title={'text' : 'Temperature (°C)'},
        gauge= { 'axis' : {'range' : [None, 50]},
                'bar': {'color': "#008000"},
                'steps' : [
                    {'range' : [0, 10], 'color' : "#440154"}, 
                    {'range' : [10, 20], 'color' : "#3b528b"},
                    {'range' : [20, 30], 'color' : "#21918c"},
                    {'range' : [30, 40], 'color' : "#5ec962"},
                    {'range' : [40, 50], 'color' : "#fde725"}
                ],
                'threshold' : {
                    'line' : {'color' : 'red', 'width' : 5},
                    'thickness' : 0.75,
                    'value' : temperature_mean,
                }
        }
    ))

    fig.update_layout(
        title = "Average global temperature <br>(updated " + last_updated + ")"
    )

    return fig.to_html(full_html=False)

def create_temperature_time_series():
    weather = pd.read_csv('global_weather.csv')
    fig = px.line(weather, x='date', y='temperature_celsius', title='Temperature Over Time')
    return fig.to_html(full_html=False)
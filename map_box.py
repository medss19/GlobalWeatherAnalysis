import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import ipywidgets as widgets
from ipywidgets import interactive

# Load dataset
df = pd.read_csv('data/GlobalWeatherRepository.csv')

temperature_mean = df['temperature_celsius'].mean()

df['last_updated'] = pd.to_datetime(df['last_updated'])
last_updated = df['last_updated'].max().strftime('%Y-%m-%d %H:%M:%S')
average_temp_by_country_year = df.groupby([df['last_updated'].dt.year, 'country'])['temperature_celsius'].mean().reset_index()
average_temp_by_country_year.columns = ['year', 'country', 'average_temperature']


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

def avg_global_temp():
    
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

def hottest_countries():
    top_countries = average_temp_by_country_year.groupby('country')['average_temperature'].mean().nlargest(5).reset_index()
    top_countries = top_countries.sort_values(by='average_temperature')

    fig = px.bar(top_countries, x='average_temperature', y='country', orientation='h', 
                title='Top 5 hottest countries', labels={'average_temperature': 'Average temperature (°C)', 'country': 'Countries'},
                text=top_countries['average_temperature'].round(2).astype(str) + ' °C'

    )

    fig.update_traces(hovertemplate='')
    fig.update_traces(hoverinfo='none')

    return fig.to_html(full_html=False)

def coldest_countries():
    top_countries = average_temp_by_country_year.groupby('country')['average_temperature'].mean().nsmallest(5).reset_index()
    top_countries = top_countries.sort_values(by='average_temperature')

    fig = px.bar(top_countries, x='average_temperature', y='country', orientation='h', 
                title='Top 5 coldest countries', labels={'average_temperature': 'Average temperature (°C)', 'country': 'Countries'},
                text=top_countries['average_temperature'].round(2).astype(str) + ' °C'

    )

    fig.update_traces(hovertemplate='')
    fig.update_traces(hoverinfo='none')

    return fig.to_html(full_html=False)

def choro_map():
    fig = px.choropleth(
        average_temp_by_country_year,
        locations="country",
        locationmode="country names",
        color="average_temperature",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Viridis,
        projection="equal earth",
        title="Temperaturas Medias Globales"
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig.to_html(full_html=False)



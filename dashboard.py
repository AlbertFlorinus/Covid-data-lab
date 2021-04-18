import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
df = df.drop(columns='Province/State')
df = df.rename(columns={'Country/Region': 'Country'})
df['Date'] = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in df['Date']]

df = df.groupby(['Date', 'Country'], as_index=False)['Confirmed'].sum()

def get_data_from_country(country):
    return df.loc[df['Country'] == country]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="country_menu",
        options=[{"label": x, "value": x} for x in df['Country'].unique()],
        multi=False,
        value="Sweden"
    ),
    dcc.Graph(id="confirmed_chart"),
])

@app.callback(
    Output("confirmed_chart", "figure"), 
    [Input("country_menu", "value")])
def update_graph(country):
	country_data_frame = get_data_from_country(country)
	fig = px.bar(country_data_frame, x='Date', y='Confirmed', title='Confirmed cases by country')
	return fig

app.run_server(debug=True)
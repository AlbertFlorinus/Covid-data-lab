import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

# Downloading the data from github, will download the latest every time the applikation is starting
df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

# Restructuring the data
df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
df = df.rename(columns={'Country/Region': 'Country'})

# Converting the date format
df['Date'] = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in df['Date']]

# Sorting and grouping the data by date and country, the data of the states will be summed by each country by each date.
df = df.groupby(['Date', 'Country'], as_index=False)['Confirmed'].sum()

# Selects a subsed of the dataframe based on country
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
    dcc.DatePickerRange(
    	id='date_picker',
    	day_size=40,
    	min_date_allowed=list(df['Date'])[0],
    	max_date_allowed=list(df['Date'])[-1],
    	updatemode='singledate',
    	start_date=list(df['Date'])[0],
    	end_date=list(df['Date'])[-1],
    	reopen_calendar_on_clear=True,
    	end_date_placeholder_text="End"),
    dcc.Graph(id="confirmed_chart"),
])

# Is triggered by an event, input is the value to the function, comed from the app layout
@app.callback(
    Output("confirmed_chart", "figure"), 
    [Input("country_menu", "value"),
     Input("date_picker", "start_date"),
     Input("date_picker", "end_date")])
def update_graph(country, start_date, end_date):
	start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
	end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

	dfc = get_data_from_country(country)
	dfcc = dfc[(dfc['Date'] > start_date) & (dfc['Date'] <= end_date)]
	fig = px.bar(dfcc, x='Date', y='Confirmed', title='Confirmed cases by country')
	return fig

app.run_server(debug=True)
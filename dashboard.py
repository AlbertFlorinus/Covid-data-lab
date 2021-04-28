import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

from User_class import User

#creating userinstance (with timeseries data format)
user = User()

# Confirmed cases ----------------------------------------------

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

# Healthcare ----------------------------------------------
raw_df = pd.read_json('https://www.svt.se/special/articledata/2532/alder_data.json')
dic = {}

for index in range(len(raw_df)):
    dic[raw_df.iloc[index][1]['datum']] = [i for i in raw_df.iloc[index][1].values()]
healthcare_df = pd.DataFrame.from_dict(dic, orient='index', columns=[i for i in raw_df.iloc[0][1]])

def healthcare_graph(healthcare_df):
    columns = []
    for column in healthcare_df.columns:
        if 'unika personer totalt' in column:
            columns.append(column)
    dates = healthcare_df.index
    healthcare_fig = px.area(healthcare_df, x=dates, y=columns)
    return healthcare_fig

# Gives the total number of deaths worldwide at the last date in the dataframe df 
def total_deaths_worldwide():
    total_deaths = df[df['Date'] == df.iloc[-1][0]]['Confirmed'].sum()
    return total_deaths

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
    f'Total number of deceased worldwide:{ total_deaths_worldwide() }'
    ),
	html.H1(
    	'Covid Datalab'),
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
    html.H1(
        'Healtcare'),
    dcc.Graph(figure=healthcare_graph(healthcare_df)),

    html.H1("World view"), 
    dcc.Graph(id="world_map",figure=user.plot_world_data(category="confirmed")),
    dcc.Dropdown(
        id='Case_type',

        #Hur löser vi flera outputs?
        options=[{"label": "confirmed", "value": "confirmed"},
                {"label": "deaths","value": "deaths"},
                {"label": "recovered", "value": "recovered"}],

        multi=False,
        value="confirmed"
    )])

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
	dfcc = dfc[(dfc['Date'] >= start_date) & (dfc['Date'] <= end_date)]
	fig = px.bar(dfcc, x='Date', y='Confirmed', title='Confirmed cases by country')
	return fig










app.run_server(debug=True)

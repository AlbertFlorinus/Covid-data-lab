import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

from User_class import User


def reshape_data(df, type_of_data):
    '''Reshapes john hopkins data to a nicer format'''
    df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name=type_of_data)
    df['Date'] = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in df['Date']]
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.groupby(['Date', 'Country'], as_index=False)[type_of_data].sum() # Date and Country shold be uniqe
    return df


def create_healthcare_data():
    df = pd.read_json('https://www.svt.se/special/articledata/2532/alder_data.json')
    dic = {}
    columns = []
    for index in range(len(df)):
        dic[df.iloc[index][1]['datum']] = [i for i in df.iloc[index][1].values()]
        
    df = pd.DataFrame.from_dict(dic, orient='index', columns=[i for i in df.iloc[0][1]])  
    for column in df.columns:
        if 'totalt' in column and 'unika personer totalt' not in column:
            columns.append(column)

    columns.remove('100-109 totalt')
    columns.remove('110-119 totalt')
    columns.sort()
    df = df[columns]
    return df


def create_global_data():
    ''' Creates a dataframe with all data combined. It uses a reshape_data function to get into proper format.
    The data itself comes from John Hopkins github-page. '''
    deaths    = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    active    = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    
    deaths = reshape_data(deaths, 'Deaths')
    active = reshape_data(active, 'Active')
    confirmed = reshape_data(confirmed, 'Confirmed')
    
    df = pd.merge(deaths, confirmed, how='inner', on=['Date', 'Country'])
    df = pd.merge(df, active, how='inner', on=['Date', 'Country'])
    return df


def healthcare_graph(df):
    dates = healthcare_df.index
    fig = px.line(df, x=dates, y=df.columns)
    return fig


def pi_graph(df):
    fig = px.pie(df, names=df.columns[:-1], values=df[df.columns[:-1]].iloc[-1], title='Number of people who been signed to a hospital in Sweden until today')
    return fig


def total_deaths_worldwide(df):
    total_deaths = df[df['Date'] == df.iloc[-1][0]]['Confirmed'].sum()
    return total_deaths


def get_data_from_country(country, df):
    return df.loc[df['Country'] == country]


user = User()

df = create_global_data()
healthcare_df = create_healthcare_data()

date_list = list(df['Date'].unique())
date_map = [i for i in range(len(date_list))]
months = list(pd.date_range(start=date_list[0], end=date_list[-1], freq='M'))

month_codes = {
    1:'Jan',  
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'Jun',
    7:'Jul',
    8:'Aug',
    9:'Sep',
    10:'Okt',
    11:'Nov',
    12:'Dec'
}

marks = {}
for d in months:
    marks[date_list.index(d)] = f'{month_codes[d.month]} {d.year}'


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Covid Datalab'),
    html.H3("Total number of deceased worldwide: {:,}".format(total_deaths_worldwide(df))),
    dcc.Dropdown(
        id="country_menu",
        options=[{"label": x, "value": x} for x in df['Country'].unique()],
        multi=False,
        value="Sweden"),
    dcc.Dropdown(
        id="status_menu",
        options=[{"label": "Confirmed", "value": "Confirmed"}, 
                 {"label": "Deaths", "value": "Deaths"}, 
                 {"label": "Active", "value": "Active"}],
        multi=False,
        value="Confirmed"),
    dcc.Graph(id="confirmed_chart"),
    html.Div(dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=date_map[-1],
        step=1,
        marks=marks,
        value=[0, date_map[-1]])),
    html.Div(id='output-container-range-slider'),
    html.H1("World view"), 
    dcc.Graph(id="world_map",figure=user.plot_world_data(category="confirmed")),
    dcc.Dropdown(
        id='Case_type',
        options=[{"label": "confirmed", "value": "confirmed"},
                {"label": "deaths","value": "deaths"},
                {"label": "recovered", "value": "recovered"}],

        multi=False,
        value="confirmed"
    ),
    html.H1('Healtcare'),
    dcc.Graph(figure=healthcare_graph(healthcare_df)),
    dcc.Graph(figure=pi_graph(healthcare_df))
])

# Is triggered by an event, input is the value to the function, comed from the app layout
@app.callback(
    Output("confirmed_chart", "figure"), 
    [Input("country_menu", "value"),
     Input("status_menu", "value"),
     Input("my-range-slider", "value")])
def _update_graph(country, status, dates):
    #start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    #end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    start_date = date_list[dates[0]]
    end_date = date_list[dates[1]]

    dfc = get_data_from_country(country, df)
    dfcc = dfc[(dfc['Date'] >= start_date) & (dfc['Date'] <= end_date)]
    fig = px.bar(dfcc, x='Date', y=status, title='Confirmed cases by country')
    return fig

app.run_server(debug=True)






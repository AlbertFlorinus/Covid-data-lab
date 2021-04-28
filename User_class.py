import datetime
import plotly.express as px
import pandas as pd

class User():
    def __init__(self):
        #first data on record, for later.
        self.inception = datetime.date(year=2020, month = 1, day=22)

        #formatting "todays" date as 10/1/21 being Januari 1, 2021. It is actually one day behind, since the datasource is not always on time,
        #prevents crashing
        self.temporary = datetime.datetime.today()- datetime.timedelta(days=1)
        self.today = self.temporary.strftime('%m/%d/%Y')[1:]
        self.Curr_Date = self.today[:-4]+self.today[-2:]

        #Colleting the three case categories data
        self.df_confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
        self.df_deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
        self.df_recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    
    def select_country(self, nation):
        #not used atm.
        self.nation = nation
    
    def plot_world_data(self, category = "confirmed"):
        K = lambda category : self.df_confirmed if category.lower() == "confirmed" else (self.df_deaths if category.lower() == "deaths" else self.df_recovered)
        y = K(category)
        y.rename(columns={'Province/State':'province', 'Country/Region':'country', 'Lat':'latitude', 'Long':'longitude'}, inplace=True)

        #Uses the coordinates to display correct locations on the worldmap.
        fig = px.scatter_geo(y[self.Curr_Date], lat=y["latitude"], lon=y["longitude"], projection="natural earth", hover_name=y["country"]+f", {category} cases", size=y[self.Curr_Date])
        return fig


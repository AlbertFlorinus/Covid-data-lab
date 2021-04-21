from setup import sql_connect, read_txtfile
import numpy as np
import datetime
import plotly.express as px
import pandas as pd

class User():

    def __init__(self):
        password, db_name = read_txtfile()
        self.engine = sql_connect(password, db_name)
        self.inception = datetime.date(year=2020, month = 1, day=22)

    def select_country(self, nation):
        self.nation = nation

    def get_country_configs(self):
        """
        Returns np.arrays of selected nations confirmed cases from the DB,
        If theres multiple Provinces the numpy array is the columnwise sum of all provinces.
        """
        self.df_conf = pd.read_sql_table("confirmed",con=self.engine)
        self.df_deaths = pd.read_sql_table("deaths",con=self.engine)
        self.df_recovered = pd.read_sql_table("recovered",con=self.engine)

    def plot_world_data(self, category = "confirmed"):
        """
        Testing needed to confirm dates match correctly,
        as in day 60 is day 60 and not day 61 from sql.
        """
        # K returns data of category chosen
        K = lambda category : self.df_conf if category.lower() == "confirmed" else (self.df_deaths if category.lower() == "deaths" else self.df_recovered)
        y = K(category)
        y.rename(columns={'Province/State':'province', 'Country/Region':'country', 'Lat':'latitude', 'Long':'longitude'}, inplace=True)
        fig = px.scatter_geo(y["4/20/21"], lat=y["latitude"], lon=y["longitude"], projection="natural earth", hover_name=y["country"]+f", {category} cases", size=y["4/10/21"])
        fig.show()

if __name__ == "__main__":
    #example, currently prone to errors if done in another order
    User1 = User()
    User1.get_country_configs()
    User1.plot_world_data(category="confirmed")

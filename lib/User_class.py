from setup import sql_connect
import matplotlib.pyplot as plt
import numpy as np
print("test")
class User():

    def __init__(self):
        password = str(input("SQL root password: "))
        db_name = str(input("Name of database: "))
        self.engine = sql_connect(password, db_name)

    def select_country(self, nation):
        self.nation = nation

    def get_country_conf(self):
        """
        Returns a np.array of selected nations confirmed cases from the DB,
        If theres multiple Provinces the numpy array is the columnwise sum of all provinces.
        """
        all_rows = np.array(self.engine.execute(f"SELECT * FROM confirmed where country like '{self.nation}'").fetchall())
        only_date_cols = all_rows[:,5:].astype(int)
        self.confirmed = np.sum(only_date_cols, axis = 0)

    def get_country_deaths(self):
        """
        Returns a np.array of selected nations confirmed cases from the DB,
        If theres multiple Provinces the numpy array is the columnwise sum of all provinces.
        """
        all_rows = np.array(self.engine.execute(f"SELECT * FROM deaths where country like '{self.nation}'").fetchall())
        only_date_cols = all_rows[:,5:].astype(int)
        self.deaths = np.sum(only_date_cols, axis = 0)

    def get_country_recovered(self):
        """
        Returns a np.array of selected nations confirmed cases from the DB,
        If theres multiple Provinces the numpy array is the columnwise sum of all provinces.
        """
        all_rows = np.array(self.engine.execute(f"SELECT * FROM recovered where country like '{self.nation}'").fetchall())
        only_date_cols = all_rows[:,5:].astype(int)
        self.recovered = np.sum(only_date_cols, axis = 0)

    def plot_data(self, category = "confirmed"):
        """
        Testing needed to confirm dates match correctly,
        as in day 60 is day 60 and not day 61 from sql.
        """
        # K returns data of category chosen
        K = lambda category : self.confirmed if category.lower() == "confirmed" else (self.deaths if category.lower() == "deaths" else self.recovered)
        y = K(category)

        x = np.arange(0, y.size)
        plt.title(f"{category} cases of {self.nation}") 
        plt.xlabel("Days since 2020/01/22") 
        plt.ylabel(f"{category} Cases") 
        plt.plot(x, y, color ="red") 
        plt.show()


if __name__ == "__main__":
    #example, currently prone to errors if done in another order
    User1 = User()
    User1.select_country("china")
    User1.get_country_conf()
    User1.get_country_deaths()
    User1.get_country_recovered()

    User1.plot_data(category="confirmed")

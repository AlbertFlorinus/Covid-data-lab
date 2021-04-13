import pandas as pd
import numpy as np
from setup import sql_connect

password = str(input("SQL root password: "))
db_name = str(input("Name of database: "))
engine = sql_connect(password, db_name)

def get_country_conf(engine, nation = "Canada"):
    """
    Returns a np.array of selected nations confirmed cases from the DB,
    If theres multiple Provinces the numpy array is the columnwise sum of all provinces.
    """
    all_rows = np.array(engine.execute(f"SELECT * FROM confirmed_global_cases where Country like '{nation}'").fetchall())
    only_date_cols = all_rows[:,5:]
    nationwide = np.sum(only_date_cols, axis = 0)
    return nationwide

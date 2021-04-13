import pandas as pd
from sqlalchemy import create_engine

def sql_connect(password, db_name, port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    return engine

def confirmed_to_sql(engine):
    engine.execute("DROP TABLE IF EXISTS confirmed")
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    df.rename(columns={'Province/State':'province', 'Country/Region':'country', 'Lat':'latitude', 'Long':'longitude'}, inplace=True)
    df.to_sql('confirmed', con=engine)

def deaths_to_sql(engine):
    engine.execute("DROP TABLE IF EXISTS deaths")
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    df.rename(columns={'Province/State':'province', 'Country/Region':'country', 'Lat':'latitude', 'Long':'longitude'}, inplace=True)
    df.to_sql('deaths', con=engine)

def recovered_to_sql(engine):
    engine.execute("DROP TABLE IF EXISTS recovered")
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    df.rename(columns={'Province/State':'province', 'Country/Region':'country', 'Lat':'latitude', 'Long':'longitude'}, inplace=True)
    df.to_sql('recovered', con=engine)

if __name__ == "__main__":
    #Renamed some columns for SQL compatability for now.
    db_name = str(input("Name of database: "))
    password = str(input("SQL root password: "))
    engine = sql_connect(password, db_name)
    confirmed_to_sql(engine)
    deaths_to_sql(engine)
    recovered_to_sql(engine)




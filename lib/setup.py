import pandas as pd
from sqlalchemy import create_engine

def sql_connect(password, db_name, port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    return engine

def confirmed_to_sql(engine):
    engine.execute("DROP TABLE IF EXISTS confirmed_global_cases")
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    df.rename(columns={'Country/Region':'Country'}, inplace=True)
    df.to_sql('confirmed_global_cases', con=engine)

def deaths_to_sql(engine):
    engine.execute("DROP TABLE IF EXISTS deaths_global_cases")
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    df.rename(columns={'Country/Region':'Country'}, inplace=True)
    df.to_sql('deaths_global_cases', con=engine)

def recovered_to_sql(engine):
    engine.execute("DROP TABLE IF EXISTS recovered_global_cases")
    df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    df.rename(columns={'Country/Region':'Country'}, inplace=True)
    df.to_sql('recovered_global_cases', con=engine)

if __name__ == "__main__":
    #Column Country/Region named for SQL compatability for now
    db_name = str(input("Name of database: "))
    password = str(input("SQL root password: "))
    engine = sql_connect(password, db_name)
    confirmed_to_sql(engine)
    deaths_to_sql(engine)
    recovered_to_sql(engine)




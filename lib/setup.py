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

def create_txtfile(password, Database_name):
    """
    Creates a txt file containing database name and password
    """
    L = [f"{password}\n", f"{Database_name}\n"]
    # Writing to file
    with open("pass_name.txt", "w") as f:
        f.writelines(L)

def read_txtfile():
    """
    opens the txt file and returns content
    """
    # Opening file
    with open("pass_name.txt", "r") as f:
        creds = []
        for line in f:
            creds.append(line.strip())

    Database_name = creds[0]
    password = creds[1]
    return Database_name, password

if __name__ == "__main__":

    #try/except here is to not require input from the user if setup has already been done.
    try:
        password, db_name = read_txtfile()
    except:
        print("txt file not created, input password and name of database \n")
        password = str(input("Enter SQL root password: "))
        db_name = str(input("Enter name of database: "))
        create_txtfile(password, db_name)
    
    engine = sql_connect(password, db_name)
    confirmed_to_sql(engine)
    deaths_to_sql(engine)
    recovered_to_sql(engine)




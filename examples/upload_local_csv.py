import pandas as pd
from tkinter.filedialog import askopenfilename
from sqlalchemy import create_engine

def csv_to_sql(password, db_name = "Corona", port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    df = pd.read_csv(askopenfilename())
    df.to_sql('confirmed_arch', con=engine)

if __name__ == "__main__":
    password = str(input("password: "))
    csv_to_sql(password)


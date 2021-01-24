from sqlite3 import connect
from os import (
    listdir,
    path
)
from csv import reader
from pandas import read_csv

from schema import (
    setup_schema,
    drop_schema
)
from data import order_data

#imports the data
dbpath = "./real-estate-data.db"
setup_schema(dbpath)
for fname in listdir("../data"):
    if fname.endswith(".csv"):
        table_name = path.basename(fname[:-4])
        fpath = f"../data/{fname}"
        con = connect(dbpath)
        df = read_csv(fpath)
        df.to_sql(table_name, con, if_exists='append', index=False)
        con.close()

properties = order_data(dbpath)
print(len(properties))
print(properties[44].location.total_address)

#database cleanup
drop_schema(dbpath)
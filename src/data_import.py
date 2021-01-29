from sqlite3 import connect
from os import (
    listdir,
    path
)
from csv import (
    reader,
    writer
)
from pandas import (
    read_csv,
    DataFrame
)

from schema import (
    setup_schema,
    drop_schema
)
from data import (
    order_data,
    ListingStatus,
    get_current_status
)
from plots import make_plots

dbpath = "./real-estate-data.db"
plot_bin = "../bin"
csv_dir = "../data"
try:
    #imports the data
    setup_schema(dbpath)
    for fname in listdir(csv_dir):
        if fname.endswith(".csv"):
            table_name = path.basename(fname[:-4])
            fpath = f"{csv_dir}/{fname}"
            con = connect(dbpath)
            df = read_csv(fpath)
            df.to_sql(table_name, con, if_exists="append", index=False)
            con.close()

    #organize the data into data structures
    properties = order_data(dbpath)

    #make plots
    make_plots(properties, plot_bin)

    #database cleanup
    drop_schema(dbpath)
except Exception as e:
    drop_schema(dbpath)
    raise e
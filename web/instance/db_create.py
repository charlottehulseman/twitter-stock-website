# Check the PYTHONPATH environment variable before beginning to ensure that the
# top-level directory is included.  If not, append the top-level.  This allows
# the modules within the .../project/ directory to be discovered.
import sys
import os

print('Creating database tables.')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    sys.path.append(os.path.abspath(os.curdir))


# Create the database tables, add some initial data, and commit to the database
from project import db
from project.models import Stock
import pandas as pd
from os import getcwd


path = getcwd() + "/instance/stocks.csv"
stocks_db = pd.read_csv(path)
print(stocks_db)
stocks = []
for index, row in stocks_db.iterrows():
    v = Stock(row["name"], row["summary"], row["logo"], row["website"],
              row["industry"], row["sector"], row["size"])
    stocks.append(v)

# Drop all of the existing database tables
db.drop_all()

# Create the database and the database table
db.create_all()

# insert Stocks
for v in stocks:
    db.session.add(v)

# Commit the changes for the recipes
db.session.commit()

print('...done!')

from threading import Thread
from project.streamer import TwitterStreamer


def start_streamer():
    ts = TwitterStreamer()
    tag_list = ["MSFT", "AAPL", "GOOG", "NVDA",
                "TSLA", "NFLX", "AMZN", "FB", "GM",
                "ABBV", "JPM", "JNJ", "DIS", "PG",
                "MA", "PYPL", "XOM", "VZ"]
    # track only tweets with $ or # next to ticker
    t_list = ["$" + t for t in tag_list]
    t_list.extend(["#" + t for t in tag_list])
    ts.stream_tweets(t_list)
thread = Thread(target=start_streamer)
thread.start()


from .tweepy_streamer import TwitterStreamer
ts = TwitterStreamer("./config.toml")

tag_list = ["APPL", "GOOG", "MSFT"]
ts.stream_tweets(tag_list)
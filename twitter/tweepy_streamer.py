from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
import toml
import pandas as pd
import time
#from pprint import pprint

class Scraper(StreamListener):

    def __init__(self, time_limit=70):
            self.time = time.time()
            self.limit = time_limit
            self.tweet_data = []

    def on_data(self, data):
        #saveFile = open('raw_tweets.json', 'r+', encoding='utf-8')
        while(time.time()- self.time) < self.limit:
                try:
                    self.tweet_data.append(data)
                    return True
                except Exception as e:
                    print('failed ondata', str(e))
                    time.sleep(5)

        saveFile = open('./raw_tweets.json', 'w+', encoding='utf-8')
        saveFile.write(u'[\n')
        saveFile.write(','.join(self.tweet_data))
        saveFile.write(u'\n]')
        saveFile.close()


"""
Learn how to clean up JSON in python 

there is a json module in python but im not sure itll be very useful
e.g. import json

look up things like "what does the tweepy API return?

we can work on this together

('{"created_at":"Tue Apr 13 06:50:38 +0000 '
 '2021","id":1381862374437572608,"id_str":"1381862374437572608","text":"4000\\nhttps:\\/\\/t.co\\/hOaFcEprn9","source":"\\u003ca '
 'href=\\"http:\\/\\/twitter.com\\/download\\/android\\" '
 'rel=\\"nofollow\\"\\u003eTwitter for '
 'Android\\u003c\\/a\\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":2148925184,"id_str":"2148925184","name":"\\u305d\\u3089","screen_name":"etorofcisca","location":null,"url":null,"description":null,"translator_type":"none","protected":false,"verified":false,"followers_count":545,"friends_count":2083,"listed_count":1,"favourites_count":50828,"statuses_count":3077,"created_at":"Tue '
 'Oct 22 12:21:21 +0000 '
 '2013","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"000000","profile_background_image_url":"http:\\/\\/abs.twimg.com\\/images\\/themes\\/theme1\\/bg.png","profile_background_image_url_https":"https:\\/\\/abs.twimg.com\\/images\\/themes\\/theme1\\/bg.png","profile_background_tile":false,"profile_link_color":"FF691F","profile_sidebar_border_color":"000000","profile_sidebar_fill_color":"000000","profile_text_color":"000000","profile_use_background_image":false,"profile_image_url":"http:\\/\\/pbs.twimg.com\\/profile_images\\/1340620746112921600\\/MR9EUqVE_normal.jpg","profile_image_url_https":"https:\\/\\/pbs.twimg.com\\/profile_images\\/1340620746112921600\\/MR9EUqVE_normal.jpg","default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[{"url":"https:\\/\\/t.co\\/hOaFcEprn9","expanded_url":"https:\\/\\/aehstaal4r6q3xdtoa3roy4b7a-adwhj77lcyoafdy-freepressers-com.translate.goog\\/articles\\/4-000-in-europe-died-after-adverse-reactions-to-vaccines","display_url":"\\u2026oafdy-freepressers-com.translate.goog\\/articles\\/4-000\\u2026","indices":[5,28]}],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"low","lang":"und","timestamp_ms":"1618296638484"}\r\n')

"""
def on_error(self, status):
    print(status)


class TwitterStreamer():

    def __init__(self, config):
        """Create a twitter streamer
        """
        self._config = self._load_config(config)
        print("Successfully loaded configuration!!")

    def _load_config(self, config_path):
        config = toml.load(config_path)
        return config

    def write_csv(self):

            data_json = open('./raw_tweets.json', mode='r+').read() #reads in the JSON file into Python as a string
            data_python = json.loads(data_json) #turns the string into a json Python object

            csv_out = open('./tweepy_streamer.csv', mode='w') #opens csv file
            writer = csv.writer(csv_out) #create the csv writer object

            fields = ['created_at', 'text', 'screen_name', 'followers', 'friends', 'rt', 'fav'] #field names
            writer.writerow(fields) #writes field

            for line in data_python:

            #writes a row and gets the fields from the json object
            #screen_name and followers/friends are found on the second level hence two get methods
                writer.writerow([line.get('created_at'),
                                line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
                                line.get('user').get('screen_name'),
                                line.get('user').get('followers_count'),
                                line.get('retweet_count'),
                                line.get('favorite_count')])

            csv_out.close()

    def stream_tweets(self, hash_tag_list):
        scraper = Scraper()
        conf = self._config["scraper"]
        auth = OAuthHandler(conf["con_key"], conf["con_secret"])
        auth.set_access_token(conf["token"], conf["token_secret"])

        stream = Stream(auth, scraper)

        stream.filter(track=hash_tag_list)

#from .tweepy_streamer import TwitterStreamer
ts = TwitterStreamer("./config.toml")

tag_list = ["APPL", "GOOG", "MSFT"]
#ts.stream_tweets(tag_list)
ts.write_csv()

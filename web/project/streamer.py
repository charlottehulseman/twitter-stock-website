from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
import time
from pprint import pprint
from . import db, app
from .models import Tweet

class Scraper(StreamListener):

    def __init__(self, stock_tickers):
        super().__init__(self)
        self.tickers = stock_tickers

    def on_data(self, data):
        all_data = json.loads(data)
        # collect all desired data fields
        if 'extended_tweet' in all_data:
            text          = all_data['extended_tweet']["full_text"]
            created_at    = all_data["created_at"]
            username      = all_data["user"]["screen_name"]
            for stock in self.tickers:
                if stock in text:
                    print("Got Tweet!!", text)
                    tweet = Tweet(stock, created_at, username, text)
                    db.session.add(tweet)
                    db.session.commit()

class TwitterStreamer():

    tickers = ["MSFT", "AAPL", "GOOG", "NVDA",
               "TSLA", "NFLX", "AMZN", "FB", "GM",
               "ABBV", "JPM", "JNJ", "DIS", "PG",
               "MA", "PYPL", "XOM", "VZ"]

    #hash tag list set in create_db
    def __init__(self):
        self.con_key = app.config["CON_KEY"]
        self.con_secret = app.config["CON_SECRET"]
        self.token = app.config["TOKEN"]
        self.token_secret = app.config["TOKEN_SECRET"]


    def stream_tweets(self, hash_tag_list):
        print("Initialized streamer!")
        scraper = Scraper(self.tickers)
        auth = OAuthHandler(self.con_key, self.con_secret)
        auth.set_access_token(self.token, self.token_secret)
        stream = Stream(auth, scraper)
        stream.filter(track=hash_tag_list, languages=["en"])


"""
Twitter Docstring

{'contributors': None,
 'coordinates': None,
 'created_at': 'Sun May 02 20:23:42 +0000 2021',
 'display_text_range': [0, 140],
 'entities': {'hashtags': [],
              'symbols': [{'indices': [74, 79], 'text': 'ACHV'},
                          {'indices': [80, 85], 'text': 'SONN'},
                          {'indices': [86, 89], 'text': 'ZN'},
                          {'indices': [90, 95], 'text': 'COCP'},
                          {'indices': [96, 100], 'text': 'HBP'},
                          {'indices': [101, 106], 'text': 'KODK'},
                          {'indices': [107, 112], 'text': 'AMZN'}],
              'urls': [{'display_url': 'twitter.com/i/web/status/1…',
                        'expanded_url': 'https://twitter.com/i/web/status/1388952359607279617',
                        'indices': [114, 137],
                        'url': 'https://t.co/SdZ3WKHmbN'}],
              'user_mentions': []},
 'extended_tweet': {'display_text_range': [0, 255],
                    'entities': {'hashtags': [],
                                 'media': [{'display_url': 'pic.twitter.com/XaRikVxkKk',
                                            'expanded_url': 'https://twitter.com/Vijayraj11122/status/1388952359607279617/photo/1',
                                            'id': 1388952344218324995,
                                            'id_str': '1388952344218324995',
                                            'indices': [256, 279],
                                            'media_url': 'http://pbs.twimg.com/media/E0aMzE8UUAMgsOk.jpg',
                                            'media_url_https': 'https://pbs.twimg.com/media/E0aMzE8UUAMgsOk.jpg',
                                            'sizes': {'large': {'h': 2048,
                                                                'resize': 'fit',
                                                                'w': 946},
                                                      'medium': {'h': 1200,
                                                                 'resize': 'fit',
                                                                 'w': 554},
                                                      'small': {'h': 680,
                                                                'resize': 'fit',
                                                                'w': 314},
                                                      'thumb': {'h': 150,
                                                                'resize': 'crop',
                                                                'w': 150}},
                                            'type': 'photo',
                                            'url': 'https://t.co/XaRikVxkKk'}],
                                 'symbols': [{'indices': [74, 79],
                                              'text': 'ACHV'},
                                             {'indices': [80, 85],
                                              'text': 'SONN'},
                                             {'indices': [86, 89],
                                              'text': 'ZN'},
                                             {'indices': [90, 95],
                                              'text': 'COCP'},
                                             {'indices': [96, 100],
                                              'text': 'HBP'},
                                             {'indices': [101, 106],
                                              'text': 'KODK'},
                                             {'indices': [107, 112],
                                              'text': 'AMZN'},
                                             {'indices': [113, 118],
                                              'text': 'AAPL'},
                                             {'indices': [119, 123],
                                              'text': 'SPY'},
                                             {'indices': [124, 129],
                                              'text': 'PINS'},
                                             {'indices': [130, 135],
                                              'text': 'NMTR'},
                                             {'indices': [136, 139],
                                              'text': 'FB'},
                                             {'indices': [140, 145],
                                              'text': 'TSLA'},
                                             {'indices': [146, 151],
                                              'text': 'MSFT'},
                                             {'indices': [152, 157],
                                              'text': 'HTGM'},
                                             {'indices': [158, 163],
                                              'text': 'CHGG'},
                                             {'indices': [164, 169],
                                              'text': 'BIOC'},
                                             {'indices': [170, 174],
                                              'text': 'KSI'},
                                             {'indices': [175, 180],
                                              'text': 'BYOC'},
                                             {'indices': [181, 186],
                                              'text': 'XSPA'},
                                             {'indices': [187, 192],
                                              'text': 'IZEA'},
                                             {'indices': [193, 198],
                                              'text': 'NKLA'},
                                             {'indices': [199, 203],
                                              'text': 'ZOM'},
                                             {'indices': [204, 209],
                                              'text': 'VISL'},
                                             {'indices': [210, 214],
                                              'text': 'ADT'},
                                             {'indices': [215, 220],
                                              'text': 'VSTM'},
                                             {'indices': [221, 226],
                                              'text': 'ATVI'},
                                             {'indices': [227, 232],
                                              'text': 'BYND'},
                                             {'indices': [233, 238],
                                              'text': 'TSLA'},
                                             {'indices': [239, 244],
                                              'text': 'MARK'},
                                             {'indices': [245, 250],
                                              'text': 'RIOT'},
                                             {'indices': [251, 255],
                                              'text': 'NOK'}],
                                 'urls': [],
                                 'user_mentions': []},
                    'extended_entities': {'media': [{'display_url': 'pic.twitter.com/XaRikVxkKk',
                                                     'expanded_url': 'https://twitter.com/Vijayraj11122/status/1388952359607279617/photo/1',
                                                     'id': 1388952344218324995,
                                                     'id_str': '1388952344218324995',
                                                     'indices': [256, 279],
                                                     'media_url': 'http://pbs.twimg.com/media/E0aMzE8UUAMgsOk.jpg',
                                                     'media_url_https': 'https://pbs.twimg.com/media/E0aMzE8UUAMgsOk.jpg',
                                                     'sizes': {'large': {'h': 2048,
                                                                         'resize': 'fit',
                                                                         'w': 946},
                                                               'medium': {'h': 1200,
                                                                          'resize': 'fit',
                                                                          'w': 554},
                                                               'small': {'h': 680,
                                                                         'resize': 'fit',
                                                                         'w': 314},
                                                               'thumb': {'h': 150,
                                                                         'resize': 'crop',
                                                                         'w': 150}},
                                                     'type': 'photo',
                                                     'url': 'https://t.co/XaRikVxkKk'}]},
                    'full_text': 'Alerts before spikes and right as big news '
                                 'drops\n'
                                 '\n'
                                 'Free discord chatroom:\n'
                                 '\n'
                                 '$ACHV $SONN $ZN $COCP $HBP $KODK $AMZN $AAPL '
                                 '$SPY $PINS $NMTR $FB $TSLA $MSFT $HTGM $CHGG '
                                 '$BIOC $KSI $BYOC $XSPA $IZEA $NKLA $ZOM '
                                 '$VISL $ADT $VSTM $ATVI $BYND $TSLA $MARK '
                                 '$RIOT $NOK https://t.co/XaRikVxkKk'},
 'favorite_count': 0,
 'favorited': False,
 'filter_level': 'low',
 'geo': None,
 'id': 1388952359607279617,
 'id_str': '1388952359607279617',
 'in_reply_to_screen_name': None,
 'in_reply_to_status_id': None,
 'in_reply_to_status_id_str': None,
 'in_reply_to_user_id': None,
 'in_reply_to_user_id_str': None,
 'is_quote_status': False,
 'lang': 'und',
 'place': None,
 'possibly_sensitive': False,
 'quote_count': 0,
 'reply_count': 0,
 'retweet_count': 0,
 'retweeted': False,
 'source': '<a href="http://twitter.com/download/android" '
           'rel="nofollow">Twitter for Android</a>',
 'text': 'Alerts before spikes and right as big news drops\n'
         '\n'
         'Free discord chatroom:\n'
         '\n'
         '$ACHV $SONN $ZN $COCP $HBP $KODK $AMZN… https://t.co/SdZ3WKHmbN',
 'timestamp_ms': '1619987022674',
 'truncated': True,
 'user': {'contributors_enabled': False,
          'created_at': 'Tue Jan 19 14:58:45 +0000 2021',
          'default_profile': True,
          'default_profile_image': False,
          'description': 'Best discord group over 80k members and even have '
                         'their own app join here https://linktr.ee/rajuray48',
          'favourites_count': 5,
          'follow_request_sent': None,
          'followers_count': 522,
          'following': None,
          'friends_count': 0,
          'geo_enabled': True,
          'id': 1351544588519915520,
          'id_str': '1351544588519915520',
          'is_translator': False,
          'lang': None,
          'listed_count': 10,
          'location': None,
          'name': 'Vijay',
          'notifications': None,
          'profile_background_color': 'F5F8FA',
          'profile_background_image_url': '',
          'profile_background_image_url_https': '',
          'profile_background_tile': False,
          'profile_image_url': 'http://pbs.twimg.com/profile_images/1351545478215733249/tYX1Z8Zq_normal.jpg',
          'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1351545478215733249/tYX1Z8Zq_normal.jpg',
          'profile_link_color': '1DA1F2',
          'profile_sidebar_border_color': 'C0DEED',
          'profile_sidebar_fill_color': 'DDEEF6',
          'profile_text_color': '333333',
          'profile_use_background_image': True,
          'protected': False,
          'screen_name': 'Vijayraj11122',
          'statuses_count': 9374,
          'time_zone': None,
          'translator_type': 'none',
          'url': 'https://linktr.ee/rajuray48',
          'utc_offset': None,
          'verified': False,
          'withheld_in_countries': []}}
"""
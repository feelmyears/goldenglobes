import csv
from dateutil import parser
from ttp import ttp
from fuzzywuzzy import fuzz

class Tweet():
    def __init__(self):
        self.text = None
        self.username = None
        self.user_id = None
        self.timestamp = None
        self.mentions = None
        self.tags = None

class TweetParser():
    def __init__(self):
        self.parser = ttp.Parser()

    def parse_tweet_row(self, row):
        (text, username, user_id, tweet_id, timestr) = row
        result = self.parser.parse(text)
        mentions = result.users
        tags = result.tags
        timestamp = parser.parse(timestr)

        t = Tweet()
        t.text = text
        t.username = username
        t.user_id = user_id
        t.timestamp = timestamp
        t.mentions = mentions
        t.tags = tags
        return t


class TweetDB():
    def __init__(self):
        self.parser = TweetParser()
        self.tweets = []
        self.mentions = {}
        self.tags = {}

    def import_tweets(self, source):
        tweets = []
        with open(source, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) == 5:  # Some rows dont have all info
                    t = self.parser.parse_tweet_row(row)
                    tweets.append(t)

        self.tweets = tweets
        return tweets

    def process_tweets(self):
        for t in self.tweets:
            mentions = t.mentions
            for m in mentions:
                self.add_mention(t, m)

            tags = t.tags
            for tag in tags:
                self.add_tag(t, tag)

    def add_mention(self, tweet, mention):
        if mention in self.mentions:
            self.mentions[mention].append(tweet)
        else:
            self.mentions[mention] = [tweet]

    def add_tag(self, tweet, tag):
        if tag in self.tags:
            self.tags[tag].append(tweet)
        else:
            self.tags[tag] = [tweet]

    def get_tweets_with_mention(self, mention):
        if mention in self.mentions:
            return self.mentions[mention]
        else:
            return None

    def get_tweets_with_tag(self, tag):
        if tag in self.tags:
            return self.tags[tag]
        else:
            return None

    def get_tweets_with_text(self, text, fuzzy=False):
        results = []
        for t in self.tweets:
            if fuzzy:
                pass
            else:
                if text in t.text:
                    results.append(t)

        return results
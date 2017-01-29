from TweetDB import Tweet, TweetDB
from kb import MOTION_PICTURE_AWARDS, TELEVISION_AWARDS
import re
from collections import Counter

USE_FULL_SET = True

class GoldenGlobes():
    def __init__(self, awards, tweets):
        self.awards = awards
        self.tweetDB = tweets

    def find_host(self):
        name_pattern = ur'([A-Z][a-z]+(?: [A-Z][a-z]+)+)'
        p = re.compile(name_pattern)

        host_counts = Counter()
        for t in self.tweetDB.tweets:
            text = t.text
            if 'host' in text or 'Host' in text:
                matches = re.findall(p, text)
                for h in matches:
                    host_counts[h] += 1

        ml_host = host_counts.most_common(1)[0][0]
        return ml_host


# Initializing Tweet Database
tweet_data = 'goldenglobes.tab' if USE_FULL_SET else 'goldenglobes_mod.tab'
tweets = TweetDB()
tweets.import_tweets(tweet_data)
tweets.process_tweets()

# Getting Awards
awards = MOTION_PICTURE_AWARDS + TELEVISION_AWARDS

# Creating GoldenGlobes app

gg = GoldenGlobes(awards, tweets)
print gg.find_host()

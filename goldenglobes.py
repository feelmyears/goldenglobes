from TweetDB import Tweet, TweetDB
from kb import MOTION_PICTURE_AWARDS, TELEVISION_AWARDS

USE_FULL_SET = True

class GoldenGlobes():
    def __init__(self, awards, tweets):
        self.awards = awards
        self.tweets = tweets

# Initializing Tweet Database
tweet_data = 'goldenglobes.tab' if USE_FULL_SET else 'goldenglobes_mod.tab'
tweets = TweetDB()
tweets.import_tweets(tweet_data)
tweets.process_tweets()

# Getting Awards
awards = MOTION_PICTURE_AWARDS + TELEVISION_AWARDS

# Creating GoldenGlobes app
gg = GoldenGlobes(awards, tweets)

# for a in gg.awards:
#     results = gg.tweets.get_tweets_with_text(a)
#     print '{award}: {num_tweets}'.format(award=a, num_tweets=len(results))

gg_mentions = gg.tweets.get_tweets_with_mention('goldenglobes')
for t in gg_mentions:
    print t.text



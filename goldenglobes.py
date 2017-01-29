from TweetDB import Tweet, TweetDB
from kb import MOTION_PICTURE_AWARDS, TELEVISION_AWARDS
import re
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
import nltk

USE_FULL_SET = True

class GoldenGlobes():
    def __init__(self, awards, tweets):
        self.awards = awards
        self.tweetDB = tweets

    def show_awards(self):
        for award in self.awards:
            print awards

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

        print host_counts.most_common()
        ml_host = host_counts.most_common(1)[0][0]
        return ml_host


    def find_awards_fuzzy_wuzzy(self):
        winners=[]
        award_hash={}
        for award in self.awards:
            award_hash[award]={}
        for tweet in self.tweetDB.tweets:
            tweet=TextBlob(str(tweet))
            tweet.correct()
            for award in self.awards:
                if award in tweet:
                    print tweet
                    print tweet.noun_phrases
        return winners




# Initializing Tweet Database
print "db startup"
tweet_data = 'goldenglobes.tab' if USE_FULL_SET else 'goldenglobes_mod.tab'
tweets = TweetDB()
print "import tweets"
tweets.import_tweets(tweet_data)
print "processing tweets"
tweets.process_tweets()

# Getting Awards
awards = MOTION_PICTURE_AWARDS + TELEVISION_AWARDS

# Creating GoldenGlobes app
gg = GoldenGlobes(awards, tweets)
extractor = ConllExtractor()
for t in gg.tweetDB.tweets:
    blob = TextBlob(t.text, np_extractor=extractor)
    print blob.noun_phrases

# print "finding host"
# print gg.find_host()
# for winner in gg.find_awards_fuzzy_wuzzy():
#     print winner
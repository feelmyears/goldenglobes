import utils
from TweetDB import Tweet, TweetDB
from kb import *
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords as nltkstopwords

USE_FULL_SET = True
USE_PICKLE = True

class GoldenGlobes():
    def __init__(self, awards, tweetDB, classifier):
        self.awards = awards
        self.tweetDB = tweetDB
        self.classifier = classifier

    def show_awards(self):
        for award in self.awards:
            print award

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

    def find_awards(self):
        pass

class AwardClassifier():
    def __init__(self, awards, stopwords, unigram_weight=1, bigram_weight=5):
        self.awards = awards
        self.stopwords = stopwords
        unigrams, bigrams = self.award_bigrams = self.gramify_awards()
        self.award_unigrams = unigrams
        self.award_bigrams = bigrams
        self.unigram_weight = unigram_weight
        self.bigram_weight = bigram_weight

    def gramify_awards(self):
        unigrams = {}
        bigrams = {}
        for a in self.awards:
            award_unigrams = self.tokenize(a)
            unigrams[a] = award_unigrams
            bigrams[a] = nltk.bigrams(award_unigrams)

        return unigrams, bigrams

    def tokenize(self, text):
        raw_tokens = nltk.word_tokenize(text)
        filtered_tokens = [tok.lower() for tok in raw_tokens if tok.lower() not in self.stopwords]
        return filtered_tokens

    def score_tweet(self, award, tweet):
        tweet_unigrams = self.tokenize(tweet)
        tweet_bigrams = nltk.bigrams(tweet_unigrams)

        common_unigrams = [u for u in tweet_unigrams if u in self.award_unigrams[award]]
        common_bigrams = [b for b in tweet_bigrams if b in self.award_bigrams[award]]

        score = self.unigram_weight*len(common_unigrams) + self.bigram_weight*len(common_bigrams)
        return score

    def rank_tweet(self, tweet):
        scores = Counter()
        for a in self.awards:
            scores[a] = self.score_tweet(a, tweet)

        return scores.most_common()

    def classify_tweet(self, tweet):
        return self.rank_tweet(tweet)[0][0]


# Initializing Tweet Database
tweetDB = None
if USE_PICKLE:
    tweet_data = 'goldenglobesTweetDB'
    tweetDB = utils.load(tweet_data)
else:
    tweet_data = 'goldenglobes.tab' if USE_FULL_SET else 'goldenglobes_mod.tab'
    tweetDB = TweetDB()
    tweetDB.import_tweets(tweet_data)
    tweetDB.process_tweets()
    utils.save(tweetDB, 'goldenglobesTweetDB')


# Getting Awards
awards = MOTION_PICTURE_AWARDS + TELEVISION_AWARDS


# Initializing Award Clasifier
stopwords = nltkstopwords.words('english') + STOPWORDS
unigram_weight = 1
bigram_weight = 5
classifier = AwardClassifier(awards, stopwords, unigram_weight, bigram_weight)

# Creating GoldenGlobes app
gg = GoldenGlobes(awards, tweetDB, classifier)
for t in gg.tweetDB.tweets:
    print gg.classifier.classify_tweet(t.text), ':\t', t.text

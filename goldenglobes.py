import logging
import time
import utils
from TweetDB import Tweet, TweetDB
from kb import *
import re
from collections import Counter
from textblob import TextBlob
from nltk.corpus import stopwords as nltkstopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from joblib import Parallel, delayed
import multiprocessing


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

    def find_awards_fuzzy_wuzzy(self):
        winners = []
        award_hash = {}
        for award in self.awards:
            award_hash[award] = {}
        for tweet in self.tweetDB.tweets:
            tweet = TextBlob(str(tweet))
            tweet.correct()
            for award in self.awards:
                if award in tweet:
                    print tweet
                    print tweet.noun_phrases
        return winners


class AwardClassifier():
    def __init__(self, awards, stopwords, pred_thresh=1):
        self.awards = awards
        self.stopwords = stopwords
        self.pred_thresh = pred_thresh
        self.feature_vector = self.gen_feature_vector(stopwords)
        self.award_feature_masks = self.gen_award_masks(self.feature_vector)

    def gen_feature_vector(self, stopwords):
        vect = TfidfVectorizer(analyzer='word', stop_words=stopwords, ngram_range=(1, 3))
        vect.fit_transform(self.awards)
        return vect

    def gen_award_masks(self, feature_vector):
        features = feature_vector.get_feature_names()
        num_features = len(features)
        masks = {}
        for a in self.awards:
            m = np.zeros(num_features)
            for i in range(num_features):
                feat = features[i]
                if re.search(feat, a, re.IGNORECASE):
                    m[i] = 1
            masks[a] = m
        return masks

    def classify_tweet(self, tweet_text):
        freqs = self.feature_vector.transform([tweet_text]).toarray()[0]
        features = self.feature_vector.get_feature_names()
        counts = Counter()
        for a in self.awards:
            mask = self.award_feature_masks[a]
            masked_freqs = np.multiply(freqs, mask)
            counts[a] = np.sum(masked_freqs)
        predicted_award = counts.most_common(1)[0]
        if predicted_award[1] > self.pred_thresh:
            return predicted_award[0]
        else:
            return None


def main():
    logging.basicConfig(filename='performance.log', level=logging.DEBUG)
    USE_FULL_SET = True
    USE_PICKLE = True
    start_time = time.time()
    logging.info(" startup at time:" + str(start_time))
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


    load_time = time.time()
    logging.info("tweets loaded after :" + str(load_time - start_time))
    # Getting Awards
    awards = MOTION_PICTURE_AWARDS + TELEVISION_AWARDS

    # Initializing Award Clasifier
    stopwords = nltkstopwords.words('english')
    classifier = AwardClassifier(awards, stopwords)
    classifier_time = time.time()
    logging.info("classifier created after :" + str(classifier_time - load_time))

    # Creating GoldenGlobes app
    gg = GoldenGlobes(awards, tweetDB, classifier)

    # parallelize this for loop
    awd_counts = Counter()
    total = 0
    skipped = 0
    parallel = True
    if (parallel):

        num_cores = multiprocessing.cpu_count()
        pred_awards = Parallel(n_jobs=num_cores)(delayed(gg.classifier.classify_tweet)(t.txt) for t in gg.tweetDB.tweets)
        for pred_award in pred_awards:
            if pred_award:
                total += 1
                awd_counts[pred_award] += 1
            else:
                skipped += 1

    else:
        for t in gg.tweetDB.tweets:
            pred_award = gg.classifier.classify_tweet(t.text)
            if pred_award:
                total += 1
                awd_counts[pred_award] += 1
            else:
                skipped += 1

    print total
    print awd_counts
    print awd_counts.most_common()
    end_time=time.time()
    logging.info("classification completed after :" + str(end_time - classifier_time))

if __name__ == "__main__":
    main()

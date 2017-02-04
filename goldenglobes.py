import re
from collections import Counter
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

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

    def find_presenters(self):
        presenter_pattern = ur'(@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))? +(?:to +)?present'
        p = re.compile(presenter_pattern)
        presenter_counts = Counter()
        for t in self.tweetDB.tweets:
            text = t.text
            if 'present' in text or 'presents' in text or 'presented' in text:
                matches = re.findall(p, text)
                if len(matches) > 0:
                    for m in matches[0]:
                        if len(m)>1:
                            presenter_counts[m] += 1
        return presenter_counts.most_common(5)


    def find_awards(self):
        winners=[]
        award_hash={}
        for award in self.awards:
            award_hash[award]=Counter()
        for tweet in self.tweetDB.tweets:
            classification = self.classifier.classify_tweet(tweet.text)
            if classification!=None:
                tweet=TextBlob(tweet.text)
                for noun in tweet.noun_phrases:
                    if noun not in ['goldenglobes']:
                        award_hash[classification][noun] += 1
        for award in self.awards:
            winners.append(award_hash[award].most_common())
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
            return str(predicted_award[0])
        else:
            return None

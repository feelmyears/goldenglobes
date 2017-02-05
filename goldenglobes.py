import re
from collections import Counter
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from Levenshtein import distance
from scorer import AwardCeremonyApp
class GoldenGlobes(AwardCeremonyApp):
    def __init__(self, awards, tweetDB, classifier):
        self.awards = awards
        self.tweetDB = tweetDB
        self.classifier = classifier

    def get_ceremony(self):
        return 'Golden Globes'

    def get_host(self):
        return self.find_host()

    def get_awards(self):
        return self.awards

    def get_winners(self):
        pass

    def get_presenters(self):
        presenters = {}
        for a in self.awards:
            presenters[a] = None
        return presenters

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

        #print host_counts.most_common()
        grouped_hosts = group_counts(host_counts.most_common())
        #print grouped_hosts
        ml_host = host_counts.most_common(1)[0][0]
        return ml_host

    def find_presenters(self):
        presenter_pattern = ur'(@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))? +(?:to +)?present'
        p = re.compile(presenter_pattern)
        presenter_counts = Counter()
        for t in self.tweetDB.tweets:
            text = t.text
            if 'present' in text or 'Present' in text:
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
            winners.append((award,(award_hash[award].most_common(10))))
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

def group_counts(counts, max_dist=10):
    ungrouped = counts
    grouped = []
    while len(ungrouped):
        pattern, ct = ungrouped[0]
        new_group_indices = [0]
        for i in range(1, len(ungrouped)):
            try:
                cmp_pattern, cmp_ct = ungrouped[i]
            except ValueError:
                pass
            if should_group(pattern, cmp_pattern, max_dist):
                ct += cmp_ct
                new_group_indices.append(i)
        grouped.append((pattern, ct))
        ungrouped = [ungrouped[i] for i in range(len(ungrouped)) if i not in new_group_indices]

    grouped_sorted = sorted(grouped, key=lambda x: x[1], reverse=True)
    return grouped_sorted


def should_group(pattern, cmp_pattern, max_dist):
    # return pattern in cmp_pattern or cmp_pattern in pattern or distance(pattern, cmp_pattern) <= max_dist
    return distance(pattern, cmp_pattern) <= max_dist

from AwardCeremony import AwardCeremonyApp
import re
from collections import Counter
from textblob import TextBlob
from Levenshtein import distance
from imdb import IMDb

class GoldenGlobes(AwardCeremonyApp):
    def __init__(self, awards, tweetDB, classifier):
        self.awards = awards
        self.tweetDB = tweetDB
        self.classifier = classifier
        self.imdb = IMDb()

        self.present_counter = 0

        self.ignored=[]
        for award in self.awards:
            for word in award.split():
               self.ignored.append(word.lower())
        self.ignored.append("goldenglobes")
        self.ignored.append("movie")
        self.ignored.append("rt")
        self.ignored.append("performance")
        self.ignored.append("congratulations")
        self.ignored.append("tv series")


    def get_name(self):
        return 'Golden Globes'

    def get_host(self):
        return self.find_host()

    def get_awards(self):
        return self.awards

    def get_winners(self):
        winners = {}
        for a in self.awards:
            winners[a] = None
        return winners

    def get_presenters(self):
        presenters = {}
        for a in self.awards:
            presenters[a] = None
        return presenters

    def get_bonuses(self):
        bonuses = {}
        # Example: bonuses['Best Dressed'] = 'Emma Stone'
        pass

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

        grouped_hosts = group_counts(host_counts.most_common())
        ml_host = grouped_hosts[0][0]
        return ml_host

    def find_presenters(self):
        presenters = []
        presenter_pattern = ur'(@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))? +(?:to +)?present'
        present_detection = r'[Pp]resent'
        p = re.compile(presenter_pattern)
        presenter_counts = {}
        unclassified_presenters = Counter()
        for award in self.awards:
            presenter_counts[award] = Counter()
        for t in self.tweetDB.tweets:
            text = t.text
            if re.search(present_detection, text):
                matches = re.findall(p, text)
                if len(matches) > 0:
                    classification = self.classifier.classify_tweet(text)
                    self.present_counter += 1
                    for m in matches[0]:
                        if len(m)>1:
                            #if m.lower() not in self.stopwords:
                            if classification != None:
                                presenter_counts[classification][m] += 1
                            else:
                                unclassified_presenters[m] += 1
        for award in self.awards:
            most_common = presenter_counts[award].most_common()
            print most_common
            new_most_common = Counter()
            for key, value in most_common:
                new_most_common[key] = value + unclassified_presenters[key]
            presenters.append(new_most_common.most_common(5))
        print unclassified_presenters
        print self.present_counter
        return presenters
        

    # New Version
    def find_winners(self):
        winners = {}
        award_hash = {}
        for award in self.awards:
            award_hash[award] = Counter()
        for tweet in self.tweetDB.tweets:
            classification = self.classifier.classify_tweet(tweet.text)
            if classification != None:
                tweet = TextBlob(tweet.text)
                for noun in tweet.noun_phrases:
                    for ignoredWord in self.ignored:
                        if noun.lower() not in ignoredWord and ignoredWord not in noun.lower():
                            award_hash[classification][noun] += 1
        for award in self.awards:
            counts = award_hash[award].most_common(100)
            grouped = group_counts(counts)
            winners[award] = grouped[0:3]
        return winners

    def get_true_name(self, messy_name):
        results = self.imdb.search_person(messy_name)
        if results:
            return results[0]['name']
        else:
            return None

    def get_true_title(self, messy_title):
        results = self.imdb.search_movie(messy_title)
        if results:
            return results[0]['title']
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
                if should_group(pattern, cmp_pattern, max_dist):
                    ct += cmp_ct
                    new_group_indices.append(i)
            except ValueError:
                pass
        grouped.append((pattern, ct))
        ungrouped = [ungrouped[i] for i in range(len(ungrouped)) if i not in new_group_indices]

    grouped_sorted = sorted(grouped, key=lambda x: x[1], reverse=True)
    return grouped_sorted


def should_group(pattern, cmp_pattern, max_dist):
    # return pattern in cmp_pattern or cmp_pattern in pattern or distance(pattern, cmp_pattern) <= max_dist
    return distance(pattern, cmp_pattern) <= max_dist

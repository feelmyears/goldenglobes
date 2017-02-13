from AwardCeremony import AwardCeremonyApp, AwardCeremonyKB
import re
from collections import Counter
from textblob import TextBlob
from Levenshtein import distance
from imdb import IMDb
from nltk import word_tokenize

class GoldenGlobesApp(AwardCeremonyApp):
    def __init__(self, tweetDB, kb, classifier):
        self.kb = kb
        self.tweetDB = tweetDB
        self.classifier = classifier
        self.imdb = IMDb()

    def get_ceremony(self):
        return 'Golden Globes'

    def get_host(self):
        return self.find_host()

    def get_awards(self):
        return self.kb.get_awards()

    def get_winners(self):
        winners = {}
        predicted_winners = self.find_winners()
        for award, recipient_type in self.kb.get_awards_and_recipients():
            predicted = predicted_winners[award]
            if recipient_type is AwardCeremonyKB.PERSON:
                winners[award] = self.get_true_name(predicted)
            elif recipient_type is AwardCeremonyKB.PRODUCTION:
                winners[award] = self.get_true_title(predicted)
            else:
                winners[award] = predicted
        return winners

    def get_presenters(self):
        presenters = {}
        predicted_presenters = self.find_presenters()
        for award in self.kb.get_awards():
            predicted = predicted_presenters[award]
            if predicted is not None:
                presenters[award] = [self.get_true_name(name) for name in predicted]
            else:
                presenters[award] = ["Unable to determine a presenter"]
        return presenters

    def get_bonuses(self):
        bonuses = {}
        stopwords = self.kb.get_stopwords()
        popular_mention = None
        mention_popularity = 0
        for m, tweets in self.tweetDB.mentions.items():
            if m.lower() in stopwords:
                continue
            test_popularity = len(tweets)
            if test_popularity > mention_popularity:
                mention_popularity = test_popularity
                popular_mention = m
        bonuses['Most Popular Twitter @mention'] = popular_mention

        popular_tag = None
        tag_popularity = 0
        for t, tweets in self.tweetDB.mentions.items():
            if t.lower() in stopwords:
                continue
            test_popularity = len(tweets)
            if test_popularity > tag_popularity:
                tag_popularity = test_popularity
                popular_tag = t
        bonuses['Most Popular Twitter #tag'] = popular_tag

        stopwords.append('best')
        stopwords.append('dressed')
        stopwords.append('best dressed')
        stopwords.append('see')

        best_dressed_counts = Counter()
        best_dressed_detection = r'[Bb]est[- ][Dd]ressed'
        best_dressed_pattern = ur'(@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))? +'
        p = re.compile(best_dressed_pattern)
        for t in self.tweetDB.tweets:
            text = t.text
            if re.search(best_dressed_detection, text):
                matches = re.findall(p, text)
                if len(matches) > 0:
                    for m in matches:
                        if m[0].lower() in stopwords:
                            continue
                        best_dressed_counts[m[0]] += 1
        bonuses['Best Dressed'] = best_dressed_counts.most_common(1)[0][0]

        # Example: bonuses['Best Dressed'] = 'Emma Stone'
        return bonuses

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

    def find_winners(self):
        award_hash = {}
        for award in self.get_awards():
            award_hash[award] = Counter()

        for tweet in self.tweetDB.tweets:
            tweet_text = tweet.text
            classification = self.classifier.classify_tweet(tweet_text)
            if classification != None:
                tweet_blob = TextBlob(tweet_text)
                for noun in tweet_blob.noun_phrases:
                    award_hash[classification][noun] += 1

        stopwords = {
            'best',
            '-',
            'goldenglobes',
            'movie',
            'rt',
            'performance',
            'congratulations',
            'tv series',
            'tv',
            'series'
        }
        for a in self.get_awards():
            tokens = word_tokenize(a)
            lower_tokens = [tok.lower() for tok in tokens]
            stopwords |= set(lower_tokens)

        filtered_winners = {}
        for award in self.get_awards():
            counts = award_hash[award].most_common(10)
            filtered_winners[award] = None
            # print award
            # print counts
            for noun, ct in counts:
                if not re.search(noun, award, re.IGNORECASE) and noun not in stopwords:
                    filtered_winners[award] = noun
                    break

        return filtered_winners

    def find_presenters(self):
        presenter_pattern1 = ur'(@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))? +(?:to +)?present'
        presenter_pattern2 = ur'[Pp]resenter[s]? (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))?'
        p1 = re.compile(presenter_pattern1)
        p2 = re.compile(presenter_pattern2)
        patterns = [p1, p2]

        presenter_counts = {}
        for award in self.kb.get_awards():
            presenter_counts[award] = Counter()

        for t in self.tweetDB.tweets:
            text = t.text
            for pat in patterns:
                matches = re.findall(pat, text)
                if len(matches) > 0:
                    classification = self.classifier.classify_tweet(text)
                    for m in matches[0]:
                        if len(m) > 1:
                            if classification != None:
                                presenter_counts[classification][m] += 1

        filtered_presenters = {}
        for award in self.kb.get_awards():
            most_common = presenter_counts[award].most_common(100)
            most_common_combined = group_counts(most_common)
            top_3 = most_common_combined[:min(3, len(most_common_combined))]
            presenters = [x[0] for x in top_3]

            # print award, most_common_combined
            filtered_presenters[award] = presenters if len(presenters) else None

        return filtered_presenters

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
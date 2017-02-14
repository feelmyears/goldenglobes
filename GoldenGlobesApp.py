from AwardCeremony import AwardCeremonyApp, AwardCeremonyKB
import re
from collections import Counter
from textblob import TextBlob
from Levenshtein import distance
from imdb import IMDb
from nltk import word_tokenize
from multiprocessing import Pool
import time

def c_t(input):
    classifier, tweet = input
    tweet_text = tweet.text
    classification = classifier.classify_tweet(tweet_text)
    noun_phrases = None
    if classification is not None:
        noun_phrases = TextBlob(tweet_text).noun_phrases

    return (tweet, classification, noun_phrases)

class GoldenGlobesApp(AwardCeremonyApp):
    def __init__(self, tweetDB, kb, classifier):
        self.kb = kb
        self.tweetDB = tweetDB
        self.classifier = classifier
        self.imdb = IMDb()

        self.network_call_time = 0

        # Tuple of Tweet Classifications in the form of (tweet, classification (None or award),
        # and noun_phrases (None if classification is None)
        self.tweet_classifications = []

    def classify_tweets(self):
        pool = Pool()
        tweets = self.tweetDB.tweets
        input = zip([self.classifier]*len(tweets), tweets)
        result = pool.map(c_t, input)
        self.tweet_classifications = result

    def get_ceremony(self):
        return 'Golden Globes'

    def get_host(self):
        return self.find_host()

    def get_awards(self):
        return self.kb.get_awards()

    def get_network_call_time(self):
        return self.network_call_time

    def get_nominees(self):
        nominees = {}
        counter = 0
        unclassified_nominees = Counter()
        stopwords = self.kb.get_stopwords()
        stopwords.append('nominee')
        stopwords.append('nominees')
        stopwords.append('nominated')
        nom_pattern_beg = r'[Nn]ominees?,? (?P<name>[@#]\w+|[A-Z][a-z-]+ (?:(?:[a-z]+ ){0,2}[A-Z][a-z-]+ )*)'
        nom_pattern_end = r'(?P<name>[@#]\w+|[A-Z][a-z-]+ (?:(?:[a-z]+ ){0,2}[A-Z][a-z-]+ )*) (?:lose|should|doesn|win)'
        p_beg = re.compile(nom_pattern_beg)
        p_end = re.compile(nom_pattern_end)
        gen_pattern = r'[Nn]omin(?:ee|ate)'
        gen_p = re.compile(gen_pattern)
        for award in self.kb.get_awards():
            nominees[award] = Counter()
        for t in self.tweetDB.tweets:
            text = t.text
            #lower = text.lower()
            match_beg = re.search(p_beg, text)
            match_end = re.search(p_end, text)
            general_match = re.search(gen_p, text)
            match = match_beg
            if not match:
                match = match_end
            closest_noun = None
            if match:
                counter += 1
                closest_noun = match.group('name')
                tokens = closest_noun.lower().split(' ')
                for token in tokens:
                    if token in stopwords:
                        continue

            elif general_match:
                name_pattern = r'(?:[@#]\w+|[A-Z][a-z-]+ (?:(?:[a-z]{1,3} ){0,2}[A-Z][a-z-]+ )*)'
                nom_end = general_match.end()
                counter += 1
                np = re.findall(name_pattern, text)
                remove_nouns = []
                for noun in np:
                    tokens = noun.lower().split(' ')
                    for token in tokens:
                        if token in stopwords:
                            remove_nouns.append(noun)
                            break

                for noun in remove_nouns:
                    np.remove(noun)
                if np == []:
                    continue
                closest_noun = None
                closest_distance = 10000000
                for noun in np:
                    noun_regex = re.compile(noun)
                    noun_match = re.search(noun_regex, text)
                    if not noun_match:
                        print "something is wrong here"
                    else:
                        dist = abs(noun_match.start() - nom_end)
                        if text[noun_match.start()-1] == '.' or text[noun_match.start()-2] == '.':
                            continue
                        if dist < closest_distance:
                            closest_distance = dist
                            closest_noun = noun
            else:
                continue

            if closest_noun != None:
                classification = self.classifier.classify_tweet(text)
                if classification:
                    nominees[classification][closest_noun] += 1
                else:
                    unclassified_nominees[closest_noun] += 1

        #print len(unclassified_nominees)
        for key, value in nominees.iteritems():
            group_input = value.most_common()
            group_input.sort()
            group_input.reverse()
            nominees[key] = dict(group_counts(group_input, 10))
            nominees[key] = Counter(nominees[key])
        next_input = unclassified_nominees.most_common()
        next_input.sort()
        next_input.reverse()
        unclassified_nominees = dict(group_counts(next_input, 10))
        #print len(unclassified_nominees)

        delete_keys = []
        for key, value in unclassified_nominees.iteritems():
            for key2, value2 in nominees.iteritems():
                if key in nominees[key2]:
                    nominees[key2][key] += value
                    if key not in delete_keys:
                        delete_keys.append(key)
        for key in delete_keys:
            if key in unclassified_nominees:
                del unclassified_nominees[key]
        #print len(unclassified_nominees)

        #print counter
        #print unclassified_nominees
        #print nominees
        nominee_dict = {}
        for key, value in nominees.iteritems():
            nominee_dict[key] = []
            tuples = value.most_common(6)
            for tup in tuples:
                if len(tup[0]) > 3:
                    nominee_dict[key].append(tup[0])
        #print nominee_dict
        return nominee_dict
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

    def get_winners_and_presenters(self):
        predicted_winners, predicted_presenters = self.find_winners_and_presenters()
        presenters = {}
        winners = {}

        for award, recipient_type in self.kb.get_awards_and_recipients():
            award_winner = predicted_winners[award]
            if recipient_type is AwardCeremonyKB.PERSON:
                true_name = self.get_true_name(award_winner)
                winners[award] = true_name if true_name is not None else award_winner
            elif recipient_type is AwardCeremonyKB.PRODUCTION:
                true_title = self.get_true_title(award_winner)
                winners[award] = true_title if true_title is not None else award_winner
            else:
                winners[award] = award_winner

            award_presenters = predicted_presenters[award]
            unable_message = ["Unable to determine a presenter"]
            if award_presenters is not None:
                true_names = [self.get_true_name(name) for name in award_presenters]
                true_names_filtered = [t for t in true_names if t is not None and len(t) > 1]
                presenters[award] = true_names_filtered if len(true_names_filtered) else unable_message
            else:
                presenters[award] = unable_message


        return winners, presenters

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

        for tweet, classification in self.tweet_classifications:
            text = tweet.text
            if classification != None:
                tweet_blob = TextBlob(text)
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
        presenter_pattern3 = ur'([A-Z][a-z]+(?: [A-Z][a-z]+)+)'
        p1 = re.compile(presenter_pattern1)
        p2 = re.compile(presenter_pattern2)
        p3 = re.compile(presenter_pattern3)
        patterns = [p1, p2, p3]

        presenter_counts = {}
        for award in self.kb.get_awards():
            presenter_counts[award] = Counter()

        for tweet, classification in self.tweet_classifications:
            text = tweet.text
            for pat in patterns:
                matches = re.findall(pat, text)
                if len(matches) > 0:
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

    def find_winners_and_presenters(self):
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

        presenter_pattern1 = ur'([A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and ([A-Z][a-z]+(?: ?[A-Z][a-z]+)*))?\s?\w+\s?[Pp]resent'
        presenter_pattern2 = ur'[Pp]resenter[s]? ([A-Z][a-z]+(?: ?[A-Z][a-z]+)*)(?: and (@?[A-Z][a-z]+(?: ?[A-Z][a-z]+)*))?'

        p1 = re.compile(presenter_pattern1)
        p2 = re.compile(presenter_pattern2)
        patterns = [p1, p2]

        presenter_counts = {}
        winner_counts = {}
        for award in self.get_awards():
            presenter_counts[award] = Counter()
            winner_counts[award] = Counter()

        for tweet, classification, noun_phrases in self.tweet_classifications:
            text = tweet.text
            if classification != None:
                for noun in noun_phrases:
                    winner_counts[classification][noun] += 1

                for pat in patterns:
                    matches = re.findall(pat, text)
                    if len(matches) > 0:
                        for m in matches[0]:
                            if len(m) > 1:
                                presenter_counts[classification][m] += 1

        filtered_presenters = {}
        filtered_winners = {}
        for award in self.get_awards():
            counts = winner_counts[award].most_common(10)
            filtered_winners[award] = None
            for noun, ct in counts:
                if not re.search(noun, award, re.IGNORECASE) and noun not in stopwords:
                    filtered_winners[award] = noun
                    break

            most_common = presenter_counts[award].most_common()
            most_common_combined = group_counts(most_common)
            # most_common_combined = most_common
            top_3 = most_common_combined[:min(3, len(most_common_combined))]
            presenters = [x[0] for x in top_3]

            # print award, most_common_combined
            possible_presenters = [p for p in presenters if len(p) > 3]
            filtered_presenters[award] = possible_presenters if len(presenters) else None

        return filtered_winners, filtered_presenters

    def get_true_name(self, messy_name):
        start_time = time.time()
        results = self.imdb.search_person(messy_name)
        end_time = time.time()
        tot_time = end_time - start_time
        self.network_call_time += tot_time
        if results:
            return results[0]['name']
        else:
            return messy_name

    def get_true_title(self, messy_title):
        tv_producers = ['netflix', 'Netflix', 'hulu', 'Hulu']
        for tv in tv_producers:
            messy_title = messy_title.replace(tv, '')

        start_time = time.time()
        results = self.imdb.search_movie(messy_title)
        end_time = time.time()
        tot_time = end_time - start_time
        self.network_call_time += tot_time
        if results:
            return results[0]['title']
        else:
            return messy_title

def group_counts(counts, max_dist=5):
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
    return distance(pattern, cmp_pattern) <= max_dist


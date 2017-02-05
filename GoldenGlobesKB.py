from AwardCeremony import AwardCeremonyKB
from nltk.corpus import stopwords as nltkstopwords
from nltk import word_tokenize

class GoldenGlobesKB(AwardCeremonyKB):
    def get_awards_and_recipients(self):
        awards_and_recipients = [
            ('Best Motion Picture - Drama', AwardCeremonyKB.PRODUCTION),
            ('Best Motion Picture - Musical or Comedy', AwardCeremonyKB.PRODUCTION),
            ('Best Director', AwardCeremonyKB.PERSON),
            ('Best Actor - Motion Picture Drama', AwardCeremonyKB.PERSON),
            ('Best Actor - Motion Picture Musical or Comedy', AwardCeremonyKB.PERSON),
            ('Best Actress - Motion Picture Drama', AwardCeremonyKB.PERSON),
            ('Best Actress - Motion Picture Musical or Comedy', AwardCeremonyKB.PERSON),
            ('Best Supporting Actor - Motion Picture', AwardCeremonyKB.PERSON),
            ('Best Supporting Actress - Motion Picture', AwardCeremonyKB.PERSON),
            ('Best Screenplay', AwardCeremonyKB.PRODUCTION),
            ('Best Original Score', AwardCeremonyKB.PRODUCTION),
            ('Best Original Song', AwardCeremonyKB.PRODUCTION),
            ('Best Foreign Language Film', AwardCeremonyKB.PRODUCTION),
            ('Best Animated Feature Film', AwardCeremonyKB.PRODUCTION),
            ('Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures', AwardCeremonyKB.PERSON),
            ('Best Drama Series', AwardCeremonyKB.PRODUCTION),
            ('Best Comedy Series', AwardCeremonyKB.PRODUCTION),
            ('Best Actor in a Television Drama Series', AwardCeremonyKB.PERSON),
            ('Best Actor in a Television Comedy Series', AwardCeremonyKB.PERSON),
            ('Best Actress in a Television Drama Series', AwardCeremonyKB.PERSON),
            ('Best Actress in a Television Comedy Series', AwardCeremonyKB.PERSON),
            ('Best Limited Series or Motion Picture made for Television', AwardCeremonyKB.PRODUCTION),
            ('Best Actor in a Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON),
            ('Best Actress in a Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON),
            ('Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON),
            ('Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON)
        ]
        return awards_and_recipients

    def get_awards(self):
        return [a[0] for a in self.get_awards_and_recipients()]

    def get_stopwords(self):
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

        stopwords |= set(nltkstopwords.words('english'))
        return list(stopwords)
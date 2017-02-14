from AwardCeremony import AwardCeremonyKB
from nltk.corpus import stopwords as nltkstopwords
from nltk import word_tokenize

class GoldenGlobesKB(AwardCeremonyKB):
    def get_awards_and_recipients(self):
        awards_and_recipients = [
            ('Best Motion Picture - Drama', AwardCeremonyKB.PRODUCTION),
            ('Best Motion Picture - Musical or Comedy', AwardCeremonyKB.PRODUCTION),
            ('Best Director - Motion Picture', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actor - Motion Picture Drama', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actor - Motion Picture Musical or Comedy', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actress - Motion Picture Drama', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actress - Motion Picture Musical or Comedy', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actor in a Supporting Role - Motion Picture', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actress in a Supporting Role - Motion Picture', AwardCeremonyKB.PERSON),
            ('Best Screenplay - Motion Picture', AwardCeremonyKB.PRODUCTION),
            ('Best Original Score - Motion Picture', AwardCeremonyKB.PRODUCTION),
            ('Best Original Song - Motion Picture', AwardCeremonyKB.PRODUCTION),
            ('Best Foreign Language Film', AwardCeremonyKB.PRODUCTION),
            ('Best Animated Feature Film', AwardCeremonyKB.PRODUCTION),
            ('Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures', AwardCeremonyKB.PERSON),
            ('Best Television Series - Drama', AwardCeremonyKB.PRODUCTION),
            ('Best Television Series - Musical or Comedy', AwardCeremonyKB.PRODUCTION),
            ('Best Performance by an Actor in a Television Series - Drama', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actor in a Television Series - Musical or Comedy', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actress in a Television Series - Drama', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actress in a Television Series - Musical or Comedy', AwardCeremonyKB.PERSON),
            ('Best Television Limited Series or Motion Picture made for Television', AwardCeremonyKB.PRODUCTION),
            ('Best Performance by an Actor in a Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON),
            ('Best Performance by an Actress in a Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON),
            ('Best Performance by a Supporting Actor in a Series, Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON),
            ('Best Performance by a Supporting Actress in a Series, Limited Series or Motion Picture made for Television', AwardCeremonyKB.PERSON)
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
MOTION_PICTURE_AWARDS = [
    'Best Motion Picture - Drama',
    'Best Motion Picture - Musical or Comedy',
    'Best Director',
    'Best Actor - Motion Picture Drama',
    'Best Actor - Motion Picture Musical or Comedy',
    'Best Actress - Motion Picture Drama',
    'Best Actress - Motion Picture Musical or Comedy',
    'Best Supporting Actor - Motion Picture',
    'Best Supporting Actress - Motion Picture',
    'Best Screenplay',
    'Best Original Score',
    'Best Original Song',
    'Best Foreign Language Film',
    'Best Animated Feature Film',
    'Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures'
]

TELEVISION_AWARDS = [
    'Best Drama Series',
    'Best Comedy Series',
    'Best Actor in a Television Drama Series',
    'Best Actor in a Television Comedy Series',
    'Best Actress in a Television Drama Series',
    'Best Actress in a Television Comedy Series',
    'Best Limited Series or Motion Picture made for Television',
    'Best Actor in a Limited Series or Motion Picture made for Television',
    'Best Actress in a Limited Series or Motion Picture made for Television',
    'Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television',
    'Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television'
]


class AwardCeremonyKB():
    PERSON = 'PERSON'
    PRODUCTION = 'PRODUCTION'
    def get_awards(self):
        pass

    def get_stopwords(self):
        pass

class GoldenGlobesKB(AwardCeremonyKB):
    def get_awards(self):
        awards = [
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
        return awards

    def get_stopwords(self):
        stopwords = [
            'best',
            '-'
        ]
        return stopwords

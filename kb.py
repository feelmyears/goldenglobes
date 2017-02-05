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

STOPWORDS = [
    'best',
    '-'
]

PERSON = 'PERSON'
PRODUCTION = 'PRODUCTION'
class KB():
    AWARDS = [
        ('Best Motion Picture - Drama', PRODUCTION),
        ('Best Motion Picture - Musical or Comedy', PRODUCTION),
        ('Best Director', PERSON),
        ('Best Actor - Motion Picture Drama', PERSON),
        ('Best Actor - Motion Picture Musical or Comedy', PERSON),
        ('Best Actress - Motion Picture Drama', PERSON),
        ('Best Actress - Motion Picture Musical or Comedy', PERSON),
        ('Best Supporting Actor - Motion Picture', PERSON),
        ('Best Supporting Actress - Motion Picture', PERSON),
        ('Best Screenplay', PRODUCTION),
        ('Best Original Score', PRODUCTION),
        ('Best Original Song', PRODUCTION),
        ('Best Foreign Language Film', PRODUCTION),
        ('Best Animated Feature Film', PRODUCTION),
        ('Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures', PERSON),
        ('Best Drama Series', PRODUCTION),
        ('Best Comedy Series', PRODUCTION),
        ('Best Actor in a Television Drama Series', PERSON),
        ('Best Actor in a Television Comedy Series', PERSON),
        ('Best Actress in a Television Drama Series', PERSON),
        ('Best Actress in a Television Comedy Series', PERSON),
        ('Best Limited Series or Motion Picture made for Television', PRODUCTION),
        ('Best Actor in a Limited Series or Motion Picture made for Television', PERSON),
        ('Best Actress in a Limited Series or Motion Picture made for Television', PERSON),
        ('Best Supporting Actor in a Series, Limited Series or Motion Picture made for Television', PERSON),
        ('Best Supporting Actress in a Series, Limited Series or Motion Picture made for Television', PERSON)
    ]
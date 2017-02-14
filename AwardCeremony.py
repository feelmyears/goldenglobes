import time

class AwardCeremonyKB():
    PERSON = 'PERSON'
    PRODUCTION = 'PRODUCTION'

    def get_awards(self):
        """
        Returns a list of awards
        """
        pass

    def get_awards_and_recipients(self):
        """
        Returns a list of tuples of (award_name, recipient_type) for all awards
        """
        pass

    def get_stopwords(self):
        """
        Returns a list of stopwords for the award ceremony
        """
        pass

class AwardCeremonyApp():
    def get_name(self):
        """
        Returns the ceremony name
        """
        pass

    def get_host(self):
        """
        Returns the ceremony host
        """
        pass

    def get_awards(self):
        """
        Returns a list of awards given out at the ceremony
        """
        pass

    def get_winners(self):
        """
        Returns a dictionary of winners for each award in the form award:winner
        """
        pass

    def get_presenters(self):
        """
        Returns a dictionary of presenters for each award in the form award:presenter
        """
        pass

    def get_bonuses(self):
        """
        Returns a list of tuples bonus items (bonus_item, result)
        """
        pass

    def get_nominees(self):
        """
        Returns a dictionary of a list of nominees for each award in the form of 
        award:[list of nominees]
        """
        pass

class AwardCeremonyScorer():
    def __init__(self, app):
        self.app = app

    def score_app(self):
        start_time = time.time()
        ceremony_name = self.app.get_ceremony()
        print 'Scoring app for {} award ceremony'.format(ceremony_name)

        print 'Please wait while all tweets are classified... (this may take a while)'
        #self.app.classify_tweets()

        host = self.app.get_host()

        print ''
        print 'Determining nominees...'
        nominees = self.app.get_nominees()
        for award, nominees in nominees.iteritems():
            print award + ':'
            for nom in nominees:
                print nom

        print ''
        print 'Determining host...'
        print 'Host: {}'.format(host)

        print ''
        print 'Determining extras...'
        boneses = self.app.get_bonuses()
        for category, winner in boneses.iteritems():
            print '{}: {}'.format(category, winner)

        print ''
        print 'Determining award winners and presenters...'
        awards = self.app.get_awards()
        winners = self.app.get_winners()
        presenters = self.app.get_presenters()
        print presenters

        for a in awards:
            print a
            print '\tWinner:    {}'.format(winners[a])
            presenter_string = ' and/or '.join(map(safe_string, presenters[a]))
            print '\tPresenters: {}'.format(presenter_string)

        end_time = time.time()
        total_time = end_time - start_time

        print ''
        print 'Scored app in {} seconds'.format(total_time)
        print ''
        print 'Presenter and nominees for each award will be implemented in the next submission.'
        print ''
        print 'We also acknowledge that our current implementation is slower than we would like'
        print 'and will work to optimize our implementation for the next submission to achieve'
        print 'sub-minute runtime.'


def safe_string(x):
    return x.encode('ascii', 'ignore').decode('ascii') if x is not None else ''

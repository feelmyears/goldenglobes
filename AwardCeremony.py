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

    def get_winners_and_presenters(self):
        """
        Returns a tuple of dictionarys of winners presenters for each award in the form (award:winner, award:presenter)
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

    def get_network_call_time(self):
        """
        Returns the amount of time spent in network calls
        """

class AwardCeremonyScorer():
    def __init__(self, app):
        self.app = app

    def score_app(self):
        start_time = time.time()
        ceremony_name = self.app.get_ceremony()

        print 'App for {} award ceremony | Created by Philip Meyers IV, Yulun Wu, and Keith Kravis'.format(ceremony_name)
        print ''
        print 'Please wait while all tweets are classified...'
        self.app.classify_tweets()


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
        print 'Determining award winners and presenters... (grab some popcorn, this may take a while)'
        awards = self.app.get_awards()
        # winners = self.app.get_winners()
        # presenters = self.app.get_presenters()
        winners, presenters = self.app.get_winners_and_presenters()
        for a in awards:
            print a
            print '\tWinner:     {}'.format(winners[a])
            presenter_string = ' and/or '.join(map(safe_string, presenters[a]))
            print '\tPresenters: {}'.format(presenter_string)

        end_time = time.time()
        total_time = end_time - start_time
        network_time = self.app.get_network_call_time()

        print ''
        print 'Total runtime:      {} seconds'.format(total_time)
        print 'Network calls time: {} seconds'.format(network_time)
        print 'Local runtime:      {} seconds'.format(total_time - network_time)
        print ''
        print 'Thanks for using and have a great day!'

def safe_string(x):
    return x.encode('ascii', 'ignore').decode('ascii') if x is not None else ''

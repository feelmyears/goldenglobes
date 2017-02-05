class Scorer():
    """
        Takes in an award ceremony app with the following API
        get_ceremony()      Returns the award ceremony name
        get_host()          Returns the award cememony host
        get_awards()        Returns a list of awards given out at the award ceremony
        get_winners()       Returns a dictionary of winners for each award
        get_presenters()    Returns a dictionary of presenters for each award
        get_bonuses()       Returns a dictionary of bonuses like "best dressed" : "Emma Stone"
    """
    def __init__(self, app):
        self.app = app

    def score_app(self):
        ceremony_name = self.app.get_ceremony()
        host = self.app.get_host()
        print 'Scoring app for {} award ceremony, hosted by {}'.format(ceremony_name, host)
        bonuses = self.app.get_bonuses()
        for bonus in bonuses:
            print bonus
            print bonuses[bonus]
        awards = self.app.get_awards()
        presenters = self.app.get_presenters()
        winners = self.app.get_winners()
        for a in awards:
            print a
            print '\tPresenter: {}'.format(presenters[a])
            print '\tWinner:    {}'.format(winners[a])

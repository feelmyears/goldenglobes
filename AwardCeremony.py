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
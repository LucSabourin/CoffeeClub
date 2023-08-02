from config import peoplePath, LOCAL
from datamgmt.clear import deleteFile


class Person():
    """Person object representing a person to be matched for a coffee chat.

    Attributes:
    -----------
    name : str
        The name of the person
    email : str
        The email of the person
    available : list
        Pool of available people for the weeks meetings
    alreadyMet : list
        Pool of people this person has already met
    yetToMeet : list
        Pool of people from available that this person has yet to meet
    matched : bool
        Boolean describing whether this person has been matched
    _storePath : str
        The path to the stored list of people this person has already met

    Methods:
    --------
    matchName(name : str) -> bool
        Returns a boolean based on weather or not this person can meet
        with the supplied name; if so returns True and adjusts attributes
        accordingly, otherwise returns False.
    revert() -> None
        Reverts this person's match status to their previous match status;
        this includes moving the most recently added name from alreadyMet back
        to yetToMeet.
    findYetToMeet() -> None
        Assigns yetToMeet by keeping all names in available that are not in
        alreadyMet, and if there are no names assigned to yetToMeet (i.e.) all
        available people have already been met, uses all names in available for
        yetToMeet.
    getAlreadyMet() -> None
        Backs up list of people with whom this person has already met.
    storeAlreadyMet() -> None
    """

    def __init__(self, name : str, guid : str, available : list = None, alreadyMet : list = None):
        self.name = name
        self.guid = guid
        self.yetToMeet = []
        self.matched = False
        self._storePath = peoplePath + name + '.txt'
        if available is None:
            self.available = []
        else:
            self.available = available
        if alreadyMet is None:
            self.alreadyMet = []
        else:
            self.alreadyMet = alreadyMet

    def matchName(self, name : str) -> bool:
        """Returns a boolean based on weather or not this person can meet
        with the supplied name; if so returns True and adjusts attributes
        accordingly, otherwise returns False.

        Parameters:
        -----------
        name : str
            string representing another person's name
        
        Returns:
        --------
        bool
            If this person can meet with the other person, return True,
            otherwise return False
        """

        if name in self.alreadyMet:
            return False

        if name not in self.yetToMeet:
            return False

        for nameToMeet in self.yetToMeet:
            if nameToMeet == name:
                self.alreadyMet.append(name)
                self.yetToMeet.remove(name)
                break
        
        self.matched = True
        return True

    def revert(self, name : str) -> None:
        """Reverts this person's match status to their previous match status;
        this includes moving the most recently added name from alreadyMet back
        to yetToMeet.
        """

        try:
            self.alreadyMet.remove(name)
        except Exception as e:
            #print(e)
            pass
        else:
            self.yetToMeet.append(name)
        self.matched = False

    def findYetToMeet(self) -> None:
        """Assigns yetToMeet by keeping all names in available that are not in
        alreadyMet, and if there are no names assigned to yetToMeet (i.e.) all
        available people have already been met, uses all names in available for
        yetToMeet.
        """

        for name in self.available:
            if name not in self.alreadyMet:
                self.yetToMeet.append(name)
        
        if len(self.yetToMeet) == 0:
            self.yetToMeet = self.available
            self.alreadyMet = []

    def getAlreadyMet(self) -> None:
        """Retrieves all names from stored list of people this person has
        already met to build alreadyMet attribute.
        """

        from datamgmt.blob import extractText

        self.alreadyMet = extractText(self._storePath)

    def storeAlreadyMet(self) -> None:
        """Backs up list of people with whom this person has already met."""

        from datamgmt.store import storeAlreadyMatched

        deleteFile(path=self._storePath)
        storeAlreadyMatched(path=self._storePath, names=self.alreadyMet)

    def serialize(self) -> dict:
        """
        """

        serialized = {}
        serialized['name'] = self.name
        serialized['guid'] = self.guid
        serialized['alreadyMet'] = self.alreadyMet
        return serialized
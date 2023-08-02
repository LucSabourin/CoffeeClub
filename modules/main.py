from random import randint

from classes.person import Person
from classes.errors import UnmatchedPersons, ServerError
from datamgmt.extract import extractExcel, getBackUp
from config import LOCAL, peoplePath
from datamgmt.clear import deleteBackUp
from support import getNames, matchNames, namesNotMatched, addExtras, prepareMatched
from datamgmt.store import saveMatchedCsv, storeMatchReport, storeBackUp

def buildLists(test : bool = False) -> dict:
    """Builds the person object for each name extracted from the source Excel
    file which has opted in.

    Parameters:
    -----------
    test : bool = False
        apply a random value to OptIn weighted at 75% for In and 25% for Out

    Returns:
    --------
    dict
        dictionary containing Person objects for each person to be matched
    """

    df = extractExcel()

    coffeeClub = {}    
    names = getNames(df, test)
    backup = getBackUp()
    if backup is not None:
        for person in backup:
            coffeeClub[person['name']] = Person(name=person['name'], guid=person['guid'], alreadyMet=person['alreadyMet'])

    all = [personName for personName, _ in names]
    for name, guid in names:
        all.remove(name)
        
        if name not in coffeeClub.keys():
            person = Person(name, guid, all)
            if LOCAL:
                person.getAlreadyMet()
            person.findYetToMeet()
            coffeeClub[name] = person
        else:
            coffeeClub[name].available = all

        all.append(name)
    return coffeeClub

def randMatch(coffeeClub : dict, name1 : str, match : dict = None) -> bool:
    """Finds a random match for person matching name1 to a name from name1's
    yetToMeet list. If a match is found, returns True, otherwise returns False.

    Parameters:
    -----------
    coffeeClub : dict
        dictionary containing the person objects for each name extracted
    name1: str
        name to be matched.
    match : dict
        dictionary containing matches for the week

    Returns:
    --------
    bool
        if a match is found for name1, returns True, otherwise returns False.
    """

    if match is None:
        match = {}

    if not namesNotMatched(match, name1):
        return True

    person1 = coffeeClub[name1]
    matchTried = []
    while True:
        if len(matchTried) == len(person1.yetToMeet):
            return False

        num = randint(0, len(person1.yetToMeet) - 1)
        if num in matchTried:
            continue

        name2 = person1.yetToMeet[num]
        person2 = coffeeClub[name2]

        if namesNotMatched(match, name1, name2):
            if matchNames(match, person1, person2):
                return True
            break
        else:
            matchTried.append(num)

    '''
    if matched is False:
        return randMatch(coffeeClub, name1, match, matchTried)
    elif not namesNotMatched(match, name1):
        person1.revert()
        person2.revert()
        match.pop(name1)
    return False
    '''

def runMatch(counter : int = 0, test : bool = False) -> None:
    """Finds a match for each name extracted and save the matches to the Excel
    UI and a backup as a CSV.

    Parameters:
    -----------
    counter : int = 0
        week number being generated - used in testing
    test : bool = False
        apply a random value to OptIn weighted at 75% for In and 25% for Out
    """

    coffeeClub = buildLists(test)
    matched = {}
    for name1 in coffeeClub.keys():
        randMatch(coffeeClub=coffeeClub, name1=name1, match=matched)
    
    if len([name for name, person in coffeeClub.items() if person.matched is False]) > 0:
        addExtras(coffeeClub, matched)
    
    if len([name for name, person in coffeeClub.items() if (person.matched is False) or ((len(person.yetToMeet) == 0) and (namesNotMatched(matched, name)))]) > 0:
        raise UnmatchedPersons

    sorted = prepareMatched(coffeeClub, matched)

    if LOCAL:
        for person in coffeeClub.values():
            person.storeAlreadyMet()

        saveMatchedCsv(matched, counter)

        return storeMatchReport(coffeeClub=coffeeClub, matched=matched, counter=counter, test=test)
    else:
        backup = []
        for person in coffeeClub.values():
            backup.append(person.serialize())
        try:
            deleteBackUp()
        except ServerError:
            pass
        
        url = storeBackUp(backUp=backup)
        report = storeMatchReport(coffeeClub=coffeeClub, matched=matched, counter=counter, test=test)


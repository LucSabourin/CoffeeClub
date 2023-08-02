import os
from pandas import DataFrame
from datetime import datetime, timedelta

from classes.person import Person
from config import LOCAL
from datamgmt.store import saveMatchedExcel

def fileExists(path : str) -> bool:
    """Determines if a path exists.

    Parameters:
    -----------
    path : str
        string of the path to be checked

    Returns:
    --------
    bool
        if file exists returns True, otherwise returns false
    """

    return os.path.isfile(path)

def getNames(df : DataFrame, test : bool = False) -> list:
    """Retrieves names of people who have opted in.

    Parameters:
    -----------
    df : DataFrame
        DataFrame containing names for the coffee club
    test : bool = False
        apply a random value to OptIn weighted at 75% for In and 25% for Out

    Returns:
    --------
    list
        list of names extracted
    """

    names = []
    if test is True:
        from random import randint
        df['OptedOut'] = df['OptedOut'].apply(lambda x: False if randint(0, 1) * randint(0, 1) == 0 else True)
    df = df.loc[df['OptedOut'] == False]

    for index in df.index:
        names.append((df.loc[index, 'Full Name'], df.loc[index, '(Do Not Modify) Participant']))

    return names

def namesNotMatched(match : dict, name1 : str, name2 : str = '') -> bool:
    """Determines if names are in match dictionary; if so, return True,
    otherwise return False.

    Parameters:
    -----------
    match : dict
        dictionary containing matches accumulated so far
    name1 : str
        first name to be checked
    name2 : str = ''
        second name to be checked (independent of name1)

    Returns:
    --------
    bool
        if either name is found in match, returns True, otherwise returns False
    """

    if name2 != '':
        return namesNotMatched(match, name2)
    
    if name1 in match.keys():
        return False
        
    if name1 in match.values():
        return False

    return True

def matchNames(match : dict, person1 : Person, person2 : Person) -> bool:
    """If person1 and person2 have not already been matched with each other,
    match them together and update the match dictionary accordingly.

    Parameters:
    -----------
    match : dict
        dictionary containing matches accumulated so far
    person1 : Person
        first person to match
    person2 : Person
        second person to match

    Returns:
    --------
    bool
        if the two people were successfully matched, returns True, otherwise
        returns False
    """

    if not person1.matchName(person2.name):
        return False

    if not person2.matchName(person1.name):
        person1.revert(person1.name)
        return False

    if namesNotMatched(match=match, name1=person1.name):
        match[person1.name] = person2.name
    else:
        if person1.name in match.keys():
            nameKey = person1.name
        
        elif person1.name in match.values():
            for name1, name2 in match.items():
                if person1.name == name2:
                    nameKey = name1
                    break
        
        if '/' in match[nameKey]:
            return False
        match[nameKey] += '/' + person2.name

    return True

def addExtras(coffeeClub : dict, matched : dict) -> None:
    """Instances where there is an odd number of people to be matched, or
    people who could not be matched with remaining individuals, matches
    outlyers to an existing match where the individuals have not already met
    each person in the existing match.

    Parameters:
    -----------
    coffClub : dict
        dictionary of Person objects
    matched : dict
        dictionary of accululated matches so far
    """

    missing = []
    for name in coffeeClub.keys():
        if name not in matched.keys() and name not in matched.values():
            missing.append(name)

    for name in missing:
        person = coffeeClub[name]
        hasMatched = False
        if len(person.yetToMeet) > 0:
            for other in person.yetToMeet:
                for name1, name2 in matched.items():

                    if other == name1:
                        matchNames(matched, coffeeClub[name1], person)
                        if person.matched is True:
                            hasMatched = True
                            break

                    elif other == name2:
                        matchNames(matched, coffeeClub[name2], person)
                        if person.matched is True:
                            hasMatched = True
                            break
                if hasMatched is True:
                    break
            if hasMatched is True:
                continue

        if len(person.yetToMeet) == 0 or hasMatched is False:
            for name1, name2 in matched.items():
                if '/' not in name2:
                    matched[name1] = name2 + '/' + name
                    person.matched = True
                    break
            continue

        

def getDay(counter : int) -> str:
    """Builds the date string for the week.

    Parameters:
    -----------
    counter : int
        week number being generated - used in testing

    Returns:
    --------
    str
        formatted string containing the dates of the week for the matches.
        Format is as follows:
            '<Monday : str : YYYY-MM-DD> to <Friday : str : YYYY-MM-DD>'
    """

    today = datetime.today() + timedelta(counter * 7)
    dayOfWeek = today.weekday()
    startDay = today - timedelta(dayOfWeek)
    endDay = startDay + timedelta(4)

    dateString = startDay.strftime('%Y-%m-%d') + 'to' + endDay.strftime('%Y-%m-%d')
    return dateString

def matchReport(coffeeClub : dict, matched : dict) -> dict:
    """Generates values for Match Report.

    Parameters:
    -----------
    coffeeClub : dict
        dictionary containing the person objects for each name extracted
    matched : dict
        dictionary containing matches for the week's coffee club
    
    Returns:
    --------
    dict
        dictionary containing the report contents for the weeks Match Report
    """
    report = {}
    report['numPeople'] = {
        'value': len(coffeeClub.keys()),
        'text': 'Number of People:'
    }
    report['numMatches'] = {
        'value': len(matched.keys()),
        'text': 'Number of Matches:'
    }
    report['numTriple'] = {
        'value': len([name2 for name2 in matched.values() if '/' in name2]),
        'text': 'Number of 3 way matches:'
    }
    report['numUnmatched1'] = {
        'value': len([person for person in coffeeClub.values() if not person.matched]),
        'text': 'Number of Unmatched People (found by method 1):'
    }
    report['numUnmatched2'] = {
        'value': report['numPeople']['value'] - 2 * report['numMatches']['value'] - report['numTriple']['value'],
        'text': 'Number of Unmatched People (found by method 2):'
    }
    report['unmatchedMatch'] = {
        'value': report['numUnmatched1']['value'] == report['numUnmatched2']['value'],
        'text': 'Number of Unmatched People found from each method Match:'
    }
    report['unmatched'] = {
        'value': {name: {'yetToMeet': person.yetToMeet, 'alreadyMet': person.alreadyMet} for name, person in coffeeClub.items() if person.matched is False or (name not in matched.keys() and len([name2 for name2 in matched.values() if name in name2]) == 0)},
        'text': 'Names of Unmatched Persons'
    }
    return report

def prepareMatched(coffeeClub : dict, matched : list) -> list:
    """
    """

    matchedFinal = []
    for name1, name2 in matched.items():
        match = {'ParticipantA': None, 'GUID_ParticipantA': None, 'ParticipantB': None, 'GUID_ParticipantB': None, 'ParticipantC': None, 'GUID_ParticipantC': None}

        match['ParticipantA'] = name1
        match['GUID_ParticipantA'] = coffeeClub[name1].guid

        if '/' in name2:
            names = name2.split('/')
            match['ParticipantB'] = names[0]
            match['ParticipantC'] = names[1]
            match['GUID_ParticipantB'] = coffeeClub[names[0]].guid
            match['GUID_ParticipantC'] = coffeeClub[names[1]].guid
        else:
            match['ParticipantB'] = name2
            match['GUID_ParticipantB'] = coffeeClub[name2].guid
        
        matchedFinal.append(match)

    if LOCAL:
        saveMatchedExcel(matched=matchedFinal)
    else:
        return matchedFinal


if __name__ == "__main__":
    print(getDay())
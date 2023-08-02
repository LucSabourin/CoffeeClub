import pandas as pd
import json

from config import excelPath, csvPath, testReportPath
from support import getDay, matchReport
from datamgmt.blob import post_file_to_blob

def saveMatchedExcel(matched : list) -> None:
    """Updates information stored in Excel dashboard for easy copy/paste into
    an email.

    Parameters:
    -----------
    matched : list
        list of dictionaries containing matches for the week's coffee club
    """

    df = pd.read_json(json.dumps(matched))
    fileName = excelPath.replace('Data.xlsx', 'Matches.xlsx')

    df.to_excel(fileName, 'Matches')

def saveMatchedCsv(matched : dict, counter : int) -> None:
    """Saves a backup of the matches found as a csv.

    Parameters:
    -----------
    matched : dict
        dictionary containing matches for the week's coffee club
    counter : int
        week number being generated - used in testing
    """

    matches = []
    for name1, name2 in matched.items():
        matches.append({'Person1': name1, 'Person2': name2})
    
    df = pd.read_json(json.dumps(matches))
    fileName = csvPath + getDay(counter) + '_matches.csv'

    df.to_csv(fileName)

def storeAlreadyMatched(path : str, names : list) -> None:
    """Stores a list of names as a text file.

    Parameters:
    -----------
    path : str
        destination path for the text file
    names : list
        list of names to be stored in the text file
    """

    with open(path, 'w', encoding='utf-8') as f:
        for name in names:
            line = name
            line += '\n'
            f.write(line)

def storeMatchReport(coffeeClub : dict, matched : dict, counter : int, test : bool) -> dict:
    """Build and store the Match Report for each match. Match report includes
    number of participants, number of matches, number of 3 way matches, number
    of unmatched people via 2 different methods (attribute from Person object)
    and mathematically from matches vs total participants, and compares those
    two methods to confirm that they are both correct.

    Parameters:
    -----------
    coffeeClub : dict
        dictionary containing the person objects for each name extracted
    matched : dict
        dictionary containing matches for the week's coffee club
    counter : int
        week number being generated - used in testing
    test : bool
        used to return the report to make a combined report across collective tests

    Returns:
    --------
    dict
        returns the report dictionary if test is true, otherwise returns None
    """

    report = matchReport(coffeeClub=coffeeClub, matched=matched)
    days = getDay(counter)
    fileName = csvPath + days + '_report.txt'
    
    with open(fileName, 'w', encoding='utf-8') as f:
        line = 'Match Report: ' + days.replace('to', ' to ') + '\n'
        line += '=' * 38 + '\n\n'
        for value in report.values():
            if type(value['value']) != dict:
                line += value['text'] + ' ' + str(value['value']) + '\n'
            else:
                line += '\n' + value['text'] + '\n'
                for name in value['value'].keys():
                    line += name + ',\n'
                    
                    line += '    Yet To Meet:\n'
                    for other in value['value'][name]['yetToMeet']:
                        line += '    ' + other + ',\n'
                    
                    line += '\n    Already Met:\n'
                    for other in value['value'][name]['alreadyMet']:
                        line += '    ' + other + ',\n'
                    
                    line += '\n'
                    
        f.write(line)

    if test is True:
        report['days'] = days
        return report

def storeTestingReports(reports : dict, weeks : int, totalTime : float) -> None:
    """
    """

    tests = []
    for report in reports:
        testing = {}
        for key, value in report.items():
            if type(value) == dict:
                testing[key] = value['value']
            else:
                testing[key] = value
        tests.append(testing)
    with open(testReportPath.format(weeks), 'w', encoding='utf-8') as f:
        json.dump(tests, f, indent=4)

def storeBackUp(backUp : list) -> str:
    """
    """

    return post_file_to_blob('matches.json', json.dumps(backUp))
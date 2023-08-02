import time

from main import runMatch
from datamgmt.clear import deleteMatched, deleteBackUp
from datamgmt.store import storeTestingReports
from classes.errors import UnmatchedPersons
from config import LOCAL

def funcTest(iter : int = 104, count : int = 0, startTime: float = None, reports : list = None):
    if reports is None:
        reports = []
    if startTime is None:
        deleteBackUp()
        deleteMatched()
        startTime = time.time()
    broken = False
    while count < iter:
        try:
            reports.append(runMatch(count, test=True))
        except UnmatchedPersons:
            deleteMatched()
            funcTest(iter=iter, count=count, startTime=startTime, reports=reports)
            broken = True
            break
        except Exception as e:
            completionTime = time.time() - startTime
            storeTestingReports(reports, count + 1, completionTime)
            broken = True
            break
        else:
            count += 1
    if not broken:
        totalTime = time.time() - startTime
        storeTestingReports(reports, iter, totalTime)

def funcRun():
    try:
        runMatch()
    except UnmatchedPersons:
        if LOCAL:
            deleteMatched()
        else:
            deleteBackUp()
        funcRun()


if __name__ == '__main__':
    funcRun()
import os

from config import peoplePath, csvPath, LOCAL
from datamgmt.blob import delete_file_from_blob

def deleteFile(path : str) -> None:
    """Used to delete a file at the given path.

    Parameters:
    -----------
    path : str
        path of file to be deleted
    """

    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception as e:
        print(f'Failed to delete {path}. Reason: {e}')

def deleteMatched() -> None:
    """Delete all backup matched files from peoplePath."""

    folder = peoplePath
    if folder[-1] == '/':
        folder = folder[0:-1]
    for fileName in os.listdir(folder):
        path = os.path.join(folder, fileName)
        deleteFile(path)

def deleteBackUp() -> None:
    """Delete all stored csvs with each week's matches from csvPath."""

    if LOCAL:
        folder = csvPath
        if folder[-1] == '/':
            folder = folder[0:-1]
        for fileName in os.listdir(folder):
            path = os.path.join(folder, fileName)
            deleteFile(path)
    else:
        delete_file_from_blob('matches.json')

if __name__ == '__main__':
    deleteBackUp()
    deleteMatched()
    
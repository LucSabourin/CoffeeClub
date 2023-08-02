import pandas as pd
from pandas import DataFrame
import warnings, json

from classes.errors import ServerError
from config import excelPath, excelSheet
from support import fileExists
from datamgmt.blob import get_file_from_blob


def extractExcel() -> DataFrame:
    """Extracts the excel contents using pandas and returns the corresponding
    DataFrame.

    Returns:
    --------
    DataFrame
        DataFrame containing the contents of the excel book used to store the
        information
    """

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(excelPath, excelSheet)
    return df

def extractText(path : str) -> list:
    """Extract the contents of the text file returning the names in each file
    as a list.

    Parameters:
    -----------
    path : str
        the path of the text file

    Returns:
    --------
    list
        list of names stored in text file
    """

    names = []
    if not fileExists(path):
        return names

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            names.append(line.strip())
    
    return names

def getBackUp() -> list:
    """
    """

    try:
        file = get_file_from_blob(location='matches.json')
    except ServerError:
        pass
    else:
        data = json.load(file)
        print(data)
        return data
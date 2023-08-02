import pandas as pd
import warnings
from config import excelPath, excelSheet

def func():
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        dfs = pd.read_excel(excelPath)
    
    print(type(dfs))
    print(dfs)
    for df in dfs:
        print(type(df))
        print(df)

def func2():
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(excelPath, excelSheet)
    print(type(df))
    print(df)

if __name__ == "__main__":
    func2()

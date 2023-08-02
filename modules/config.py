import os

ROOTDIR = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
excelPath = '/'.join(ROOTDIR.split('/')[:-1]) + '/Data.xlsx'
excelSheet = 'Export View'
csvPath = '/'.join(ROOTDIR.split('/')[:-1]) + '/matched_backup/'
peoplePath = '/'.join(ROOTDIR.split('/')[:-1]) + '/people/'
testReportPath = '/'.join(ROOTDIR.split('/')[:-1]) + '/setup/testReport_{}_weeks.json'

# LOCAL = True
LOCAL = False

def funcTest():
    print(ROOTDIR)
    print(excelPath)
    print(csvPath)
    print(peoplePath)

if __name__ == '__main__':
    funcTest()
from . import Riveter
import csv

MAX_ROWS = 1048576
MAX_COLS = 16384

# Child class of Riveter that checks for dates and standardizes them
# @author MWK
class MaxFileSizeRiveter(Riveter.MetaRiveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, csvFile):
        # Specifications from https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3
        # Key details:
        # 1,048,576 rows by 16,384 columns
        analysis = {}
        delim = self.sniffDelimiter(csvFile)
        reader = csv.reader(csvFile, delim)
        analysis["detected"] = {}

        colnum = 1
        rownum = 1
        with open(csvFile) as f:
            reader = csv.reader(f, delim)
        # Get maximum file row size and file column size
            for row in reader:
                rownum += 1
                # Branchless programming:
                colnum = (len(row) > colnum) * len(row) + (len(row) <= colnum) * colnum

        mre = rownum >= MAX_ROWS
        mce = colnum >= MAX_COLS
        result = "Total Rows: {rows}<br>Total Cols: {cols}<br>Max Rows Exceeded: {mre}<br>Max Cols Exceeded: {mce}".format(rows=rownum, cols=colnum, mre=mre, mce=mce)
        analysis["detected"]["data"] = result
    
        analysis["hits"] = [1]     
            
        return analysis

    def scream(self):
        return "MaxFileSizeRiveter"

MaxFileSizeRiveter()
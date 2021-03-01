from __future__ import unicode_literals, print_function

#Article about the date inconsistency: https://academy.datawrapper.de/article/89-prevent-excel-from-changing-numbers-into-dates
import sys, os, json
import rosie
import csv
from excel import *

if sys.version_info.major < 3:
    str23 = lambda s: str(s)
    bytes23 = lambda s: bytes(s)
else:
    str23 = lambda s: str(s, encoding='UTF-8')
    bytes23 = lambda s: bytes(s, encoding='UTF-8')

def readFile(data_file):
#     librosiedir = './lib'
#     rosie.load(librosiedir, quiet=True)
    engine = rosie.engine()
    engine.import_package("date")
    date_patterns = engine.compile("date.any")
    info = {}
    with open(data_file, 'r') as csvfile:
        content = csvfile.read()
        is_sylk = False
        if content[0:2] == "ID":
            is_sylk = True
        info["SYLK"] = is_sylk
        csvfile.seek(0)
        dial = csv.Sniffer().sniff(csvfile.read(), delimiters=';,| \t')
        info["DUTCHSEP"] = dial.delimiter
        csvfile.seek(0)    
        fileRead = csv.reader(csvfile, dialect=dial)
        keys = next(fileRead)
        print("CSV file has these column headings: {}".format(keys))
        cols = len(keys)
        rows = 0
        date_found = []
        num_found = []
        injection_found = []
        all = []
        date_counter = [0] * cols
        actual_date_counter = [0] * cols
        total_counter = [0] * cols
        date_check = engine.compile("{ { \"APR\" / \"OCT\" / \"MARCH\" / \"SEPT\" } [:digit:]* }")
        num_check = engine.compile("{ [0]+ [:digit:]+ } / [0]+")
        engine.load("short_year = [0-9]{ 2 }")
        excel_check = engine.compile("{ { date.month { \"-\" / [/] } short_year } / { date.day { \"-\" / [/] } date.month } }")
        limit = r"[:digit:]{15,}"
        num_check1 = engine.compile(limit)
        #num_check2 = engine.compile("{ [:digit:]+ {\"e\" / \"E\"} {[\\-]? [:digit:]*}}")
        for row in fileRead:
            rows += 1
            for i in range(0, cols):
                element = row[i]
                #print(element)
                if element != None:
                    total_counter[i] += 1
                if date_patterns.fullmatch(element) != None:
                    actual_date_counter[i] += 1
                    all.append({"row_no" : rows, "col_no": i + 1, "data" : element, "type": "ACTUALDATE"})
                if num_check.fullmatch(element) != None or num_check1.fullmatch(element) != None:
                    num_found.append({"row_no" : rows, "col_no": i + 1, "data" : element})
                    all.append({"row_no" : rows, "col_no": i + 1, "data" : element, "type": "BIGNUM"})
                if date_check.fullmatch(element.upper()) != None or excel_check.fullmatch(element) != None:
                    date_counter[i] += 1
                    date_found.append({"row_no" : rows, "col_no": i + 1, "data" : element})
                    all.append({"row_no" : rows, "col_no": i + 1, "data" : element, "type": "NOTADATE"})
                if element[0] == "=":
                    injection_found.append({"row_no" : rows, "col_no": i + 1, "data" : element})
                    all.append({"row_no" : rows, "col_no": i + 1, "data" : element, "type": "INJECTION"})
        info["ROWS"] = rows
        info["COLUMNS"] = cols
        info["INJECTION"] = injection_found
        info["NOTADATE"] = date_found
        info["BIGNUM"] = num_found
        info["DATESTAT"] = [[a / c, b / c] for a, b, c in zip(date_counter, actual_date_counter, total_counter) ]
        print(info["DATESTAT"])
    with open(data_file[0:len(data_file) - 4] + "_sorted.txt", 'w') as file:
        json.dump(all, file)
    return info

def writeFile(info, data_file):
    with open(data_file[0:len(data_file) - 4] + "_analysis.txt", 'w') as file:
        json.dump(info, file)

def getColumnExcel(n):
    
    excel_column = ""
    while n > 0:
        rem = (n - 1) % 26
        excel_column = chr(rem + 65) + excel_column
        n = (n - 1) // 26
    
    return excel_column

if __name__ == "__main__":
    data_file = sys.argv[len(sys.argv) - 1]
    try:
        with open(data_file, "r") as check:
            check.close()
    except IOError:
        print("Can't open the CSV file entered. Please try again.")
        sys.exit()
    info = None
    length = len(data_file)
    if os.path.exists(data_file[0:length - 4] + "_analysis.txt"):
        with open(data_file[0:length - 4] + "_analysis.txt", "r") as json_file:
            info = json.load(json_file)
    else:
        info = readFile(data_file)
    print("CSV file uses " + info["DUTCHSEP" ] + " as separator")
    print("CSV file has " + str(info["COLUMNS"]) + " columns, " + str(info["ROWS"]) + " rows")
    if info["SYLK"] == False:
        print("NOTSYLK   True   This CSV file will not be mistaken for a SYLK file")
    else:
        print("NOTSYLK   False   This CSV file will be mistaken for a SYLK file")

    if len(info["INJECTION"]) > 0:
        print("INJECTION FOUND")
        for each in info["INJECTION"]:
            print("\tRow " + str(each["row_no"]) + ", " + "Col " + getColumnExcel(each["col_no"]) + "   " + str(each["data"]))
    else:
        print("INJECTION None")
        
    if len(info["NOTADATE"]) > 0:
        print("NOTADATE FOUND")
        for each in info["NOTADATE"]:
            print("\tRow " + str(each["row_no"]) + ", " + "Col " + getColumnExcel(each["col_no"]) + "   " + str(each["data"]))
    else:
        print("NOTADATE None")

    if len(info["BIGNUM"]) > 0:
        print("BIGNUM FOUND")
        for each in info["BIGNUM"]:
            print("\tRow " + str(each["row_no"]) + ", " + "Col " + getColumnExcel(each["col_no"]) + "   " + str(each["data"]))
    else:
        print("BIGNUM None")

    writeFile(info, data_file)
    if "-m" in sys.argv:
        read_file_excel(data_file[0:length - 4] + "_analysis.txt")

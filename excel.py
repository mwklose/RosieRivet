import json, os, rosie, csv, sys

THRESHOLD = 0.8

month_dict = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12
}

def date_format(element):
    #print(element)
    librosiedir = './lib'
    rosie.load(librosiedir, quiet=True)
    engine = rosie.engine()
    engine.import_package("date")
    date_patterns = engine.compile("date.any")
    match = date_patterns.fullmatch(element).rosie_match
    type_of_format = match['subs'][0]['type']
    #print(type_of_format)
    if type_of_format == "date.us_long":
        #print("us long")
        if match['subs'][0]['subs'][0]['type'] == "date.day_name":
            return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][2]['data'] + ", " + match['subs'][0]['subs'][3]['data']
        else:
            return match['subs'][0]['subs'][0]['data'] + " " + match['subs'][0]['subs'][1]['data'] + ", " + match['subs'][0]['subs'][2]['data']
    elif type_of_format == "date.eur":
        #print("europe")
        return match['subs'][0]['subs'][1]['data'] + "/" + match['subs'][0]['subs'][0]['data'] + "/" + match['subs'][0]['subs'][2]['data']
    elif type_of_format == "date.spaced":
        #print("spaced")
        return element.replace(" ", "/")
    elif type_of_format == "date.spaced_en" or (type_of_format == "date.rfc2822" and "," not in element):
        #print("eng or rfc")
        return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][2]['data'] + ", " + match['subs'][0]['subs'][0]['data']
    elif type_of_format == "date.rfc2822" and "," in element:
        #print("big rfc")
        index = element.rindex(",")
        return date_format(element[index + 1:].strip())
    elif type_of_format == "date.us_short":
        #print(match['subs'][0]['subs'])
        return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][0]['data'] + ", " + match['subs'][0]['subs'][2]['data']
    return element

def getSortedData(data_file):
    data = None
    try:
        with open(data_file[0:len(data_file) - 13] + "_sorted.txt", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("File does not exist. Make sure to run the analysis on the csv file first and then run this program again with the name of the analysis file created.")
        exit()
    row = data[0]["row_no"]
    row_keys = {row:{"row_data":[], "col_data":{}}}
    #print(row_keys)
    for each in data:
        if row != each["row_no"]:
            row = each["row_no"]
            row_keys[row] = {}
            row_keys[row]["row_data"] = [each]
            row_keys[row]["col_data"] = {}
            row_keys[row]["col_data"][each["col_no"]] = each["type"]
        else:
            #print(row_keys[row])
            row_keys[row]["row_data"].append(each)
            row_keys[row]["col_data"][each["col_no"]] = each["type"]
    #print(row_keys)
    return row_keys

def make_dates_uniform(date):
    date = date.lower()
    index_month = date.find(" ")
    index_day = date.find(",")
    return str(month_dict[date[0: index_month]]) + "/" + date[index_month + 1: index_day] + "/" + date[index_day + 2:]

def solve(elem):
    return "\"=\"" + "\"" + elem + "\"" + "\"" + "\""

def find_remedy(elem, typ, stat):
    if typ == "INJECTION":
        return solve(elem)
    elif typ == "NOTADATE":
        #print(elem, stat)
        if stat[1] >= THRESHOLD or (stat[1] != 0.0 and stat[1] + stat[0] >= 0.9):
            return elem
        else:
            return solve(elem)
    elif typ == "ACTUALDATE":
        date = date_format(elem)
        if "," in date:
            date = make_dates_uniform(date)
        return date
    else:
        return solve(elem)

def read_file_excel(data_file):
    data = None
    try:
        with open(data_file, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("data_file", data_file)
        print("File does not exist. Make sure to run the analysis on the csv file first and then run this program again with the name of the analysis file created.")
        exit()
    #print("here")
    row_keys = getSortedData(data_file)
    try:
        with open(data_file[0:len(data_file) - 13] + ".csv", "r") as csvfile:
            stats = data["DATESTAT"]
            fileRead = csv.reader(csvfile, delimiter = data["DUTCHSEP"])
            keys = next(fileRead)
            if data["SYLK"]:
                keys[0] = "id"
            outfile = open(data_file[0:len(data_file) - 13] + "_modified.csv", "w")
            outfile.write(",".join(keys) + "\n")
            cols = len(keys)
            rows = 0
            for row in fileRead:
                rows += 1
                if rows not in row_keys.keys():
                    outfile.write(",".join(row) + "\n")
                    continue
                elem_arr = []
                for i in range(0, cols):
                    element = row[i]
                    if i + 1 not in row_keys[rows]["col_data"].keys():
                        if "," in element:
                            element = "\"" + element + "\""
                        elem_arr.append(element)
                        continue
                    incon_type = row_keys[rows]["col_data"][i + 1]
                    remedy = find_remedy(element, incon_type, stats[i])
                    elem_arr.append(remedy)
                outfile.write(",".join(elem_arr) + "\n")
            outfile.close()

    except FileNotFoundError:
        print("CSV file does not exist or the name of the analysis file was changed. Please run the analysis again and do not change the name of the analysis created after.")
        exit()


if __name__ == "__main__":
    data_file = sys.argv[1]
    read_file_excel(data_file)

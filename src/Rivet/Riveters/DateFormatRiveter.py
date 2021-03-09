from . import Riveter
import rosie
#Child class of Riveter that checks for dates and standardizes them

def solve(elem):
            return "\"=\"" + "\"" + elem + "\"" + "\"" + "\""

def make_dates_uniform(date):
    date = date.lower()
    index_month = date.find(" ")
    index_day = date.find(",")
    return str(month_dict[date[0: index_month]]) + "/" + date[index_month + 1: index_day] + "/" + date[index_day + 2:]

#Given an element, according to stat provided, determines the correct way to remedy data in order to prevent
#excel from possible misinterpretation 
def find_remedy(self, elem, typ, stat):
    THRESHOLD = 0.8
    if typ == "NOTADATE":
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

#Determines the correct date to use
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
    
# @author MWK
class DateFormatRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, column):
        return {"detected" : {},
                "confidence" : {},
                "hits" : {}}

    def apply(self, csvFile, options, confidence):
        pass

    def scream(self):
        return "DateFormatRiveter"
    


DateFormatRiveter()
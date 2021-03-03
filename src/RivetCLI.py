from Rivet import RosieRivet
import sys
import pprint

# Jennigns comments:
# 1. Less fine grain control for users in CLI
# 2. guarantee data structure (via abstract class, check when passing back)
# 3. guarantee key existence
# 4. analyze only riveters?
# 5. Demo riveter for researchers?

pp = pprint.PrettyPrinter(indent=4)

def main(file, silentMode):
    print("In main with", file)
    rr = RosieRivet.RosieRivet(file) # call constructor of RosieRivet

    # Analyze File
    myAnalysis = analyzeFile(rr)
    
    # Approve File
    options = approveFile(rr, myAnalysis, silentMode)

    # Process File
    rivetCSV, rivetTXT = processFile(rr, options)

    # Write File
    writeFile(rivetCSV, rivetTXT)

    return

#calls in the RosieRivet RivetFileAnalyzer function; starts the analysis process which trickles
    #down the hierarchy all the way to the individual scenario riveters
def analyzeFile(rr):
    return rr.RivetFileAnalyzer()

#starts interaction between user and system to approve the potential changes to files
   #will eventually display each column that could be misread and gets user to approve or deny
    #that this column needs to be protected.
def approveFile(rr, analysis, silentMode):
    if silentMode:
        return analysis

    print("--------------------")
    rivetsToRemove = []
    for r in rr.riveters:
        # See if riveting even possible
        if len(analysis[r.scream()]) == 0:
            print("No rivets for", r.scream())
            rivetsToRemove.append(r)
            continue

        print("----------", "\nRivets detected for", r.scream())
        # Want to get into format: ROW NAME --> EX1, EX2, EX3

        # handle editing rows
        rc = "START"
        # Iterate until User decides to be done. 
        while rc.upper() != "DONE":
            printhits = {}
            colnames = {}
            for ov in analysis[r.scream()]['detected'].keys():
                try:
                    # Key: Column name --> Value: Add example to list
                    printhits[ov[1]].append("%10s" % analysis[r.scream()]['detected'][ov])
                except KeyError:
                    # If key error, list does not exist yet, so create list with first element. 
                    # Key: Column name --> Value: Formatted List for values detected
                    printhits[ov[1]] = ["%10s" % analysis[r.scream()]['detected'][ov]]
                    # Keep track of column names for happy printing :)))))
                    colnames[ov[1]] = ov[2]
            # CLI show potential values to hit:
            print()
            for k in sorted(printhits.keys()):
                print("%10s" % colnames[k], "(Column: %2d)" % k, "-->", printhits[k][:5])
            print()

            # If there are no values in the list, then we are done with this approval.
            if len(printhits.keys()) == 0:
                rc = "DONE"
                continue

            # Otherwise, if columns still left, ask if they want to remove them. 
            ans = input("Would you like to remove any columns from the analysis (Y/N)? ")
            # Short circuit if no removal is wanted.
            if "y" not in ans and "Y" not in ans:
                rc = "DONE"
                continue
            
            # Ask for which columns to remove
            col = input("What COLUMNS would you like to remove from editing? (Type * for all columns, DONE to exit) ")
            if col.upper() == "DONE":
                rc = "DONE"
                continue

            # Input validation: make sure correct row and column
            try:
                if col != "*":
                    col = int(col)
            except ValueError:
                print("Input should be integers or *.")
                continue
            
            # Remove values from ANALYSIS
            # Get copy of list to remove values from; throws RunTimeError otherwise due to shallow copy of list
            remove = list(analysis[r.scream()]['detected'].keys()).copy()
            # If not all columns, then only remove values needed.
            if col != "*":
                remove = [k for k in remove if k[1] == col]

            # Iterate through all matches and remove them.
            for i in remove:
                analysis[r.scream()]['detected'].pop(i)
            
            # Check if all values have been removed - this is okay. 
            if len(analysis[r.scream()]['detected']) == 0:
                rivetsToRemove.append(r)
        print("----------")

    # Filter out all unused riveters.
    for rv in rivetsToRemove: 
        rr.riveters.remove(rv)
        analysis.pop(rv.scream())   
    # have access to analysis
    return analysis


#if approved, file will be processed taking in the user input from approveFile to adjust columns
    #will return the exact columns that need to be protected that will then be written in writeFile
def processFile(rr, options):
    return rr.RivetProcessor(options)
#begins process of writing the files after figuring out which should be processed from processFile
    #will return the final adjusted CSV file with the columns protected.
def writeFile(CSV, TXT):
    pass

# Runs the file only if directly called. 
if __name__ == "__main__":
    
    # Match all files given in
    files = [a for a in sys.argv if ".csv" in a]
    # Match silent mode
    silentMode = "-s" in sys.argv
    for f in files:
        main(f, silentMode)


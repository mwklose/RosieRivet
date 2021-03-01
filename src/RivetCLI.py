from Rivet import RosieRivet
import sys
import pprint

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
        ans = input("Would you like to view/edit them (Y/N)? ")
            
        # Handle viewing rows
        if "y" in ans or "Y" in ans:
            # flow if they answered yes: ask if they would like to edit any of them?
            hits = analysis[r.scream()]['detected']
            print("----------")
            print("%20s: %s" % ("(row,col,col name)", "value detected"))
            for k in sorted(hits.keys(), key=lambda e: e[1]):
                print("%20s: %s" % (k, hits[k]))
            
            # handle editing rows
            ans = input("Would you like to remove any values from the analysis (Y/N)? ")

        if "y" in ans or "Y" in ans:
            rc = "START"
            while rc.upper() != "DONE":
                row = input("What ROWS would you like to remove from editing? (Type * for all rows, DONE to exit) ")
                if row.upper() == "DONE":
                    rc = "DONE"
                    continue
                # Validate row input
                try:
                    if row != "*":
                        row = int(row)
                except ValueError:
                    print("Input should be integers or *.")
                    continue

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
                remove = analysis[r.scream()]['detected'].keys()
                if row != "*":
                    remove = [k for k in remove if k[0] == row]
                if col != "*":
                    remove = [k for k in remove if k[1] == col]

                # Iterate through all matches and remove them.
                for i in remove:
                    analysis[r.scream()]['detected'].pop(i)

                rc = input("To view rows, type 'VIEW'. If finished, type 'DONE'. ")
                if rc.upper() == "VIEW":
                    for k in sorted(analysis[r.scream()]['detected'].keys(), key=lambda e: e[1]):
                        print("%20s: %s" % (k, hits[k]))

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
    print("ARGV", sys.argv)
    print("FILES:", files, "SILENTMODE=", silentMode)
    for f in files:
        main(f, silentMode)


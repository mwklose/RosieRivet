from Rivet import RosieRivet
import sys
import pprint
import csv, json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\u001b[7m'

pp = pprint.PrettyPrinter(indent=4)

def main(file, silentMode):
    rr = RosieRivet.RosieRivet(file) # call constructor of RosieRivet

    # Analyze File
    mesaAnalysis, metaAnalysis = analyzeFile(rr)
    
    # Approve File
    options = approveFile(rr, mesaAnalysis, metaAnalysis, silentMode)

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
def approveFile(rr, mesa_analysis, meta_analysis, silentMode):
    if silentMode:
        return mesa_analysis
    
    # Flow of procedure: 
    # MetaRiveter analysis (static)
    # MesaRiveter analysis (dynamic)
    # Return adjusted MesaRiveter analhsis

    print("\n----METARIVETER ANALYSIS----")
    for r in rr.meta_riveters:
        # See if riveting even possible
        if sum(meta_analysis[r.scream()]['hits']) == 0:
            print("No detections in", bcolors.OKBLUE, r.scream(), bcolors.ENDC)
            continue

        printhits = {}
        colnames = {}
        print("\nAnalysis detected in", bcolors.OKGREEN, r.scream(), bcolors.ENDC)
        for ov in meta_analysis[r.scream()]['detected'].keys():
            try:
                # Key: Column name --> Value: Add example to list
                printhits[ov[1]].append("%10s" % meta_analysis[r.scream()]['detected'][ov])
            except KeyError:
                # If key error, list does not exist yet, so create list with first element. 
                # Key: Column name --> Value: Formatted List for values detected
                printhits[ov[1]] = ["%10s" % meta_analysis[r.scream()]['detected'][ov]]
                # Keep track of column names for happy printing :)))))
                colnames[ov[1]] = ov[2]

        # CLI show potential values to hit:
        print()
        for k in sorted(printhits.keys()):
            print(bcolors.BOLD, # Bold face
                    "%10s" % colnames[k],  # Column name
                    #"(Column:%2d; Confidence:%1.5f; Hits:%4d)" % (k, meta_analysis[r.scream()]['confidence'][k - 1], meta_analysis[r.scream()]['hits'][k - 1]), # Col num, Confidence, Number of hits
                    bcolors.ENDC, # End bold face
                    "-->", # Arrow for pretty shapes
                    printhits[k][:5]) # Print up to 5 examples
        print()

    # MesaRiveter Analysis (dynamic)

    print("\n----MESARIVETER ANALYSIS----")
    rivetsToRemove = []
    for r in rr.mesa_riveters:
        # See if riveting even possible
        if sum(mesa_analysis[r.scream()]['hits']) == 0:
            print("No rivets for", bcolors.OKBLUE, r.scream(), bcolors.ENDC)
            rivetsToRemove.append(r)
            continue

        print("\nRivets detected for", bcolors.OKGREEN, r.scream(), bcolors.ENDC)
        # handle editing rows
        rc = "START"
        # Iterate until User decides to be done. 
        while rc.upper() != "DONE":
            printhits = {}
            colnames = {}
            for ov in mesa_analysis[r.scream()]['detected'].keys():
                try:
                    # Key: Column name --> Value: Add example to list
                    printhits[ov[1]].append("%10s" % mesa_analysis[r.scream()]['detected'][ov])
                except KeyError:
                    # If key error, list does not exist yet, so create list with first element. 
                    # Key: Column name --> Value: Formatted List for values detected
                    printhits[ov[1]] = ["%10s" % mesa_analysis[r.scream()]['detected'][ov]]
                    # Keep track of column names for happy printing :)))))
                    colnames[ov[1]] = ov[2]

            # CLI show potential values to hit:
            print()
            for k in sorted(printhits.keys()):
                print(bcolors.BOLD, # Bold face
                        "%10s" % colnames[k],  # Column name
                        "(Column:%2d; Confidence:%1.5f; Hits:%4d)" % (k, mesa_analysis[r.scream()]['confidence'][k - 1], mesa_analysis[r.scream()]['hits'][k - 1]), # Col num, Confidence, Number of hits
                        bcolors.ENDC, # End bold face
                        "-->", # Arrow for pretty shapes
                        printhits[k][:5]) # Print up to 5 examples
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
            remove = list(mesa_analysis[r.scream()]['detected'].keys()).copy()
            # If not all columns, then only remove values needed.
            if col != "*":
                remove = [k for k in remove if k[1] == col]

            # Iterate through all matches and remove them.
            for i in remove:
                mesa_analysis[r.scream()]['detected'].pop(i)
            
            # Check if all values have been removed - this is okay. 
            if len(mesa_analysis[r.scream()]['detected']) == 0:
                rivetsToRemove.append(r)
        print("----------")

    # Filter out all unused riveters.
    for rv in rivetsToRemove: 
        rr.mesa_riveters.remove(rv)
        mesa_analysis.pop(rv.scream())   
    # have access to analysis
    print("--------------------")
    return mesa_analysis


#if approved, file will be processed taking in the user input from approveFile to adjust columns
#will return the exact columns that need to be protected that will then be written in writeFile
def processFile(rr, options):
    return rr.RivetProcessor(options)

#begins process of writing the files after figuring out which should be processed from processFile
#will return the final adjusted CSV file with the columns protected.
def writeFile(CSV, TXT):
    with open("out.csv", "w") as cf:
        cw = csv.writer(cf)
        cw.writerows(CSV)

    with open("out.txt", "w") as tf:
       pprint.PrettyPrinter(indent=4, stream=tf).pprint(TXT)

    return

# Runs the file only if directly called. 
if __name__ == "__main__":
    
    # Match all files given in
    files = [a for a in sys.argv if ".csv" in a or ".txt" in a]
    # Match silent mode
    silentMode = "-s" in sys.argv
    for f in files:
        main(f, silentMode)

# Add input values for DateFormatRiveter????

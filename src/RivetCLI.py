from Rivet import RosieRivet
import sys

def main(file):
    print("In main with", file)
    rr = RosieRivet.RosieRivet(file) # call constructor of RosieRivet
    # Analyze File
    myAnalysis = analyzeFile(rr)
    # Approve File
    myCSV, options = approveFile(rr, myAnalysis)
    # Process File
    rivetCSV, rivetTXT = processFile(rr, myCSV, options)
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
def approveFile(rr, analysis):
    print("APPROVE FILE: ", analysis)
    return "CSV", "OPTIONS"
    
#if approved, file will be processed taking in the user input from approveFile to adjust columns
    #will return the exact columns that need to be protected that will then be written in writeFile
def processFile(rr, myCSV, options):
    print("PROCESS FILE: ", myCSV, options)
    rr.RivetProcessor(None, None)
    return "RIVETCSV", "RIVETTXT"
#begins process of writing the files after figuring out which should be processed from processFile
    #will return the final adjusted CSV file with the columns protected.
def writeFile(CSV, TXT):
    pass


# Runs the file only if directly called. 
if __name__ == "__main__":
    # Match all files in the system
    files = [a for a in sys.argv if ".csv" in a]
    silentMode = "-s" in sys.argv
    print("ARGV", sys.argv)
    print("FILES:", files, "SILENTMODE=", silentMode)
    data_file = sys.argv[len(sys.argv) - 1]
    for f in files:
        main(f)

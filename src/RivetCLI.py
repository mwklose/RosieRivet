from RosieRivet import RosieRivet
import sys

def main():
    print("In main.")
    rr = RosieRivet() # call constructor of RosieRivet
    # Analyze File
    myAnalysis = analyzeFile(rr)
    # Approve File
    myCSV, options = approveFile(rr, myAnalysis)
    # Process File
    rivetCSV, rivetTXT = processFile(rr, myCSV, options)
    # Write File
    print(rivetCSV, rivetTXT)
    return

def analyzeFile(rr):
    print("ANALYZE FILE")
    return "ANALYSIS"

def approveFile(rr, analysis):
    print("APPROVE FILE: ", analysis)
    return "CSV", "OPTIONS"

def processFile(rr, myCSV, options):
    print("PROCESS FILE: ", myCSV, options)
    rr.RivetProcessor(None, None)
    return "RIVETCSV", "RIVETTXT"

if __name__ == "__main__":
    print(sys.argv)
    print("CHECK ARGS:", "-m" in sys.argv)
    data_file = sys.argv[len(sys.argv) - 1]
    main()
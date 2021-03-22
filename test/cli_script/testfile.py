import unittest, csv, sys
sys.path.append("../../src/")
from Rivet import RosieRivet
import RivetCLI

NUM_FILES = 7

class FlowMethodTest(unittest.TestCase):
    # EEnsures that the flow exists and proves correct. 
    def test_fullsystem(self):
        for i in range(NUM_FILES):
            filename = "test" + str(i + 1) + ".csv"
            rrr = RosieRivet.RosieRivet(filename)
            # Analyze file
            d = rrr.RivetFileAnalyzer()
            # Get output from file as Row/Col pointer
            out, options = rrr.RivetProcessor(d)
            # Open the expected output file
            filename2 = "test" + str(i + 1) + "_expected.csv"
            with open(filename2) as f:
                csvreader = csv.reader(f)

                # Assert lines are fixed as intended
                for r in out:
                    s = next(csvreader)
                    self.assertEqual(r, s, "Error in file: " + str(i+1))
        return

    # Ensures that all the desired keys exist for each of the riveters. 
    def test_rivetkeys(self):
        for i in range(NUM_FILES):
            filename = "test" + str(i + 1) + ".csv"
            rrr = RosieRivet.RosieRivet(filename)
            # Analyze file
            d = rrr.RivetFileAnalyzer()
            # Check for each of the riveters, an analysis exists:
            for riveter in rrr.riveters:
                # Ensure that DETECTED field exists in analysis
                try:
                    d[riveter.scream()]["detected"]
                except KeyError:
                    self.fail(riveter.scream() + " has no 'detected' in analysis")
                # Ensure that CONFIDENCE field exists in analysis
                try:
                    d[riveter.scream()]["confidence"]
                except KeyError:
                    self.fail(riveter.scream() + " has no 'confidence' in analysis")
                # Ensure that HITS field exists in analysis
                try:
                    d[riveter.scream()]["hits"]
                except KeyError:
                    self.fail(riveter.scream() + " has no 'hits' in analysis")
     
    def test_RivetCLI(self):
        for i in range(NUM_FILES):
            filename = "test" + str(i + 1) + ".csv"
            RivetCLI.main(filename, True)

if __name__ == "__main__":
    unittest.main()
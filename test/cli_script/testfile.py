from Rivet import RosieRivet
import unittest, csv

class FlowMethodTest(unittest.TestCase):
    def test_fullsystem(self):
        for i in range(7):
            filename = "test" + str(i+1) + ".csv"
            rrr = RosieRivet.RosieRivet(filename)
            # Analyze file
            d = rrr.RivetFileAnalyzer()
            # Get output from file as Row/Col pointer
            out = rrr.RivetProcessor(d)
            # Open the expected output file
            filename = "test" + str(i+1) + "_expected.csv"
            with open(filename) as f:
                csvreader = csv.reader(f)

                # Assert lines are fixed as intended
                for r in out:
                    s = next(csvreader)
                    print(r, s)
                    self.assertTrue(r == s)
        return

    def test_rivetkeys(self):
        pass

    

if __name__ == "__main__":
    unittest.main()
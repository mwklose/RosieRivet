import unittest, csv, sys
sys.path.append("../../src/")
from Rivet import RosieRivet

class FlowMethodTest(unittest.TestCase):
    def test_fullsystem(self):
        self.assertTrue(True)
        #for i in range(7):
        filename = "test1.csv"
        rrr = RosieRivet.RosieRivet(filename)
        # Analyze file
        d = rrr.RivetFileAnalyzer()
        print(d)
        # Get output from file as Row/Col pointer
        out, options = rrr.RivetProcessor(d)
        # Open the expected output file
        filename2 = "test1_expected.csv"
        with open(filename2) as f:
            csvreader = csv.reader(f)

            # Assert lines are fixed as intended
            for r in out:
                s = next(csvreader)
                print(r, s)
                self.assertEquals(r, s)
            f.close()
        return

    def test_rivetkeys(self):
        pass

    

if __name__ == "__main__":
    unittest.main()
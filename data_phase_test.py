import unittest
from data_phase import readFile

class TestData(unittest.TestCase):
    def test_sylk_no_dutch(self):
        self.info = readFile("pattern1.csv")
        assert self.info["DUTCHSEP"] == ",", "fail dutch"
        assert self.info["SYLK"] == True, "fail sylk"
        assert self.info["ROWS"] == 8, "fail rows"
        assert self.info["COLUMNS"] == 7, "fail columns"
        assert len(self.info["INJECTION"]) == 7, "fail injection"
        assert len(self.info["NOTADATE"]) == 2, "fail not a date"
        assert len(self.info["BIGNUM"]) == 11, "fail big num"

    def test_no_sylk_dutch(self):
        self.info = readFile("pattern2.csv")
        assert self.info["DUTCHSEP"] == ";", "fail dutch"
        assert self.info["SYLK"] == False, "fail sylk"
        assert self.info["ROWS"] == 4, "fail rows"
        assert self.info["COLUMNS"] == 5, "fail columns"
        assert len(self.info["INJECTION"]) == 0, "fail injection"
        assert len(self.info["NOTADATE"]) == 0, "fail not a date"
        assert len(self.info["BIGNUM"]) == 0, "fail big num"

    def test_sylk_dutch(self):
        self.info = readFile("pattern.csv")
        assert self.info["DUTCHSEP"] == ",", "fail dutch"
        assert self.info["SYLK"] == False, "fail sylk"
        assert self.info["ROWS"] == 4, "fail rows"
        assert self.info["COLUMNS"] == 5, "fail columns"
        assert len(self.info["INJECTION"]) == 0, "fail injection"
        assert len(self.info["NOTADATE"]) == 2, "fail not a date"
        assert len(self.info["BIGNUM"]) == 0, "fail big num"
        assert self.info["NOTADATE"][0]["row_no"] == 1, "fail content row"
        assert self.info["NOTADATE"][0]["col_no"] == 1, "fail content row"
        assert self.info["NOTADATE"][1]["row_no"] == 2, "fail content row"
        assert self.info["NOTADATE"][1]["col_no"] == 2, "fail content row"

if __name__ == "__main__":
    unittest.main()
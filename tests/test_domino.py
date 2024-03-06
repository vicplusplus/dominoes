import unittest
from src.domino import Domino


class TestDomino(unittest.TestCase):
    def setUp(self):
        self.domino = Domino(5, 3)

    def test_init(self):
        self.assertEqual(self.domino.sides[0]["value"], 5)
        self.assertEqual(self.domino.sides[1]["value"], 3)
        self.assertIsNone(self.domino.sides[0]["domino"])
        self.assertIsNone(self.domino.sides[1]["domino"])

    def test_f_repr(self):
        self.assertEqual(self.domino.f_repr(), "[5|3]")
        self.assertEqual(self.domino.f_repr(reverse=True), "[3|5]")

    def test_value(self):
        self.assertEqual(self.domino.value(), 8)

    def test_connect(self):
        other_domino = Domino(2, 1)
        self.domino.connect(other_domino, 1, 0)
        self.assertEqual(self.domino.sides[1]["domino"], other_domino)
        self.assertEqual(other_domino.sides[0]["domino"], self.domino)


if __name__ == "__main__":
    unittest.main()

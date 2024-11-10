import unittest
import tests_12_2

test1 = unittest.TestSuite()
test1.addTest(unittest.TestLoader().loadTestsFromTestCase(tests_12_2.TournamentTest))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(test1)


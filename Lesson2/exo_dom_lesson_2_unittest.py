# UNIT TESTS for exo_dom_lesson_2.py
#
#

import unittest
import exo_dom_lesson_2
    
class ExoDomLesson2Tests(unittest.TestCase):
    def testExtract_ABDC_Indicators(self):
        self.assertEqual(exo_dom_lesson_2.extract_ABDC_Indicators(2015) , [2322, 2322, 2354, 2354, 914, 914, 788, 788])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
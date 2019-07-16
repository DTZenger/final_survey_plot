import unittest
import final_survey_plot as fsp


class MyTestCase(unittest.TestCase):

    def test_of_structure_of_array(self):
        ss = fsp.StaveSurvey('./test-files/1_0.csv',
                             './test-files/stub_ideals.csv')
        self.assertEqual(len(ss.separate_module), 2)

    def test_of_finding_fid(self):
        ss = fsp.StaveSurvey('./test-files/1_0.csv', './test-files/fid_1_0.csv')
        self.assertEqual(ss.fiducial_mark, 'F')

    def test_of_2nd_module_x_failing_with_40_tolerance(self):
        ss = fsp.StaveSurvey('./test-files/stub_ideals.csv', './test-files/mixed_1.csv')
        passed_modules, total_failed = ss.find_if_passing(tolerance=40)

        self.assertTrue(passed_modules[0][0], msg='Module 1 x shown False')
        self.assertTrue(passed_modules[0][1], msg='Module 1 y shown False')
        self.assertFalse(passed_modules[1][0], msg='Module 2 x shown True')
        self.assertTrue(passed_modules[1][1], msg='Module 2 y shown False')

        self.assertEqual(total_failed[0], 1, msg='x is not shown with only 1 failure')
        self.assertEqual(total_failed[1], 0, msg='y has at least 1 failure shown')

    def test_of_2nd_module_x_failing_with_7_tolerance(self):
        ss = fsp.StaveSurvey('./test-files/stub_ideals.csv', './test-files/mixed_1.csv')
        passed_modules, total_failed = ss.find_if_passing(tolerance=7)

        self.assertTrue(passed_modules[0][0], msg='Module 1 x shown False')
        self.assertTrue(passed_modules[0][1], msg='Module 1 y shown False')
        self.assertFalse(passed_modules[1][0], msg='Module 2 x shown True')
        self.assertFalse(passed_modules[1][1], msg='Module 2 y shown True')

        self.assertEqual(total_failed[0], 1, msg='x is not shown with only 1 failure')
        self.assertEqual(total_failed[1], 1, msg='y is not shown with only 1 failure')


if __name__ == '__main__':
    unittest.main()

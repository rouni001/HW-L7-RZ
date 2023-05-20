from django.test import TestCase
from benford.models import BenfordLawFitnessAnalyzer, BENFORD_EXP_DIST
from benford.utils import get_lead_digits_frequencies
from pathlib import Path

import numpy as np
import os


DIR = Path(__file__).parent


class BenfordLawFitnessAnalyzerTest(TestCase):
    def test_base_case_rejected(self):
        """Test when the observed distribution is uniform: Frequency for each digit is 100/9 %.
        So this test must fail: the null hypothesis is rejected.
        """
        analyzer_case = BenfordLawFitnessAnalyzer([100.0/9]*9)
        self.assertTrue(analyzer_case.is_null_hypothesis_rejected())

    def test_base_case_accepted(self):
        """Test when the observed distribution is exactly the Benford's uniform.
        So this test must pass: the null hypothesis is accepted.
        """
        analyzer_case = BenfordLawFitnessAnalyzer(BENFORD_EXP_DIST)
        self.assertFalse(analyzer_case.is_null_hypothesis_rejected())


class UtilsTest(TestCase):
    def test_base_case_exception_wrong_values(self):
        """Test when the last column of the user file is full of string values instead of integers.
        So this test must capture an exception.
        """   
        with open(os.path.join(DIR, "tests/data/input_file_1.formatted.txt"), "rb") as fin:
            with self.assertRaises(Exception):
                get_lead_digits_frequencies(fin)
            
    def test_base_case_exception_wrong_value(self):
        """Test when the last column contains only integers except for one row.
        So this test must capture an exception.
        """         
        with open(os.path.join(DIR, "tests/data/input_file_2.formatted.txt"), "rb") as fin:
            with self.assertRaises(Exception):
                get_lead_digits_frequencies(fin)

    def test_base_case_exception_missing(self):
        """Test when the last column contains a missing value.
        So this test must capture an exception.
        """ 
        with open(os.path.join(DIR, "tests/data/input_file_3.formatted.txt"), "rb") as fin:
            with self.assertRaises(Exception):
                get_lead_digits_frequencies(fin)

    def test_base_case_success_small_distr(self):
        """Test when the last column of the user file contains integers as expected.
        The user file used here has a very limited number of observations (8).
        The number of observations found and the frequencies of lead digits must be returned.
        This test must succeed if the returned values for correct.
        """ 
        with open(os.path.join(DIR, "tests/data/input_file_4.formatted.txt"), "rb") as fin:
            (num_obs, obs_distr) = get_lead_digits_frequencies(fin)

        self.assertEqual(num_obs, 8)
        self.assertEqual(len(obs_distr), 9)
        self.assertEqual(obs_distr, [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 0])

    def test_base_case_success_medium_distr(self):
        """Test when the last column contains integers as expected.
        The user file used here has a limited number of observations (30).
        The number of observations found and the frequencies of lead digits must be returned.
        This test must succeed if the returned values for correct.
        """ 
        with open(os.path.join(DIR, "tests/data/input_file_5.formatted.txt"), "rb") as fin:
            (num_obs, obs_distr) = get_lead_digits_frequencies(fin)

        self.assertEqual(num_obs, 30)
        self.assertEqual(len(obs_distr), 9)
        expected_obs_distr = [
            36.666666666666664, 
            36.666666666666664, 
            6.666666666666667, 
            3.3333333333333335, 
            3.3333333333333335, 
            3.3333333333333335, 
            3.3333333333333335, 
            3.3333333333333335, 
            3.3333333333333335
        ]
        distance = np.linalg.norm(np.array(expected_obs_distr) - np.array(obs_distr))
        self.assertTrue(distance < 10E-6, "Distance found: " + str(distance)) 

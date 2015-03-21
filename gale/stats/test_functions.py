'''
File: test_functions.py
Author: Adam Pah
Description: 
py.test tests for the functions script
'''
from __future__ import division
import pytest
import numpy as np
import functions as statfunc

class TestGini:
    '''
    Covers the gini function
    '''
    def test_gini_calculation(self):
        '''
        Make sure that the gini function works correctly
        '''
        #Check the uneven condition
        setmax = [0.5, 0.125, 0.125, 0.125, 0.125]
        gini_answer = statfunc.gini(setmax)
        assert gini_answer == 0.29999999999999993
        #Check the even condition
        setzero = [0.25, 0.25, 0.25, 0.25]
        gini_answer = statfunc.gini(setzero)
        assert gini_answer == 0.0

    def test_integer_conversion(self):
        '''
        Make sure that the gini function converts a set
        of integers gt one are converted to a frequency
        '''
        #Check the uneven condition
        setmax = [3, 1, 1, 1]
        gini_answer = statfunc.gini(setmax)
        assert gini_answer == 0.25
        #Check the even condition
        setzero = [1, 1, 1, 1]
        gini_answer = statfunc.gini(setzero)
        assert gini_answer == 0.0

    def test_lt_one_exit(self):
        '''
        Make sure that the gini function ends with an exit
        when frequencies that do not equal 1 are inputted
        '''
        freqdata = [0.33, 0.2]
        with pytest.raises(SystemExit):
            statfunc.gini(freqdata)

    def test_zero_sum_exit(self):
        '''
        Make sure that the gini function ends with an exit
        when a zero sum is entered
        '''
        freqdata = [0, 0]
        with pytest.raises(SystemExit):
            statfunc.gini(freqdata)

class TestCalcZ:
    '''
    Tests the calc_z function
    '''
    def test_zcalc(self):
        '''
        Tests the calculation with all nonzero values
        '''
        obs, exp = (4, 2), (6, 1)
        #calculate the answer
        answer = (4-6)/np.sqrt(5)
        #Run the function
        z = statfunc.calc_z(obs, exp)
        assert z == answer

    def test_zcalc_zero_se_sided(self):
        '''
        Tests to make sure that one zero does not error out
        '''
        obs, exp = (4, 2), (6, 0)
        z = statfunc.calc_z(obs, exp)
        assert z == -1

    def test_zcalc_zero_se_all(self):
        '''
        Tests the edge case of both SEs being zero
        '''
        obs, exp = (8, 0), (9, 0)
        z = statfunc.calc_z(obs, exp)
        assert z == np.inf

class TestFoldChange:
    '''
    Tests the fold_change function and the deprecation of baseline_normalizer.
    '''
    obs = 8
    obs_list = [8, 16, 20]
    exp = 4

    def test_baseline_normalizer(self, capsys):
        '''
        Tests that he baseline normalizer function works and gives an 
        error message to sys.stderr
        '''
        #Run teh deprecated function
        norm = statfunc.baseline_normalizer(self.obs, self.exp)
        #Check the calculation
        assert norm == self.obs/self.exp
        #Capture the messages
        out, err = capsys.readouterr()
        #The message is:
        m = "WARNING: The function name 'baseline_normalizer' is deprecated.\n"
        m += "Please use the function name 'fold_change' in the future\n"
        assert m == err

    def test_fold_change_value(self):
        '''
        Tests that the fold_change function will work with singular values
        '''
        #Run teh deprecated function
        norm = statfunc.fold_change(self.obs, self.exp)
        #Check the calculation
        assert norm == self.obs/self.exp

    def test_fold_change_list(self):
        '''
        Tests that the function works with a list of values
        '''
        #Run teh deprecated function
        norm = statfunc.fold_change(self.obs_list, self.exp)
        #Check the calculation
        answer = [i/self.exp for i in self.obs_list]
        assert norm == answer

    def test_zero_exp_exception(self):
        '''
        Tests to make sure that it errors on an expected value of zero
        '''
        with pytest.raises(SystemExit):
            statfunc.fold_change(self.obs, 0)

class TestZScoreToPValue:
    '''
    Tests the zscore_to_pvalue function
    '''
    zScores = [-3, -2, -1, 0, 1, 2, 3]
    pValues = [0.00134989803163, 0.0227501319482, 0.158655253931, 0.5, \
               0.841344746069, 0.977249868052, 0.998650101968]

    def test_conversions(self):
        '''
        Tests the conversions 
        '''
        for zScore, pValue in zip(self.zScores, self.pValues):
            pVal = statfunc.zscore_to_pvalue(zScore)
            #Test to the 8th decimal
            answer_str = "%.8f" % pVal
            given_str = "%.8f" % pValue
            assert answer_str == given_str

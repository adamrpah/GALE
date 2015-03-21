'''
File: test_conversions.py
Author: Adam Pah
Description: 
py.test test ensemble
'''
import pytest
import conversions as conv

class TestConvertTimeseries:
    '''
    Covers the convert_timeseries_to_intervalseries function
    '''
    timeseries = [[0, 2], [2, 3], [5, 3]]

    def test_basic(self):
        '''
        Timeseries conversion test.
        '''
        #Set up the answer
        intervalseries = [[0, 2], [1, 3]]
        #Get the intervalseries
        test_intervals = conv.convert_timeseries_to_intervalseries(self.timeseries)
        #Just make sure that these things aren't the same
        assert intervalseries == test_intervals

    def test_yaxis_only(self):
        '''
        Timeseries conversion test with the yaxis only
        '''
        #Set up the answer
        intervalseries = [2, 3]
        #Get the intervalseries
        test_intervals = conv.convert_timeseries_to_intervalseries(self.timeseries, yaxis_only=True)
        #Just make sure that these things aren't the same
        assert intervalseries == test_intervals

    def test_negative_bounds(self):
        '''
        Test to make sure that system exit happens
        '''
        #Load up the data
        timeseries = [[0, 2], [-2, 3], [4, 3]]
        #Check for the system exit
        with pytest.raises(SystemExit):
            conv.convert_timeseries_to_intervalseries(timeseries, yaxis_only=True)

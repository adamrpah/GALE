'''
File: conversions.py
Author: Adam Pah
Description: 
Converts a time series between formats
'''
import sys
sys.path.append('../')
import gale.general.errors as gerr

def convert_timeseries_to_intervalseries(timeseries, yaxis_only=False):
    '''
    Will note accept any negative intervals (since that shouldn't be possible
    input:
        timeseries: [[numeric_date_from_start, arbitrary value of interest], []....
        yaxis_only: False, by default. if True then the return is [20, 6, ...]
    output:
        intervalseries: [[0, 20], [1, 6], ...

    Outputs the orderd series of gaps between dates
    '''
    intervalseries = []
    for i, dtpoint in enumerate(timeseries[:-1]):
        #Unpack the dates
        idate = dtpoint[0]
        jdate = timeseries[i+1][0]
        #Perform the calculation
        interval = jdate - idate
        #Go through the options, break if it is negative
        if interval < 0:
            m = 'Negative interval detected, this should not be an out of order timeseries'
            gerr.generic_error_handler(message = m)
        elif yaxis_only:
            intervalseries.append(interval)
        else:
            intervalseries.append([i, interval])
    return intervalseries

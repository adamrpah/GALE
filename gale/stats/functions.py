'''
Generic statistical functions.
'''
from __future__ import print_function
from math import erf, sqrt
import sys
import gale.general.errors as gerr

def gini(data):
    '''
    Calculates the gini coefficient for a given dataset.
    input:
        data- list of values, either raw counts or frequencies. 
              Frequencies MUST sum to 1.0, otherwise will be transformed to frequencies
              If raw counts data will be transformed to frequencies.
    output:
        gini- float, from 0.0 to 1.0 (1.0 most likely never realized since it is
              only achieved in the limit)
    '''
    def _unit_area(height, value, width):
        '''
        Calculates a single bars area.
        Area is composed of two parts:
            The height of the bar up until that point
            The addition from the current value (calculated as a triangle)
        input:
            height: previous bar height or sum of values up to current value
            value: current value
            width: width of individual bar
        output:
            bar_area: area of current bar
        '''
        bar_area = (height * width) + ((value * width) / 2.)
        return bar_area
    
    #Fair area will always be 0.5 when frequencies are used
    fair_area = 0.5
    #Check that input data has non-zero values, if not throw an error
    datasum = float(sum(data))
    if datasum==0:
        m = 'Data sum is 0.0.\nCannot calculate Gini coefficient for non-responsive population.'
        gerr.generic_error_handler(message=m)
    elif datasum < 0.99:
        m = 'Data sum is frequencies and less than 1.0.'
        gerr.generic_error_handler(message=m)
    #If data does not sum to 1.0 transform to frequencies
    elif datasum > 1.0:
        data = [x/datasum for x in data]
    #Calculate the area under the curve for the current dataset
    data.sort()
    width = 1/float(len(data))
    height, area = 0.0, 0.0
    for value in data:
        area += _unit_area(height, value, width)
        height += value
    #Calculate the gini
    gini = (fair_area-area)/fair_area
    return gini

def calc_z(obs, exp):
    '''
    Calculates the z for two independent quantities as:
    z = (obs - exp)/se_diff
    where se_diff is
    se_diff = sqrt(a**2 + b**2)
    with a being the SE for the first quantity and b the SE for the second quantity
    If se's are both zero then it returns infinity from numpy
    Input:
        obs - Tuple containing (quantity, SE)
        exp - Tuple containing (quantity, SE)
    Output:
        z - float
    '''
    import numpy as np
    se_diff = np.sqrt(obs[1]**2 + exp[1]**2)
    if se_diff != 0:
        z = (obs[0] - exp[0])/se_diff
    else:
        z = np.inf
    return z

def baseline_normalizer(obs, exp):
    '''
    Deprecated name
    '''
    m = "WARNING: The function name 'baseline_normalizer' is deprecated.\n"
    m += "Please use the function name 'fold_change' in the future"
    print(m, file=sys.stderr)
    #Run the function anyways
    norm = fold_change(obs, exp)
    return norm

def fold_change(obs, exp):
    '''
    Rescales the observation (either a single value or list) by the expected value
    Cannot accept zero as the expected value
    input:
        obs -- int/float or list of int/floats
        exp -- int/float
    output:
        norm -- int/float or list of int/floats
    '''
    if exp == 0:
        m = "Cannot accept zero as an expected value"
        gerr.generic_error_handler(message = m)
    elif type(obs)==list:
        norm = [ival/float(exp) for ival in obs]
    else:
        norm = obs/float(exp)
    return norm

def zscore_to_pvalue(z):
    '''
    Converts a zscore to a pvalue
    input:
        - zscore
    output:
        - pvalue
    '''
    p = 0.5 * (1 + erf(z/sqrt(2)))
    return p

###################
# Statsmodels
###################

def sm_summary_restrict(summary, dropFE=False, alpha=None):
    '''
    Drops fixed effects or nonsignificant predictors. Can do both simultaneously
    input:
        * summary - statsmodels summary() object (i.e. smf.ols(formula).fit().summary() )
        * dropFE - True/False, default is False - drop fixed effects (any predictor with 'C(' in name
        * alpha - Float, alpha value to drop parameters at (i.e. if predictor is 0.08 and alpha=0.05, predictor will not be included) 
    output:
        * summary - statsmodels summary() object
    '''
    from statsmodels.iolib.table import SimpleTable
    tblheader = summary.tables[1].data[0]
    tbldata = []
    for r in summary.tables[1].data[1:]:
        if dropFE == True:
            if 'C(' in r[0]:
                continue
            else:
                pass
        if alpha != None:
            if float(r[-2]) < alpha:
                tbldata.append(r)
        else:
            tbldata.append(r)
    #Add back in our restricted table
    summary.tables[1] = SimpleTable(tbldata, tblheader)
    return summary

def write_statsmodels_glm_result(res, fname):
    '''
    Writes a statsmodels GLM result object to a latex table in a given filename
    input:
        * res - statsmodels results object
        * fname - filename to write the resulting latex table to
    output:
        None
    '''
    import re
    latex = res.summary().as_latex()
    latex = '\\begin{tabular}{lc}'.join( latex.split('\\begin{tabular}{lclc}') )
    top, start_middle = latex.split('\\toprule\n')
    middle, bottom_one, bottom_two = start_middle.split('\\bottomrule\n')
    #Split the middle on lines, then split each line at &
    half_lines = []
    for line in middle.split('\n'):
        if '&' in line:
            half_lines.append( ' & '.join( line.split(' & ')[2:] ) )
    #Add in the AIC/BIC
    template_line = '\\textbf{  %s:           } &   %d   \\\\'
    half_lines.append( template_line % ('AIC', res.aic) )
    half_lines.append( template_line % ('BIC', res.bic) )
    #Reconstruct
    middle = '\n'.join(half_lines) + '\n'
    latex = top + '\\toprule\n' + middle + '\\bottomrule\n' + bottom_one + '\\bottomrule\n' + bottom_two
    #Change out the '_' titles so i tdoesn't break latex
    if '_' in latex:
        latex = re.sub('_', ' ', latex)
    with open(fname, 'w') as f:
        print(latex, file = f)

def write_statsmodels_ols_result(res, fname):
    '''
    Writes a statsmodels OLS result object to a latex table in a given filename
    input:
        * res - statsmodels results object
        * fname - filename to write the resulting latex table to
    output:
        None
    '''
    latex = res.summary().as_latex()
    splatex = latex.split('\\begin{tabular}{lclc}')
    latex = splatex[0] + '\\begin{tabular}{lc}' + splatex[1] + '\\begin{tabular}{lclc}' + splatex[2]
    top, start_middle = latex.split('\\toprule\n')
    middle, bottom_one, bottom_two, bottom_three = start_middle.split('\\bottomrule\n')
    #Split the middle on lines, then split each line at &
    half_lines = []
    for line in middle.split('\n'):
        if '&' in line:
            half_lines.append( ' & '.join( line.split(' & ')[2:] ) )
    #Reconstruct
    middle = '\n'.join(half_lines) + '\n'
    latex = top + '\\toprule\n' + middle + '\\bottomrule\n' + bottom_one + '\\bottomrule\n' + bottom_two + '\\bottomrule\n' + bottom_three
    if '_' in latex:
        latex = re.sub('_', ' ', latex)
    with open(fname, 'w') as f:
        print(latex, file = f)

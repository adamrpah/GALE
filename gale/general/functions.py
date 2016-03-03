def paired_list_generator(tlist):
    '''
    Takes a list and returns a list of the iterative element pairs
    input:
        list
    output:
        paired_list
    '''
    paired_list =[]
    for i in range(len(tlist)-1):
        paired_list.append([tlist[i], tlist[i+1]])
    return paired_list

def tex_sanitizer(tstr):
    '''
    Takes in a string and sanitizes it for LaTeX
    '''
    import re
    tstr = re.sub('_', ' ', tstr)
    return tstr

def labelifier(tstr):
    '''
    Turns a unix-like string to a human readable one for an axis label
    input:
        - tstr (str)
    output:
        - tstr (str)
    '''
    import re
    tstr = re.sub('_', ' ', tstr)
    tstr = re.sub('-', ' ', tstr)
    tstr = ' '.join(map(lambda x: x.capitalize(), tstr.split(' ')))
    return tstr

def pair_setter(tlist, concat='?'):
    '''
    Takes a list of lists or tuples and makes the set
    input:
        - tlist - list of lists to concat
        - concat - what to join sublists by, default is ?
    output:
        - ulist - unique list of entries
    '''
    str_tlist = []
    for entry in tlist:
        sentry = [str(ientry) for ientry in entry]
        str_tlist.append('?'.join(sentry))
    #Set the list
    strings = list( set( str_tlist ) )
    #unpack it
    ulist = []
    for sentry in strings:
        ulist.append(strings.split('?'))
    return ulist


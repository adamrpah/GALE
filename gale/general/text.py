def text_sanitizer(tstr):
    '''
    Strips out all syntax and punctuation leaving only alphanumerical characters
    input:
        - tstr (str)
    output:
        - new_str (str)
    '''
    import re
    pattern = re.compile('[\W_]+')
    new_str = pattern.sub('', tstr)
    return new_str

def deadspace_killer(string_list):
    '''
    Removes all whitespace entries in a list of strings
    input:
        - string_list 
    output:
        - cleaned_list
    '''
    for ws_element in ['', ' ']:
        string_list = [x for x in string_list if x != ws_element]
    return string_list

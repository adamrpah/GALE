def parse_infomap(comfile, netfile='', hierarchy=True):
    '''
    Parses an infomap community file. 
    Returns the (now) standard mod2node and node2mod dictionaries
    If recursion is wanted then the will ...
    ****Network features still missing*****
    inputs:
        comfile- name of infomap community file
        netfile- network file, will have more information
        hierarchy- boolean, toplevel or all levels.
    outputs:
        mod2node - dictionary with module class
    '''
    import sys
    try:
        import networkx as nx
    except ImportError:
        hierarchy = False
        print >> sys.stderr, "NetworkX is not available" 
        print >> sys.stderr, "Any network features of the modules will not be calculated"
    import gale.general.errors as gerr


    class Module(object):
        '''
        The module class
        Contains information related to sub-modules, such as sub-hierarchy,
        connecting modules, connecting partners, size, and nodes
        '''
        def __init__(self):
            ##Level - 0, 1, 2, 3
            self.level = None
            ##Hierarchy 
            self.children = False
            self.submodules = []
            ##Size related
            self.nodes = []
            self.size = None
            ##Network characteristics
            #module:link strength
            self.connect_modules = {}
            #node: outside_node
            self.connect_nodes = {}

        def attribute_generators(self):
            self.size = len(self.nodes)

    def _reader(fname):
        '''
        Read the input file, ignore comments that are #
        '''
        data = []
        for line in open(comfile).readlines():
            if line[0]=='#':
                #Comment
                pass
            elif line=='' or line==' ' or line=='\t' or line=='\n':
                #Blank line
                pass
            else:
                sline = line.split()
                #First part is modules, then numeric, then node name
                modlisting = sline[0].split(':')
                del modlisting[-1]
                #Kill the double quotes, join anything split with aspace in the node name
                #nodename = ' '.join(sline[2:])[1:-1]
                nodename = sline[-1]
                data.append([modlisting, nodename])
        return data
    
    #Reference variables
    mod2node = {}
    node2mod = {}
    #Read in the community data
    comdata = _reader(comfile)
    for mods, node in comdata:
        #Start with the easy part first
        if node in node2mod:
            m='Duplicitous node identifier'
            gerr.generic_error_handler(message=m)
        #CHeck on hierarchy
        if hierarchy == True:
            modname = '-'.join(mods)
        else:
            modname = mods[0]
        #Add the node2mod
        node2mod[node] = modname
        #Go through the modules in the listing
        for i in range(len(mods)):
            tmod = '-'.join(mods[:i+1])
            #Start the class
            if tmod not in mod2node:
                mod2node[tmod] = Module()
                mod2node[tmod].level = i
                #Check if there are children
                if len(mods) > (i+1):
                    mod2node[tmod].children = True
                    mod2node[tmod].submodules.append(mods[i+1])
            #Class upkeeping
            mod2node[tmod].nodes.append(node)
    #class upkeeping
    for module in mod2node:
        mod2node[module].attribute_generators()
    return mod2node, node2mod

def process_partition(fname):
    '''
    process a partion file.
    A partition file is structured as:
        key --- value value value
    input:
        fname: filename of partition file
    output:
        tdict: matched as dict[key] = [val, val, val]     
    '''
    indata = [l.strip().split(' --- ') for l in open(fname).readlines()]
    tdict = dict([(l[0], l[1].split()) for l in indata])
    return tdict

def read_json_netfile(infile):
    '''
    Reads in a JSON network
    input:
        infile name
    output:
        Networkx graph object
    '''
    from networkx.readwrite import json_graph
    G = json_graph.loads(open(infile).read())
    return G

def write_json_netfile(G, outfile):
    '''
    Writes a JSON network
    input:
       G: NetworkX graph object 
       outfile: name of output file
    Returns:
        Nothing
    '''
    from networkx.readwrite import json_graph
    import json
    gdata = json_graph.node_link_data(G)
    gstr = json.dumps(gdata)
    with open(outfile, 'w') as wfile:
        print >> wfile, gstr
        wfile.close()

def file_reader(infile, weighted=False):
    '''
    Arbitrary function to determine network file type and parse according to rules
    input:
        filename
    output:
        networkx graph
    '''
    import os
    import networkx as nx
    fname, ext = os.path.splitext(infile)
    if ext=='json':
        G = read_json_netfile(infile)
    else:
        if weighted:
            G = nx.read_edgelist(infile, data=(('weight',float),))
        else:
            G = nx.read_edgelist(infile)
    return G





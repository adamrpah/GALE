'''
Calculates node properties
'''
from __future__ import division
import numpy as np
import networkx as nx

class Node(object):
    '''
    The generalized node object
    '''
    def __init__(self, name):
        '''
        Basic analytical properties
        '''
        self.name = name
        self.integer = None
        self.role = None
        self.participation = None
        self.mod_degree = None
        self.degree = None
        self.betweenness = None

def calculate_betweenness_zscore(G, node2module):
    '''
    Calculates the betweeenness z-Score
    input:
        * G - networkx graph object
        * node2module - node to module translation dictionary
    output:
        * betweennes_zscore_dict - node to betweenness mapping
    '''
    bcdict = nx.betweenness_centrality(G)
    #Calculate the mean and standard deviation
    mean = np.mean(bcdict.values())
    std = np.std(bcdict.values())
    #Calculate the z-scores
    betweenness_zscore_dict={}
    for node in bcdict:
        betweenness_zscore_dict[node]=(bcdict[node]-mean)/std
    return betweenness_zscore_dict

def calculate_degree_zscore(G, node2module):
    '''
    Calculates the degree z-Score
    input:
        * G - networkx graph object
        * node2module - node to module translation dictionary
    output:
        * degree_zscore_dict - node to betweenness mapping
    '''
    #Get node degrees
    degree_dict={}
    for node in G.nodes():
        degree_dict[node] = G.degree(node)
    #Calculate the mean and standard deviation
    mean = numpy.mean(degree_dict.values())
    std = numpy.std(degree_dict.values())
    #Calcualte teh z-score
    degree_zscore_dict={}
    for node in degree_dict:
        degree_zscore_dict[node]= (degree_dict[node] - mean)/std
    return degree_zscore_dict

def calculate_inmodule_degree(G, node2module):
    '''
    Calculates the in-module degree z-Score
    input:
        * G - networkx graph object
        * node2module - node to module translation dictionary
    output:
        * inmoduledegree - node to betweenness mapping
    '''
    inmoduledegree={}
    for node in node2module:
        if G.has_node(node):
           inmod_deg=0
           for neigh_node in G.neighbors(node):
                try:
                  if node2module[neigh_node]==node2module[node]:
                     inmod_deg+=1
                except KeyError:
                  pass
           inmoduledegree[node]=inmod_deg
    return inmoduledegree

def calculate_inmodule_degree_zscore(G, module2node, node2module):
    '''
    Calculates the in-module degree z-Score
    input:
        * G - networkx graph object
        * module2node - module to node list translation dictionary
        * node2module - node to module translation dictionary
    output:
        * inmod_degree_zscore_dict - node to betweenness mapping
    '''
    #Get the inmodule degree
    inmoduledegree = calculate_inmodule_degree(G, node2module)
    #Get the zscore for each module
    module_props = {} #Module scores
    for module, nodelist in module2node.items():
        templist  = [inmoduledegree[n] for n in nodelist]
        module_props[module] = [np.mean(templist), np.std(templist)]
    #zScore for each node now
    inmod_degree_zscore_dict = {} #node zscore
    for node, mod in node2module.items():
        inmod_degree_zscore_dict[node] = (inmoduledegree[node] - module_props[mod][0]) / module_props[mod][1]
    return inmod_degree_zscore_dict


def calculate_participation(G, module2node, node2module):
    '''
    Calculates the participation coefficient as 
    p = 1 - sum[ (num_links_module)/num_links_total^2 ]
    Input:
        * G - graph
        * module2node - module to node list translation
        * node2module - node to module translation
    Output:
        * participation - dictionary
    '''
    from collections import Counter
    participation = {}
    for node in node2module:
        #Set up the basics
        degree = G.degree(node)
        module_ends = [node2module[neigh] for neigh in G.neighbors(node)]
        uniq_modules = list(set(module_ends))
        #Start the calculation
        p = 1.0
        for um in uniq_modules:
            p -= (module_ends.count(um) / degree) ** 2
        #Save it
        participation[node] = p
    return participation


def build_node_roles():
    '''
    Builds a dictionary of the node roles
    Input:
        - None
    Output:
        - Dictionary of node roles with classes. Each class has it's min and max points
    '''
    class Role:
        def __init__(self, minp, maxp, mino, maxo):
            self.minp = minp
            self.maxp = maxp
            self.mino = mino
            self.maxo = maxo

    #enumerate the roles
    roles = {}
    role_num = map(lambda x: x + 1 , range(7))
    for role in role_num:
        if role  in [1, 2, 3, 4]:
            mino = -5.0
            maxo = 2.5
        else:
            mino = 2.5
            maxo = 100 
        #Do the ps, more complicated
        if role in [1, 5]:
            minp = 0.0
            if role == 1:
                maxp = 0.05
            else:
                maxp = 0.30
        elif role == 2:
            minp = 0.05
            maxp = 0.62
        elif role == 3:
            minp = 0.62
            maxp = 0.80
        elif role == 4:
            minp = 0.8
            maxp = 1.0
        elif role == 6:
            minp = 0.30
            maxp = 0.75
        elif role == 7:
            minp = 0.75
            maxp = 1.0
        roles[role] = Role(minp, maxp, mino, maxo)
    return roles

def classify_node_role(p, i):
    '''
    Classifies a node into its role based on participation coefficient
    and within module score
    input:
        * p -- particpation coefficient (float)
        * i -- intra-module z-score
    output:
        * role - integer [1-7]
    '''
    if i < 2.5:
        if p <= 0.05:
            role = 1
        elif p > 0.05 and p<= 0.62:
            role = 2
        elif p > 0.62 and p<= 0.8:
            role = 3
        else:
            role = 4
    else:
        if p <= 0.30:
            role = 5
        elif p > 0.3 and p <= 0.75:
            role = 6
        else:
            role = 7
    return role

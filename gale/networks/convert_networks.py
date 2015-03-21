'''
File: convert_weighted_network_to_linklist.py
Author: Adam Pah
Description: 
Convert a weighted network to linklist
1 2 4
Where links 1 and 2 have weight 4
'''

#Standard path imports
import random
from math import floor
import networkx as nx

#Non-standard imports

#Global directories and variables

def convert_weighted_to_linklist(inputFile, outputFile=None):
    '''
    input: filename, outputFilename
    output: None
    '''
    import gale.fileIO.generic as fgen
    #Get the random name
    if not outputFile:
        outputFile = fgen.random_file_namer(__file__, 'dat')
    indata = [l.strip().split() for l in open(inputFile).readlines()]
    wfile = open(outputFile, 'w')
    for x,y,w in indata:
        w = int(w)
        for z in range(w):
            print >> wfile, '%s %s' % (x,y)
    wfile.close()

def check_neighbor(n1, n2, G):
    '''
    Checks to see if n1 and n2 are neighbors in teh graph G
    input: 
        n1 node 1 label
        n2 node 2 label
        G graph of interest
    output:
        True if neighbors, False if not neighbors
    '''
    if n2 in G.neighbors(n1):
        neighbors = True
    else:
        neighbors = False
    return neighbors

def randomize_network(G, times=100, seed=9999):
    '''
    Randomizes an undirected, unweighted network using the algorithm from rgraph
    input:

    output:
    '''
    #Set the seed
    random.seed(seed)
    #Calculate the number of iterations
    num_edges = G.number_of_edges()
    niter = int(times * (num_edges + random.random()))
    #Swap with the networkx method
    nx.double_edge_swap(G, nswap=niter, max_tries = 10*niter)
    return G

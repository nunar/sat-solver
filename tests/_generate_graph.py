import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

def vrni_graf(stevilo_vozlisc, st_povezav):

    states = [i+1 for i in range(stevilo_vozlisc)]
    print states

    neighbors = []

    #posebej obravnavamo primer za 1. vozlisce, saj mu dodelimo veliko stevilo povezav:
    number_of_neighbours =  stevilo_vozlisc/4
    local_neighbours = []
    i = 0
    while True:
        random_neighbour = random.randint(2, stevilo_vozlisc)
        if random_neighbour not in local_neighbours:
            local_neighbours.append(random_neighbour)
            i=i+1
        if i == number_of_neighbours:
            break
    
    for ln in local_neighbours:
        neighbors.append((1, ln))
        
    #print '1: ', number_of_neighbours, ' sosedov'   
    
    #posebej obravnavamo primer za 2. vozlisce, saj mu dodelimo veliko stevilo povezav:
    number_of_neighbours =  stevilo_vozlisc/5
    local_neighbours = []
    i = 0
    while True:
        random_neighbour = random.randint(2, stevilo_vozlisc)
        if random_neighbour not in local_neighbours:
            local_neighbours.append(random_neighbour)
            i=i+1
        if i == number_of_neighbours:
            break
    
    for ln in local_neighbours:
        neighbors.append((1, ln))

      
    #print stevilo_vozlisc
    for j in range(1, stevilo_vozlisc-1):
        #print 'j',j
        vertex = states[j]
        local_neighbours = []
    
        number_of_neighbours =  random.randint(1, st_povezav)
        #print number_of_neighbours 
        if number_of_neighbours + j + 1 > stevilo_vozlisc:
            number_of_neighbours = 1
   
        #print vertex, ': ', number_of_neighbours, ' sosedov'
        i = 0
    
        while i < number_of_neighbours:
            random_neighbour = random.randint(vertex+1, stevilo_vozlisc)
            if random_neighbour not in local_neighbours:
                local_neighbours.append(random_neighbour)
                i=i+1
            
            
        for ln in local_neighbours:
            neighbors.append((vertex, ln))
            
        #print local_neighbours
    
    
    print neighbors
    return neighbors
    
    
def barvanje_grafov(v, e):
    
    ime = 'barvanje_grafov' + str(v) + '.txt' 
    try:
        file = open(ime,'w')   # Trying to create a new file or open one
        
        #1. del: vozlisce lahko pobarvamo s 3 barvami
        niz1 = 'p cnf ' + str(3*v) + ' ' + str(4*v + 3*len(e)) + ' \n'
        for i in range(v):
            niz1 = niz1 + str(3*i+1) + ' ' + str(3*i+2) + ' ' + str(3*i+3) + ' 0\n'
            niz1 = niz1 + str(-(3*i+1)) + ' ' + str(-(3*i+2)) + ' 0\n'
            niz1 = niz1 + str(-(3*i+1)) + ' ' + str(-(3*i+3)) + ' 0\n'
            niz1 = niz1 + str(-(3*i+2)) + ' ' + str(-(3*i+3)) + ' 0\n'
        
        #2. del: krajisci povezave morati biti razlicno pobarvani
        for edge in e:
            niz1 = niz1 + str(-(3*(edge[0]-1)+1)) + ' ' + str(-(3*(edge[1]-1)+1)) + ' 0\n'
            niz1 = niz1 + str(-(3*(edge[0]-1)+2)) + ' ' + str(-(3*(edge[1]-1)+2)) + ' 0\n'
            niz1 = niz1 + str(-(3*(edge[0]-1)+3)) + ' ' + str(-(3*(edge[1]-1)+3)) + ' 0\n'
            
        file.write(niz1)
        file.close()

    except:
        print('NAPAKA!!!')
        sys.exit(0) 



def resitev(d):
    print len(d)
    ime = 'barvanje_grafov' + str(len(d)) + '.txt' 
    print ime
    try:
        file = open(ime,'w')   # Trying to create a new file or open one 
        niz1 = ''
        
        for i in range(len(d)):
            barva = d[i+1];
            print 'v zaniki'
            if barva == 0:
                niz1 = niz1 + str(3*i+1) + ' ' + str(-(3*i+2)) + ' ' + str(-(3*i+3)) + ' ' 
            elif barva == 1:
                niz1 = niz1 + str(-(3*i+1)) + ' ' + str(3*i+2) + ' ' + str(-(3*i+3)) + ' ' 
            else:
                niz1 = niz1 + str(-(3*i+1)) + ' ' + str(-(3*i+2)) + ' ' + str(3*i+3) + ' '  
            
        file.write(niz1)
        file.close()

    except:
        print('NAPAKA pri pisanju resitve!!!')
        sys.exit(0) 
            
            
            

stevilo_vozlisc = 10
st_povezav = 2

neighbors = vrni_graf(stevilo_vozlisc, st_povezav)

#generiranje datoteke za SAT solver
barvanje_grafov(stevilo_vozlisc, neighbors)

G = nx.Graph()
G.add_edges_from(neighbors)
d = nx.coloring.greedy_color(G, strategy=nx.coloring.strategy_saturation_largest_first)
print d

barve = list(set(d.values()));
print barve

if len(barve) == 3:

    r = []
    g = []
    b = []

    for j in range(stevilo_vozlisc):
        if d[j+1] == 0:
            r.append(j+1)
        elif d[j+1] == 1:
            g.append(j+1)
        elif d[j+1] == 2:
            b.append(j+1)
        
    #print r
    #print g
    #print b
        
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,
                       nodelist=r,
                       node_color='r',)
    nx.draw_networkx_nodes(G,pos,
                       nodelist=g,
                       node_color='g',)
    nx.draw_networkx_nodes(G,pos,
                       nodelist=b,
                       node_color='b',)

    nx.draw_networkx_edges(G,pos,
                       neighbors,
                       width=1)
else:
    print "Za barvanje smo uporabili prevec barv"

plt.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PERT graph generation
#-----------------------------------------------------------------------
# PPC-PROJECT
#   Multiplatform software tool for education and research in
#   project management
#
# Copyright 2007-8 Universidad de C�rdoba
# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math, os, sys
from graph import *

class Pert(object):
    """
    PERT class to store graph data, contains:
      self.successors = directed graph data structure
      self.arcs = activity labels

    directed graph data structure: see graph.py.

    activity labels:
     { (OriginNode, DestinationNode) : (ActivityLabel, DummyActivity), ... }

    DummyActivity: True if dummy, False if real

    Create example PERT graphs with Pert(pertN):
    """
    pert2= ( {1 : [2,4],
              2 : [3],
              3 : [4,6],
              4 : [5],
              5 : [],
              6 : [5]
              },
             {(1,2) : ('b',   False),
              (1,4) : ('a',   False),
              (2,3) : ('d',   False),
              (3,4) : ('du1', True),
              (3,6) : ('e',   False),
              (4,5) : ('c',   False),
              (6,5) : ('f',   False),
              }
            )

    pert3= ( {1 : [2,4],
              2 : [3],
              3 : [4,5],
              4 : [5],
              5 : [],
              },
             {(1,2) : ('b',   False),
              (1,4) : ('a',   False),
              (2,3) : ('d',   False),
              (3,4) : ('du1', True),
              (3,5) : ('e',   False),
              (4,5) : ('c',   False),
              }
            )

    pert4 = ( {1 : [2,3],
               2 : [4,5],
               3 : [4],
               4 : [5],
               5 : [],
               },
              {(1,2) : ('a', False),
               (1,3) : ('b', False),
               (2,5) : ('c', False),
               (4,5) : ('d', False),
               (2,4) : ('e', False),
               (3,4) : ('du1', True),
       }
       )

    pert5 = ( {1 : [2,5],
               2 : [3],
               3 : [4],
               4 : [],
               5 : []
               },
              {(1,2) : ('a', False),
               (2,3) : ('b', False),
               (3,4) : ('c', False),
               (1,5) : ('d', False),
               }
              )

    pert6 = ( {1 : [2],
               2 : [3],
               3 : [4],
               4 : [],
               5 : [6],
               6 : []
               },
              {(1,2) : ('a', False),
               (2,3) : ('b', False),
               (3,4) : ('c', False),
               (5,6) : ('d', False),
               }
              )

    def __init__(self, pert=None):
        if pert == None:
            self.successors = {}
            self.arcs = {}
        else:
            self.successors, self.arcs = pert

    def __repr__(self):
        return 'Pert( (' + str(self.successors) + ',' + str(self.arcs) + ') )'

    def __str__(self):
        s = str(self.successors) + '\n'
        for link, act in self.arcs.iteritems():
            s += str(link) + ' ' + str(act) + '\n'
        return s

    def nextNodeNumber(self):
        """
        New node number max(graph)+1 O(n)
          O(1): len(directed graph)+1 must be an available node number
          (i.e. graph nodes must be numbered starting in 0 or 1 at most)
          Valid if nodes are not deleted (or reasigned when deleted
          O(n))
        """
        if self.successors:
            return max(self.successors)+1
        else:
            return 0

    def addActivity(self, activityName, origin=None, destination=None, dummy=False):
        """
        Adds activity with new nodes or the specified ones
        """
        if origin == None:
            origin = self.nextNodeNumber()
            self.successors[origin] = []

        if destination == None:
            destination = self.nextNodeNumber()
            self.successors[destination] = []

        self.successors[origin].append(destination)
        self.arcs[(origin,destination)] = (activityName, dummy)
        return (origin,destination)

    def addNode(self, node):
        """
        Adds a new node
        """
        self.successors[node] = []

    def activityArc(self, activityName):
        """
        Given an activity name returns the arc which represents it on graph
        """
        for arc,act in self.arcs.iteritems():
            if act[0] == activityName:
                return arc
        return None


    def inActivities(self, reversedGraph, node):
        """
        Return the name of activities directly preceding node
        """
        inAct = []
        for inNode in reversedGraph[node]:
            act, dummy = self.arcs[ (inNode, node) ]
            if not dummy:
                inAct.append(act)

        return inAct

    def inActivitiesR(self, reversedGraph, node):
        """
        Return the name of activities preceding node (directly or throgh
        dummies)
        """
        inAct = []
        for inNode in reversedGraph[node]:
            act, dummy = self.arcs[ (inNode, node) ]
            if dummy:
                inAct += self.inActivitiesR(reversedGraph, inNode)
            else:
                inAct.append(act)

        return inAct

    def outActivities(self, node):
        """
        Return the name of activities directly following node
        """
        outAct = []
        for outNode in self.successors[node]:
            act, dummy = self.arcs[ (node, outNode) ]
            if not dummy:
                outAct.append(act)

        return outAct

    def outActivitiesR(self, node):
        """
        Return the name of activities following node (directly or throgh
        dummies)
        """
        outAct = []
        for outNode in self.successors[node]:
            act, dummy = self.arcs[ (node, outNode) ]
            if dummy:
                outAct += self.outActivitiesR(outNode)
            else:
                outAct.append(act)

        return outAct


    def pertSuccessors(self):
        """
        Extracts all implicit prelations (not redundant)
        """
        revGraph = reversedGraph(self.successors)
        successors = {}
        for node,connections in self.successors.items():
            inputs  = self.inActivities(revGraph, node)
            outputs = self.outActivitiesR(node)
            for i in inputs:
                if i in successors:
                    successors[i] += outputs
                else:
                    successors[i] = outputs
        return successors



    def pert(self, successors):
        """
        Generates a AOA graph (PERT) from successors table
        Algorithm sharma1998 extended
        returns: PERT graph data structure
        """
        if self.successors or self.arcs:
            raise Exception('PERT structure must be empty')

        precedents = reversedGraph(successors)

        # Close the graph (not in sharma1998)
        origin = self.nextNodeNumber()
        self.successors[origin] = []
        dest = self.nextNodeNumber()
        self.successors[dest] = []
        beginAct    = beginingActivities(successors)
        endAct      = endingActivities(successors)
        beginEndAct = beginAct.intersection(endAct)

        #  -Creates a common node for starting activities
        for act in beginAct - beginEndAct:
            self.addActivity(act, origin)

        #  -Creates a common node for ending activities
        for act in endAct - beginEndAct:
            self.addActivity(act, origin=None, destination=dest)

        #  -Deals with begin-end activities
        if beginEndAct:
            act = beginEndAct.pop()
            self.addActivity(act, origin, dest)
            for act in beginEndAct:
                o,d = self.addActivity(act, origin)
                self.addActivity("seDummy", d, dest, dummy=True)

        # Sharma1998 algorithm
        for act in successors:
            #print "Processing", act, self
            #window.images.append( pert2image(self) )
            if not self.activityArc(act):
                self.addActivity(act)
                #window.images.append( pert2image(self) )
            aOrigin, aDest = self.activityArc(act)
            #print '(', aOrigin, aDest, ')'
            for pre in precedents[act]:
                #print self.successors
                #print pre, pre in self.inActivitiesR(reversedGraph(self.successors), aOrigin)
                if pre not in self.inActivitiesR(reversedGraph(self.successors), aOrigin):
                    if not self.activityArc(pre):
                        self.addActivity(pre)
                        #window.images.append( pert2image(self) )
                    self.makePrelation(pre, act)
                    aOrigin, aDest = self.activityArc(act)


    def equivalentRemovingDummy(self, dummy):
        """
        Idea of Lemma1 of Sharma1998 modified

        dummy given as (origin, destination)
        """
        revGraph = reversedGraph(self.successors)
        nodeO, nodeD = dummy

        # Stop being a graph?
        inNodesO  = revGraph[nodeO]
        inNodesD = revGraph[nodeD]
        for n in inNodesO:
            if n in inNodesD:
                return False # Two activities would begin and end in the same nodes
        outNodesO  = self.successors[nodeO]
        outNodesD = self.successors[nodeD]
        for n in outNodesO:
            if n in outNodesD:
                return False # Two activities would begin and end in the same nodes

        # Implies new prelations?
        inO  = set( self.inActivitiesR(revGraph, nodeO) )
        inD  = set( self.inActivitiesR(revGraph, nodeD) )
        outO = set( self.outActivitiesR(nodeO) )
        outD = set( self.outActivitiesR(nodeD) )
        return inD.issubset(inO) or outO.issubset(outD)

    def removeDummy(self, dummy):
        """
        Removes a dummy activity as in sharma1998 (removes destination node
        of dummy moving their dependencies to origin)
        """
        nodeO, nodeD = dummy

        # Removes the dummy activity link from graph
        self.successors[nodeO].remove(nodeD)
        revGraph = reversedGraph(self.successors)

        inD = revGraph[nodeD]
        outD = self.successors[nodeD]
        self.successors.pop(nodeD)

        for node in inD:
            self.successors[node].remove(nodeD)
            self.successors[node].append(nodeO)
        self.successors[nodeO] += outD

        # Activities table
        self.arcs.pop( (nodeO, nodeD) )
        for node in inD:
            act = self.arcs.pop( (node,nodeD) )
            self.arcs[ (node,nodeO) ] = act
        for node in outD:
            act = self.arcs.pop( (nodeD,node) )
            self.arcs[ (nodeO,node) ] = act


    def makePrelation(self, preName, folName):
        """
        Links two activities as described in Sharma1998 (simplified to
        change less arcs)
        """
        pre = self.activityArc(preName)
        fol = self.activityArc(folName)
        preO, preD = pre
        folO, folD = fol

        # New nodes
        newO = self.nextNodeNumber()
        self.successors[newO] = []
        newD = self.nextNodeNumber()
        self.successors[newD] = []

        # Change links of existing nodes to new nodes
        self.successors[folO].remove(folD)
        self.successors[folO].append(newD)
        self.successors[preO].remove(preD)
        self.successors[preO].append(newO)
        # New links
        self.successors[newO].append(newD)
        self.successors[newO].append(preD)
        self.successors[newD].append(folD)

        # Activities table
        # New dummy activities
        dummy1 = (folO, newD)
        dummy2 = (newO, preD)
        dummy3 = (newO, newD)
        self.arcs[ dummy1 ] = ('dummy', True)
        self.arcs[ dummy2 ] = ('dummy', True)
        self.arcs[ dummy3 ] = ('dummy', True)
        # New link of activities with new nodes
        act = self.arcs.pop(pre)
        self.arcs[ (preO, newO) ] = act
        act = self.arcs.pop(fol)
        self.arcs[ (newD, folD) ] = act

        #window.images.append( pert2image(self) )

        # Remove dummy activities if possible
        if self.equivalentRemovingDummy(dummy2):
            #print dummy2, ':equivalent'
            self.removeDummy(dummy2)
            #window.images.append( pert2image(self) )

        if self.equivalentRemovingDummy(dummy1):
            #print dummy1, ':equivalent'
            self.removeDummy(dummy1)
            #window.images.append( pert2image(self) )
            dummy3 = (newO, folO)

        if self.equivalentRemovingDummy(dummy3):
            #print dummy3, ':equivalent'
            self.removeDummy(dummy3)
            #window.images.append( pert2image(self) )

    def demoucron(self):
        """
         Divide un grafo PERT en niveles usando el algoritmo de Demoucron
         Return: lista de listas de nodos representando los niveles de inicio a fin
        """
        nodos = self.successors.keys()

        # v inicial, se obtiene un diccionario con la suma de '1' de cada nodo
        v = {}       
        for n in nodos:
            v[n] = 0
            for m in nodos:
                if (n,m) in self.arcs:
                    v[n] += 1

        num = 0
        niveles = []
        # Mientras haya un nodo no marcado
        while [e for e in v if v[e] != 'x']:
            # Se establecen los nodos del nivel
            niveles.append([])
            for i in v:
                if v[i] == 0:
                    v[i] = 'x'
                    niveles[num].append(i)

            # Actualiza v quitando el nivel procesado
            for m in v:
                if v[m] != 'x':
                    for a in niveles[num]:
                        if (m,a) in self.arcs:
                            v[m] -= 1
            num+=1

        niveles.reverse()
        return niveles
         
           
    def renumerar(self):
        """
         Renumera un grafo Pert para que sus nodos vayan desde 1 a N, donde N
         es el n�mero total de nodos. Cumple que un nodo anterior a otro siempre
         tenga un n�mero menor.
         Valor de retorno: nuevoGrafo (grafo renumerardo)
        """
        niveles = self.demoucron()
        # Se crea un diccionario con la equivalencia entre los nodos originales y los nuevos
        s = 1
        nuevosNodos = {}
        for m in range(len(niveles)):
            if len(niveles[m]) == 1:
                nuevosNodos[niveles[m][0]] = s
                s += 1
            else:
                for a in niveles[m]:
                    nuevosNodos[a] = s            
                    s += 1

        # Se crea un nuevo grafo
        nuevoGrafo = Pert()
        
        # New graph
        for n in self.successors:
            #print n, 'n'
            for m in nuevosNodos:            
                #print  m, 'm'
                if n == m:
                    if self.successors[n] != []:
                        for i in range(len(self.successors[n])):
                            for a in nuevosNodos:
                                if self.successors[n][i] == a:
                                    if i == 0:
                                        nuevoGrafo.successors[nuevosNodos[m]] = [nuevosNodos[a]]
                                    else:                                   
                                        nuevoGrafo.successors[nuevosNodos[m]].append(nuevosNodos[a])
                    else: 
                        nuevoGrafo.successors[nuevosNodos[m]] = []

        # New activities'
        for n in self.arcs:
            for m in nuevosNodos:            
                if n[0] == m:
                    for a in nuevosNodos:
                        if n[1] == a:
                            nuevoGrafo.arcs[nuevosNodos[m],nuevosNodos[a]] = self.arcs[n]

                elif n[1] == m:
                    for a in nuevosNodos:
                        if n[0] == a:
                            nuevoGrafo.arcs[nuevosNodos[a],nuevosNodos[m]] = self.arcs[n]

        return nuevoGrafo

#
# --- GTK para probar imagen del grafo
#
import pygtk
pygtk.require('2.0')
import gtk
import rsvg
import cairo
from SVGViewer import SVGViewer


class Test(object):
    def __init__(self):
        self.images = []
        self.imageIndex = 0

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(800, 600)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", gtk.main_quit)

        self.svg_viewer = SVGViewer()
        self.svg_viewer.show()
        self.screen = gtk.ScrolledWindow()
        self.screen.add_with_viewport(self.svg_viewer)

        self.pos_label = gtk.Label(" -- / -- ")
        self.b_prev = gtk.Button("< Previous")
        self.b_prev.connect("clicked", self.pinta, True)
        self.button = gtk.Button("Next >")
        self.button.connect("clicked", self.pinta, None)

        self.hBox = gtk.HBox(homogeneous=False, spacing=0)
        self.hBox.pack_start(self.pos_label, expand=False, fill=False, padding=4)
        self.hBox.pack_start(self.b_prev,    expand=False, fill=False, padding=4)
        self.hBox.pack_start(self.button,    expand=False, fill=False, padding=4)

        self.vBox = gtk.VBox(homogeneous=False, spacing=0)
        self.vBox.pack_start(self.screen, expand=True,  fill=True,  padding=0)
        self.vBox.pack_start(self.hBox,   expand=False, fill=False, padding=4)
        self.window.add(self.vBox)

#        self.screen.show()
#        self.button.show()
#        self.vBox.show()
        self.window.show_all()

    def delete_event(self, widget, event, data=None):
        return False

    def pinta(self, widget, data=None):
        if data:
            self.imageIndex = (self.imageIndex - 1) % len(self.images)
        else:
            self.imageIndex = (self.imageIndex + 1) % len(self.images)
        self.svg_viewer.update_svg( self.images[self.imageIndex] )
        self.pos_label.set_text( str(self.imageIndex+1) + ' / ' + str(len(self.images)) )


def main(window):
    """
    Test code
    """
    import traceback
    successors = {'a':['c','e'],
                  'b':['d'],
                  'c':[],
                  'd':[],
                  'e':['d'],
                  }

    successors2 = {'a':['c','e','d'],
                  'b':['d'],
                  'c':['f'],
                  'd':['f','g'],
                  'e':['g'],
                  'f':['h'],
                  'g':['h'],
                  'h':['i','j','k'],
                  'i':['l'],
                  'j':['l'],
                  'k':[],
                  'l':[],
                   }
    
    


##   print reversedGraph(pert2[0])
##   for n in range(1,6):
##      print inActivitiesR(pert2, reversedGraph(pert2[0]), n)
##   print "OUT"
##   for n in range(1,6):
##      print outActivitiesR(pert2, n)

##   window.images.append( pert2image(pert4) )
##   print equivalentRemovingDummy(pert4, (3,4) )
##   removeDummy(pert4, (3,4) )

##   pertP = pert5
##   window.images.append( pert2image(pertP) )
##   makePrelation( pertP, (1,5), (3,4) )
##   addActivity( pertP, 'nueva' )
##   makePrelation( pertP, (1,2), (7,8) )
##   makePrelation( pertP, (9,8), (6,4) )
       
#    window.images.append( pert2image(pert.Pert(pert4)) )

#    window.images.append( graph2image(successors2) )
#    window.images.append( graph2image(successors3) )
    try:
        pertP = Pert()
        pertP.pert(successors2)
        #window.images.append( pert2image(pertP) )
        #print pertP
    except Exception as e:
        traceback.print_exception(*sys.exc_info())

##   s = pertSuccessors(pertP)
##   window.images.append( graph2image( roy(s) ) )
    gtk.main()
    

# If the program is run directly    
if __name__ == "__main__":
    pert2= ( {1 : [2,4],
              2 : [3],
              3 : [4,6],
              4 : [5],
              5 : [],
              6 : [5]
              },
             {(1,2) : ('b',   False),
              (1,4) : ('a',   False),
              (2,3) : ('d',   False),
              (3,4) : ('du1', True),
              (3,6) : ('e',   False),
              (4,5) : ('c',   False),
              (6,5) : ('f',   False),
              }
            )

    pert3= ( {1 : [2,4],
              2 : [3],
              3 : [4,5],
              4 : [5],
              5 : [],
              },
             {(1,2) : ('b',   False),
              (1,4) : ('a',   False),
              (2,3) : ('d',   False),
              (3,4) : ('du1', True),
              (3,5) : ('e',   False),
              (4,5) : ('c',   False),
              }
            )

    pert4 = ( {1 : [2,3],
               2 : [4,5],
               3 : [4],
               4 : [5],
               5 : [],
               },
              {(1,2) : ('a', False),
               (1,3) : ('b', False),
               (2,5) : ('c', False),
               (4,5) : ('d', False),
               (2,4) : ('e', False),
               (3,4) : ('du1', True),
       }
       )

    pert5 = ( {1 : [2,5],
               2 : [3],
               3 : [4],
               4 : [],
               5 : []
               },
              {(1,2) : ('a', False),
               (2,3) : ('b', False),
               (3,4) : ('c', False),
               (1,5) : ('d', False),
               }
              )

    pert6 = ( {1 : [2],
               2 : [3],
               3 : [4],
               4 : [],
               5 : [6],
               6 : []
               },
              {(1,2) : ('a', False),
               (2,3) : ('b', False),
               (3,4) : ('c', False),
               (5,6) : ('d', False),
               }
              )

    window = Test()
    main(window)

"""
algoritmo que abre un fichero con extension *.sm pasado como parametro por linea de comandos,
asi como el numero de repeticiones de cada algoritmo para que de resultados que se puedan comparar,
y realiza pruebas a los tres algoritmos:
Conjuntos, Salas, Cohen-Sadeh
las pruebas consisten en tiempo de ejecucion, numero de arcos, numero de arcos ficticios, numeros de arcos
reales, y numero de nodos.
"""

import os
import os.path
import sys
import algoritmoConjuntos
import algoritmoSalas
import algoritmoCohenSadeh
import Cohen_sadeh_Alberto
import graph
import fileFormats
import pert

#REPETICIONES = 1
#REPETICIONES = int(sys.argv[2])
def openProject(filename):
    """
    abre un proyecto ante un nombre pasado como paramentro por linea de comandos
    """
    try:
        actividad  = []
        recurso    = []
        asignacion = []
        schedules  = []
        fileFormat = [
            fileFormats.PPCProjectFileFormat(),
#            fileFormats.PPCProjectOLDFileFormat(),
            fileFormats.PSPProjectFileFormat(),
        ]

        

        # Tries to load file with formats that match its extension in format order
        data = None
        extension = filename[filename.rfind('.')+1:]

        for format in fileFormat:
            if extension in format.filenameExtensions:
                try:
                    data = format.load(filename)
                    break
                except fileFormats.InvalidFileFormatException:
                    pass

        if not data:
            print 'Can not understand file'
            sys.exit(1)

        actividad, schedules, recurso, asignacion = data
        return data[0]
    except IOError:
        print 'Error reading file:', filename
        sys.exit(1)

###si hay dos argumentos pasados por lineas de comandos 
if len(sys.argv)==3:
    repeticiones= int(sys.argv[2]) ###repeticiones es igual al segundo parametro
    filename=sys.argv[1]           ###el nombre del fichero es el primer parametro

    data = openProject(filename)
    successors = {}
    ###obtengo los sucesores de cada actividad
    for i in data:
        successors[i[1]]=i[2]
    ###obtengo prelaciones revertiendo sucesores
    prelaciones1 = graph.reversed_prelation_table(successors)
    

    """
    ejemplos de prelaciones

    prelaciones = {
        'B': [], 
        'A': [], 
        'D': ['B'], 
        'C': [], 
        'F': ['C'], 
        'E': ['D'], 
        'H': ['B'], 
        'G': ['F'], 
        'J': ['F'], 
        'I': ['A'], 
        'L': ['C', 'E'], 
        'K': ['I'], 
        'N': ['B'], 
        'M': ['H'], 
        'P': ['D'], 
        'O': ['E'], 
        'R': ['F'], 
        'Q': ['E'], 
        'S': ['O'], 
        'T': ['J', 'N', 'P'], 
        'U': ['I'], 
        'V': ['Q'], 
        'W': ['K'],
        'X': ['L', 'M', 'R'], 
        'Y': ['J', 'P', 'O'], 
        'Z': ['Y', 'U', 'G'], 
        'AB': ['H'], 
        'AC': ['W', 'U', 'P'],
        'AD': ['X', 'Z', 'AB'],
        'AE': ['S', 'T', 'V']
        }
    prelaciones = {
        'A' : [],
        'B' : [],
        'C' : ['A','B'],
        'D' : ['A'],
        'E' : ['B'],
        'F' : ['A','B'],
        'G' : ['C'],
        'H' : ['D','E'],
        'I' : ['D','E','F'],
        'J' : ['D','E','F'],
        'K' : ['D','F','L'],
        'L' : ['A'],
        }
    prelaciones = {
        'A' : [],
        'B' : [],
        'C' : ['A'],
        'D' : ['A','B'],
        'E' : ['C','D'],
        'F' : ['D'],
        'G' : ['E'],
        'H' : ['F','D','C'],
        'I' : ['F'],
        }
    prelaciones = {
        'A' : [],
        'B' : [],
        'C' : [],
        'D' : ['A'],
        'E' : ['B'],
        'F' : ['C'],
        'G' : ['E','F'],
        'H' : ['D'],
        }
    """
    # List of name and file of each algorithm to test 
    algorithms = [('Cohen-Sadeh', Cohen_sadeh_Alberto.cohen_sadeh), ('Algoritmo Salas', algoritmoSalas.salas), ('Algoritmo Conjuntos', algoritmoConjuntos.algoritmoN)]
    
    for name, alg in algorithms:
        itime=os.times()
        for i in range(repeticiones):
            g = alg(prelaciones1)
        ftime=os.times()
        utime = ftime[0] - itime[0]
        print name
        print "utime %.4f"% (utime)
        print "numero de nodos: ",g.number_of_nodes()
        print "numero de arcos: ",g.number_of_arcs()
        print "numero de arcos reales: ",g.numArcsReales()
        print "numero de arcos ficticios: ",g.numArcsFicticios()
#        print "Prelaciones1: ", prelaciones1
        gg1 = Cohen_sadeh_Alberto.cohen_sadeh(prelaciones1)
#        print "gg1: ", gg1.pertSuccessors()
#        print "Successors: ", successors
        print "Validation: ", Cohen_sadeh_Alberto.validation(successors, gg1)
        print
#        image_text = graph.pert2image(g) # Draw graph and save in a file (*.svg)
#        fsalida = open(name + ' ' + os.path.split(filename)[1] + '.svg', 'w')
#        fsalida.write(image_text)
#        fsalida.close()

else:
    print
    print "Numero de parametros introducidos erroneo."
    print
    print "Ejemplo:"
    print
    print "python pruebaAC.py j301_1.sm 1000"
    print

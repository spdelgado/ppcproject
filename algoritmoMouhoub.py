"""
Algorithm to build a PERT graph based on method of Malek Mouhoub

"""

import namedlist

import fileFormats
import validation
import pert
import graph
import mouhoubRules


def mouhoub(prelations):
    """
    Build a PERT graph using Mouhoub algorithm
    
    prelations = {'activity': ['predecesor1', 'predecesor2'...}

    return p_graph pert.PertMultigraph()
    """
    
    Columns = namedlist.namedlist('Columns', ['pre', 'su', 'blocked', 'dummy', 'suc', 'start_node', 'end_node', 'aux'])
                            # [0 Predecesors, 1 Successors, 2 Blocked, 3 Dummy, 4 Blocked successor, 5 Start node, 6 End node, 7 Auxiliar ]
                            # Blocked = (False or Activity with same precedents) 


    # Adaptation to avoid multiple end nodes
    successors = graph.reversed_prelation_table(prelations)
    successors_copy = graph.reversed_prelation_table(prelations.copy())
    end_act = graph.ending_activities(successors)

  
    
    # STEPS TO BUILD THE PERT GRAPH
    
    #Step 1. Save the prelations in the work table
    complete_bipartite = graph.successors2precedents(Zconf(successors))
    
    
    work_table = {}
    for act, sucesores in complete_bipartite.items():
        work_table[act] = Columns(set(sucesores), successors[act], None, False, None, None, None, None)
        if act not in prelations:
            work_table[act].dummy = True
          
          
    #Step 2. Identify Identical Precedence Constraint of Diferent Activities
    visited_pred = {}
    for act, columns in work_table.items():
        pred = frozenset(columns.pre)
        if pred not in visited_pred:
            visited_pred[pred] = act
        else:
            columns.blocked = visited_pred[pred]
                   
            
    #Step 3. Creating nodes
    # (a) Find start nodes
    node = 0 # instead of 0, can start at 100 to avoid confusion with activities named with numbers when debugging
    for act, columns in work_table.items():
        if not columns.blocked:
            columns.start_node = node
            node += 1
        if columns.blocked:
            columns.start_node = work_table[columns.blocked].start_node
        
        # Associate activities with their end nodes
        for suc, suc_columns in work_table.items():
            if not suc_columns.blocked:
                if act in suc_columns.pre:
                    columns.suc = suc
                    break

    

    # (b) Find end nodes
    graph_end_node = node # Reserve one node for graph end 
    node += 1
    for act, columns in work_table.items():
        suc = columns.suc
        if suc:
            columns.end_node = work_table[suc].start_node
        else:
            # Create needed end nodes, avoiding multiple graph end nodes (adaptation)
            if act in end_act:
                columns.end_node = graph_end_node 
            else:
                columns.end_node = node
                node += 1   


    #Step 4. MOUHOUB algorithm rules to remove extra dummy activities
    
    mouhoubRules.rule_1(successors_copy, work_table)
    
    G2 = mouhoubRules.rule_2(prelations, work_table)
    
    G3 = mouhoubRules.rule_3(G2, work_table)
    
    G4 = mouhoubRules.rule_4(G3, work_table)
    
    G5_6 = mouhoubRules.rule_5_6(successors_copy, work_table, G4)
    
    G3_4 = mouhoubRules.rule_3(G5_6, work_table)
    
    G7 = mouhoubRules.rule_7(successors_copy, successors, G3_4, node)
    
    work_table_final = {}
    for act, sucesores in G7.items():
        work_table_final[act] = Columns([], [], [], sucesores.dummy, sucesores.suc, sucesores.start_node, sucesores.end_node, [])
    

                   
    #Step 6. Generate the graph
    pm_graph = pert.PertMultigraph()
    for act, columns in work_table_final.items():
        _, _, _, dummy, _, start, end, _ = columns
        pm_graph.add_arc((start, end), (act, dummy))
    p_graph = pm_graph.to_directed_graph()
    
    return p_graph




def Zconf(successors):
    """
    Insert a new dummy activity and update the table
    
    return complete_bipartite (PERT network withour Z Configuration)
    """
    complete_bipartite = successors
    
    # Build a PERT network according to Sterboul algorithm
    for act, columns in successors.items():
        for dummy in columns:
   
            node = act + "|" + dummy
           
            if not complete_bipartite.has_key(act):
                complete_bipartite[act] = successors[act]
            new_suc = list(complete_bipartite[act])
        
            complete_bipartite[node] = [dummy]
            new_suc.append(node)
                                
            if dummy in new_suc:
                new_suc.remove(dummy)
            complete_bipartite[act] = list(set(new_suc))  
            
    return complete_bipartite
    
    
    
    
def main():
    """
    Test Mouhoub algorithm

    Arguments:
        infile - project file
    """
    # Parse arguments and options
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    # Open the input file collecting the required information.
    activities, _, _, _ = fileFormats.load_with_some_format(args.infile, [fileFormats.PPCProjectFileFormat(),
                                                                          fileFormats.PSPProjectFileFormat()])
    successors = dict(((act[1], act[2]) for act in activities))
    
    pert_graph = mouhoub(graph.successors2precedents(successors))
    
    window = graph.Test()
    window.add_image(graph.pert2image(pert_graph))
    graph.gtk.main()
    print pert_graph
    print validation.check_validation(successors, pert_graph)
    return 0   
    
    
    
# If the program is run directly
if __name__ == '__main__':
    # Imports needed just for main()
    import sys
    import argparse
    # Run
    sys.exit(main())

import numpy as np
import heapq
from typing import Union

class Graph:
    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """ Unlike project 2, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or the path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self,starting_node=0):
        """ 
        starting_node: adj_mat index for node that will be used to start MST construction from. This is included in the method
        to facilitate a test, `test_find_unique_mst` in `test_mst.py` that a graph with unique edge weights will have a unique MST by constructing an MST from all possible start nodes 
        and checking the same MST is constructed

        What construct_mst is doing:
        1) Instantiate the visited_vertices list with an arbitrarily chosen starting node (default is node from idx 0 of adj_mat but can be chosen as an argument)
        2) instantiate an empty heap for the priority queue
        3) Instantiate an empty 2D nunpy array of the same shape as adj_mat to hold the MST
        4) Add outgoing edges from this starting node to the heap (priority queue), so that you can pick the lowest weight edge to grow the tree.
            4a) look for outgoing edges using `add_edges_to_pq`; docstring of this function explains how it works
        5) While the number of number of nodes within the growing MST (the number of nodes in visited_vertices) is less than the total number of nodes:
            a)Pop the highest priority edge from the priority queue. This edge will (almost) always be the the lowest weight edge because the priority queue is a heap that prioritizes low weights
            b)A popped edge is of the form (weight, start_node, destination node). If the destination node has not already been added to the growing MST (i.e, if it is not already in visited_vertices):
                i) Add the edge to the MST adjacency matrix by adding this edge's weight to the MST at position MST[start_node,destination_node]
                ii) Also add the edge to the opposite side of the MST diagonal by adding this edge's weight at position MST[destination_node,start_node]. This ensures the MST remains symmetric and therefore an undirected graph
                iii) At this point, we have grown the MST by adding the minimum weight edge to a vertex not already in the tree. The added edge was the one of minimum weight because a heap was used for the priority queue
                iv) Add the destination node of the edge to the visited_vertices list
                v) add all outgoing edges from the node to the priority queue, so edges from this vertex ending at a node not already in the growing MST can possibly be added to the MST (if they are of lowest weight)
                vi) steps iv and v together ensure no edges starting from a node in the MST end at a node already in the MST and therefore prevents a cycle, which would be impossible in a MST.
            c) repeat a & b until the MST has the same number of edges as the adjacency matrix (i.e len(vsited_vertices) == num_vertices)
        6) Save the MST in the self.mst attribute

        """
        num_vertices = self.adj_mat.shape[0] #pick one of the 2 dimensions of the symmetric matrix to get the # of vertices
        visited_vertices = [starting_node] #instantiate  list of visited vertices with the 0th vertex arbitrarily chosen to be the starting node
        priority_queue = []
        heapq.heapify(priority_queue) #turn priority_queue list into a heap

        MST = np.array([[float(0) for column in range(num_vertices)] for row in range(num_vertices)]) #instantiate MST filled with 0s that will be updated step-by-step
        def add_edges_to_pq(pq,start_node):
            '''
            pq: priority queue to which outgoing edges will be added
            start_node: All edges from this node will be found and added to the priority queue

            This function adds a tuple to the heap (priority queue) of the form (weight, start_node, destination_node)

            Strategy:
            1. Find neighboring nodes of start node that form an edge (weight >0)
                1a. This is done by indexing the row corresponding to the start node in the adjacency matrix, and looking for indices in that row where the value > 0 
                1b. Those elements are the neighbors that form an edge with the source node
            2. Add the tuple containing (weight, start_node index, neighbor index) to the priority queue

            '''

            for neighbor in np.argwhere(self.adj_mat[start_node]>0):#find neighboring nodes of start node by finding what other nodes form an edge of weight >0 with the start node. Iterate through those neighbors

                neighbor = neighbor[0]#index of neighbor in adjacency matrix is returned in a list of length 1 after using np.argwhere. Get the actual value by indexing it out.  
                heapq.heappush(priority_queue,(self.adj_mat[start_node,neighbor],start_node,neighbor)) #add tuple to priority_queue with form (weight,visited_node_idx,neighbor_idx)

        add_edges_to_pq(priority_queue,visited_vertices[0])#add edges from the start node in visited_vertices to priority_queue

        while len(visited_vertices) < num_vertices: #while not all nodes have been added to visited_vertices, and therefore not all nodes have been added to the MST (MST has to be fully connected)

            lowest_weight_edge = heapq.heappop(priority_queue) #pop lowest weight edge from the priority queue
            if lowest_weight_edge[2] not in visited_vertices: #3rd element in tuple is the destination node of the edge. Check if it is already in visited_vertices. If it is then there is already an edge connecting a node in the MST to this node, which is already in the MST. That would form a cycle; skip it
                MST[lowest_weight_edge[1],lowest_weight_edge[2]] = lowest_weight_edge[0] #Add weight (0th idx) of lowest weight edge in PQ to MST. Add weight to position MST[start_node,destination_node]. Start_node = idx 1 of tuple,  destination node = idx 2 of tuple
                MST[lowest_weight_edge[2],lowest_weight_edge[1]] = lowest_weight_edge[0] #fill in the same edge weight on the other side of the diagonal so the mst adjacency matrix remains symmetric and therefore undirected
                visited_vertices.append(lowest_weight_edge[2]) #add destination vertex to visited_vertices
                add_edges_to_pq(priority_queue,lowest_weight_edge[2]) #add outgoing edges from destination vertex to priority_queue

        self.mst = MST #add finished MST to self.mst attribute
        

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
        """ Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. 
        Note that because we assume our input graph is undirected, `self.adj_mat` is symmetric. 
        Row i and column j represents the edge weight between vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        TODO: 
            This function does not return anything. Instead, store the adjacency matrix 
        representation of the minimum spanning tree of `self.adj_mat` in `self.mst`.
        We highly encourage the use of priority queues in your implementation. See the heapq
        module, particularly the `heapify`, `heappop`, and `heappush` functions.
        

        starting_node: index of adj_mat for node that will be used to start MST construction from. This is included in the method
        to facilitate a test that a graph with unique edge weights will have a unique MST by constructing an MST from all possible start nodes
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

            This function adds a tuple to the heapq priority queue of the form (weight, start_node, destination_node)

            Strategy:
            1. Find neighboring nodes of start node that form an edge (weight >0)
                1a. This is done by indexing the row corresponding to the start node in the adjacency matrix, and looking for indices in that row where the value >0 (those indices are the neighbors that form an edge with source node)
                1b. Those indices are the neighbors that form an edge
            2. Add the tuple containing (weight, start_node index, neighbor index) to the priority queue

            '''

            for neighbor in np.argwhere(self.adj_mat[start_node]>0):#find neighboring nodes of start node by finding what other nodes form an edge of weight >0 with the start node.

                neighbor = neighbor[0]#index of neighbor in adjacency matrix is returned in a list of length 1 after using np.argwhere. Get the actual value by indexing it out.  
                heapq.heappush(priority_queue,(self.adj_mat[start_node,neighbor],start_node,neighbor)) #add tuple to priority_queue with form (weight,visited_node_idx,neighbor_idx)

        add_edges_to_pq(priority_queue,visited_vertices[0])#add edges from the start node in visited_vertices to priority_queue

        while len(visited_vertices) < num_vertices: #while not all vertices have been added to visited_vertices

            lowest_weight_edge = heapq.heappop(priority_queue)
            if lowest_weight_edge[2] not in visited_vertices: #3rd element in tuple representing edge is the destination node. Check if it is already in visited_vertices
                MST[lowest_weight_edge[1],lowest_weight_edge[2]] = lowest_weight_edge[0] #Add weight (0th idx) of lowest weight edge in PQ to MST as an edge visited vertex (1st idx of tuple) and destination node (2nd idx of tuple)
                MST[lowest_weight_edge[2],lowest_weight_edge[1]] = lowest_weight_edge[0] #fill in the same edge weight on the other side of the diagonal so the mst adjacency matrix remains undirected
                visited_vertices.append(lowest_weight_edge[2]) #add destination vertex to visited_vertices
                add_edges_to_pq(priority_queue,lowest_weight_edge[2]) #add edges from destination vertex to priority_queue

        self.mst = MST
        

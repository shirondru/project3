# write tests for bfs
import pytest
import numpy as np
from mst import Graph, BFS
from sklearn.metrics import pairwise_distances
import networkx as nx


def check_mst(adj_mat: np.ndarray, 
              mst: np.ndarray, 
              expected_weight: int, 
              allowed_error: float = 0.0001):
    """ 
        Arguments:
            adj_mat: Adjacency matrix of full graph
            mst: Adjacency matrix of proposed minimum spanning tree
            expected_weight: weight of the minimum spanning tree of the full graph
            allowed_error: Allowed difference between proposed MST weight and `expected_weight`



        ###################################### Added assertions ######################################
        1) Check proposed MST is symmetric: 
        Because the input graph is undirected, the MST adjacency matrix should be symmetric. This also checks that the upper triangle of the MST adjacency matrix
        has the expected edge weights, as the lower triangle was already validated by `check_mst` and this ensures the two triangles are identical.
        This test checks for symmetry by checking that each element in the MST adjacency matrix and the same element in the transposed matrix are similar within a very small tolerance
        
        2) Check all edges in MST are also in adj_mat (i.e, there are no new edges)
        The MST of adj_mat should not contain any edges that were not in adj_mat. This test tests that is the case by iterating through
        each element in the lower triangle of the MST. If an edge exists (the element has weight > 0) between those nodes, check the edge of the same weight
        also exists between the same nodes in adj_mat. Because we have also tested for symmetry, only checking the lower triangle is sufficient.
        
        3) Check MST has expected number of edges
        A tree such as an MST with n nodes will have n-1 edges. Test that is the case by counting the number of nodes in the lower triangular
        portion of the MST. Beacuse we also checked for symmetry, only checking the lower triangle is sufficient.

        4) Check the MST is connected
        MSTs are always connected, so this test tests the proposed MST is connected. It does this by importing the BFS class from project 2. 
        This BFS class was adapted for this project to perform BFS on undirected graphs (rather than directed graphs like in project 2). Because the MST
        is an undirected graph, performing BFS starting at any node will cause traversal of the whole tree. If the MST is connected, then every node will be traversed.
        Therefore, running BFS --starting at an arbitrary node -- will cause traversal of the graph and should return every node in the graph in the list of nodes traversed.
        Test that is the case by asserting the length of the list of bfs-traversed nodes is the same as the number of nodes in the graph
    """
    def approx_equal(a, b):
        return abs(a - b) < allowed_error

    total = 0
    for i in range(mst.shape[0]):
        for j in range(i+1): 
            total += mst[i, j]
    assert approx_equal(total, expected_weight), 'Proposed MST has incorrect expected weight'


    #1) Check proposed MST matrix is symmetric
    assert np.allclose(mst, mst.T), 'Proposed MST adjacency matrix is not symmetric' #Check each element in MST and its transpose are identical within a very small threshold to test for symmetry



    #2) Check that all of the edges in MST are also in the adj_mat
    for i in range(mst.shape[0]):
        for j in range(i+1): #iterate through elements in lower triangle of MST
            if mst[i,j] > 0: #if an element in the lower triangle has weight > 0 it is an edge
                assert approx_equal(mst[i,j], adj_mat[i,j]), 'Proposed MST contains an edge not found in the original graph' #test the edge found in the MST is approx_equal to the edge between the same nodes in the original adj_mat
    
    #3) Check MST has expected number of edges
    num_edges = 0
    num_nodes = adj_mat.shape[0]
    for i in range(mst.shape[0]):
        for j in range(i+1): #iterate through elements in lower triangle of MST
            if mst[i,j] > 0: #if element is an edge (i.e, weight > 0)
                num_edges +=1 #add another edge to the tally of total edges
    assert num_edges == num_nodes - 1, "Proposed MST does not contain expected n-1 # of nodes" #test the MST has n-1 edges, where n is the number of nodes in the graph

    #4) Check if MST is connected 
    mst_bfs = BFS(mst) #instantiate BFS class from project2 with mst matrix. the BFS class was adapted for this project to use an undirected graph (directed graphs were used in project 2)
    bfs_traversal_list = mst_bfs.bfs(start=0) #arbitrarily choose 0th node to start traversal from. Doesn't matter where I start bfs because graph is undirected so it will always traverse the whole thing
    assert len(bfs_traversal_list) == num_nodes #check that the number of nodes traversed via bfs is the same as the number of nodes in the graph, demonstrating connectivity





def test_mst_small():
    """ Unit test for the construction of a minimum spanning tree on a small graph """
    file_path = './data/small.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 8)


def test_mst_single_cell_data():
    """ Unit test for the construction of a minimum spanning tree using 
    single cell data, taken from the Slingshot R package 
    (https://bioconductor.org/packages/release/bioc/html/slingshot.html)
    """
    file_path = './data/slingshot_example.txt'
    # load coordinates of single cells in low-dimensional subspace
    coords = np.loadtxt(file_path)
    # compute pairwise distances for all 140 cells to form an undirected weighted graph
    dist_mat = pairwise_distances(coords)
    g = Graph(dist_mat)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 57.263561605571695)


#test_mst_student
def test_find_unique_mst():
    """ TODO: Write at least one unit test for MST construction 

    If an undirected graph has unique weights for its edges (i.e, no two edges have the same weight) then
    there is one and only one MST for that graph. Proof by contradiction: Let there be two MSTs for a graph with unique edge weights, MST1 and MST2.
    Since MST1 and MST2 are different despite containing the same nodes and despite being connected (by definition of an MST) they must differ by at least one edge.
    Assume they differ by an edge e that is the lowest weight edge possible. There is no other edge in the graph with the same weight because all edge weights are unique.
    If e were to be added to MST2, a cycle C would form because MST2 is an MST. MST1, by definition, does not have any cycles, so there must be an edge e2 in the cycle C that 
    is not in MST1, or else a cycle would exist in MST1. e2 must have higher weight than e1 because e1 was chosen to be the edge with minimum weight in the graph. 
    e1 could replace e2 in MST2 and MST2 would still be an MST (and connected). Therefore, if MST2 was replaced with e1, it would contradict the assertion that MST2 is an MST,
    because it now has a lower total weight --> proof by contradiction that a graph with unique edge weights has a unique MST

    This test therefore tests whether a graph with unique edge weights `small_unique.csv` has a unique mst by constructing 
    the mst repeatedly and starting with a different starting node at each iteration. The resulting mst, no matter what node 
    construction was started at, should be identical. This test asserts that is the case and tests for proper MST construction by showing that, if I input a graph with unique edge weights, a unique MST will be constructed

    """
    file_path = './data/small_unique.csv' #use small_unique.csv, which is the same as small.csv except one of the edges with weight 5 now has weight 3 and therefore all edge weights are unique
    g = Graph(file_path) #instantiate Graph with unique edge weights
    num_nodes = g.adj_mat.shape[0] #number of nodes in g
    for starting_node in range(num_nodes):
        g.construct_mst(starting_node = starting_node) #try constructing the mst for this graph starting with each possible starting node in the graph
        if starting_node == 0:
            baseline_mst = g.mst #the mst that comes from construction starting at node 0 will be compared to the mst constructed starting at each of the other nodes
        else:
            #this line tests that g.mst, which is the mst constructed starting with the starting_node at this iteration is similar within a very small tolerance to the mst constructed starting at node 0
            #This tests for proper MST construction by showing that, if I input a graph with unique edge weights, a unique MST will be constructed
            assert np.allclose(g.mst, baseline_mst), 'There is a problem with your MST construction because the MST for this graph should be unique!' 




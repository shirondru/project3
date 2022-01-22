# write tests for bfs
import pytest
import numpy as np
from mst import Graph
from sklearn.metrics import pairwise_distances


def check_mst(adj_mat: np.ndarray, 
              mst: np.ndarray, 
              expected_weight: int, 
              allowed_error: float = 0.0001):
    """ Helper function to check the correctness of the adjacency matrix encoding an MST.
        Note that because the MST of a graph is not guaranteed to be unique, we cannot 
        simply check for equality against a known MST of a graph. 

        Arguments:
            adj_mat: Adjacency matrix of full graph
            mst: Adjacency matrix of proposed minimum spanning tree
            expected_weight: weight of the minimum spanning tree of the full graph
            allowed_error: Allowed difference between proposed MST weight and `expected_weight`

        TODO: 
            Add additional assertions to ensure the correctness of your MST implementation
        For example, how many edges should a minimum spanning tree have? Are minimum spanning trees
        always connected? What else can you think of?



        ###################################### Added assertions ######################################
        1) Check proposed MST is symmetric: 
        Because the input graph is undirected, the MST adjacency matrix should be symmetric. This also checks that the upper triangle of the MST adjacency matrix
        has the expected edge weights, as the lower triangle was already validated by `check_mst` and this ensures the two triangles are identical.
        This test checks for symmetry by checking that each element in the MST adjacency matrix and the same element in the transposed matrix are similar within a very small tolerance
        
        2) Check all edges in MST are also in adj_mat
        The MST of adj_mat should not contain any edges that were not in adj_mat. This test tests that is the case by iterating through
        each element in the lower triangle of the MST. If an edge exists (the element has weight > 0) between those nodes, check the edge of the same weight
        also exists between the same nodes in adj_mat. Because we have also tested for symmetry, only checking the lower triangle is necessary.

    """
    def approx_equal(a, b):
        return abs(a - b) < allowed_error

    total = 0
    for i in range(mst.shape[0]):
        for j in range(i+1): 
            total += mst[i, j]
    assert approx_equal(total, expected_weight), 'Proposed MST has incorrect expected weight'


    #1) Check proposed MST matrix is symmetric
    assert np.allclose(mst, mst.T), 'Proposed MST adjacency matrix is not symmetric'



    #2) Check that all of the edges in MST are also in the adj_mat
    for i in range(mst.shape[0]):
        for j in range(i+1):
            if mst[i,j] > 0:
                assert mst[i,j] == adj_mat[i,j], 'Proposed MST contains an edge not found in the original graph'
    #Check that the MST edges actually form a path

    #Check MST has correct number of edges
    #Check if MST is connected

    #check there are no cycles

    #given an undirected graph wth unique edge weights, check the MST is unique (by starting at different vertices and seeing what you get)


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
    Since MST1 and MST2 are different despite containing the same nodes and despite being connected (by definition of an MST) they must differ by at least one edge
    Assume they differ by an edge e that is the lowest weight edge possible. There is no other edge in the graph with the same weight because all edge weights are unique.
    If e were to be added to MST2, a cycle C would form because MST2 is an MST. MST1, by definition, does not have any cycles, so there must be an edge e2 in the cycle C that 
    is not in MST1, or else a cycle would exist in MST1. e2 must have higher weight than e1 because e1 was chosen to be the edge with minimum weight in the graph. 
    e1 could replace e2 in MST2 and MST2 would still be an MST and connected. Therefore, if MST2 was replaced with e1, it would contradict the assertion that MST2 is an MST,
    because it now has a lower total weight.


    This test therefore tests whether a graph with unique edge weights `small_unique.csv` has a unique mst by constructing 
    the mst repeatedly and starting with a different starting node at each iteration. The resulting mst, no matter what node 
    construction was started at, should be identical. This test asserts that is the case

    """
    file_path = './data/small_unique.csv' #use small_unique.csv which is same as small.csv except one of the edges with weight 5 now has weight 3 and therefore all edge weights are unique
    g = Graph(file_path) #instantiate Graph with unique edge weights
    num_nodes = g.adj_mat.shape[0] #number of nodes in g
    for starting_node in range(num_nodes):
        g.construct_mst(starting_node = starting_node) #try constructing the mst for this graph starting with each possible starting node in the graph
        if starting_node == 0:
            baseline_mst = g.mst #the mst that comes from construction starting at node 0 will be compared to the mst constructed starting at each of the other nodes
        else:
            #this line tests that g.mst, which is the mst constructed starting with the starting_node at this iteration is similar within a very small tolerance to the mst constructed starting at node 0
            assert np.allclose(g.mst, baseline_mst), 'There is a problem with your MST construction because the MST for this graph should be unique!'




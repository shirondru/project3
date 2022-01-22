import networkx as nx
from collections import deque
from typing import Union

class BFS:
    """
    Class to contain a graph and your bfs function
    """
    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        if type(adjacency_mat) == str:
                self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.graph = nx.Graph(self.adj_mat)

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')
    
    def __trace_path(self,parent,start,end=None):
        """
        This method traces back the path to find the end node by utilizing a dictionary `parent`, whose values
        are the parent nodes to the keys. Specifically, the method:
        1. Initiates a list, `path`, with only the end node inside the list.
        While the last item in the list `path` is not the start node:
        2. Finds the parent of the end node by accessing `parent` using the end node as a key.
        3. Appending the parent of the end node to the end of `path`
        4. While loop exits if the parent of the end node is the start node
        5. Otherwise, the next parent node is found by accessing `parent` using the most recent node (found at the end of `path`)
        6. Append that parent node to `path`
        7. While loop exits if that parent node is the start node
        8. Repeat 5-8 until start node is added to the end of `path`
        9. Reverse `path` from having the order end-> start to having the order start->end
        
        If end == None, there is no path, and this method will return None. However, if end == None,
        this method will never be called because the `bfs` method only calls __trace_path once the end node was found.
    
        
        This method is only meant to be accessed from within the bfs method

        """
        if end: #True if end != None
            path = [end] #if there was an end node, initialize the list with it inside.
            
            while path[-1] != start: #once path contains all nodes from end->start exit the loop
                parent_node = parent[path[-1]] #Parent node of the key is the value returned
                path.append(parent_node)
            return path[::-1] #reverse path so it has order start->end then return it

    def bfs(self, start, end=None):
        """
        This method works as follows:
        * Instantiate an empty `parent` dictionary that will be used to help trace back the shortest, if one exists.
        * Instantiate a visited list and include the start node as the first element. This list will ensure elements won't be re-added to the queue
        * Instantiate the queue and include the start node as the first element. The queue represents the order of nodes that need to be traversed next, and will be built up to ensure the graph is a traversed in a layer-by-layer, breadth-first manner.

        While the queue is not empty:
        1. Mark the first node in the queue as the current node and dequeue it.
        2. If the current node is the end node, break the loop by returning the shortest path via __trace_path. This path is guaranteed to be the shortest path because BFS was used.
        3. If the current node is not the end node, iterate through the current node's outgoing neighbors, adding unvisited ones to the end of the queue and marking them as visited. Additionally, add each neighbor as a key in `parent` with the current node as the value.
            Mark them as visited here because all nodes in the graph will be visited in the same order they appear in the queue anyways, and the if statement condition prevents nodes from appearing in the visited list more than once, preventing cycles from hurting the algorithm.
            At this point, the current node is the parent node of each of its outgoing neighbors. Adding each of these neighbors as a key with the current node as a value into the `parent` dictionary will allow backtracing in the following manner:
                The final outoing neighbor, the end node, can be looked up in the dictionary as a key and it's parent node will be returned as a value. The parent node can then be looked up as a key and it's parent node will be returned. 
                Continue in this manner until the start node is returned, and you will have a list from end node -> start node. Reverse that list to get the shortest path. That is what __trace_path is doing.
        4. Repeat 1-3 until the end node is found or the queue becomes empty
            4a. If the end node is found, return the shortest path via __trace_path
            4b. If there is no end node defined, return the order of traversal which is the visited list.
            4c. If the queue becomes empty, and there was an end node defined, there must not be a path, or the path would have been found. Return None
            
        """
        parent = {} #instantiate dictionary that will be used to trace back shortest path between start and end node using __trace_path method.
        visited = [start] #initialize visited list and include the start node as the first element
        
        
        queue = deque([start]) #initialize deque object with start node already inserted
        #using a deque object instead of a list because popping an item from the front of a list in python has complexity O(N), because the rest of the list needs to be shifted afterwards.
        #while deque objects are built to pop an item from the front of a list with O(1)

        
        while queue: #non-empty lists are True in Python. While loop will continue until queue runs out
            current_node = queue.popleft() #dequeue node at index 0 and mark it as current node. Using deque.popleft() is O(1) rather than pop() which has a worst-case O(N)

            if current_node == end: #if current node is the end node break the loop by returning the shortest path
                path = self.__trace_path(parent,start,end)
                return path #if there is an end node and a path exists, the list of the shortest path will be returned here
            else:
                for out_neighbor in self.graph[current_node]: #iterate through all outgoing neighbors from current node
                    if out_neighbor not in visited: 
                        parent[out_neighbor] = current_node #current_node is parent node of out_neighbor. This dictionary will be used to backtrace the shortest path in the __trace_path method
                        queue.append(out_neighbor) #add outgoing neighbor to queue if it has not already been visited, to avoid issues with cyclical connections
                        visited.append(out_neighbor) #add outgoing neighbor to visited list; nodes are visited in the same order they appear in the queue.
        if end == None: 
            return visited #the visited list contains the order of traversal
        return None #if queue becomes empty a path was not found. If there is an end node, Return None to indicate there is no path. 
            #This line could have been skipped and the method would return None by default if nothing else was returned. But it is clearer to explicitly return None

    



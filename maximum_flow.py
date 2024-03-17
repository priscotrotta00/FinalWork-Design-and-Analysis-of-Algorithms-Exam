from Collections.graphs.graph import Graph
from Collections.graphs import dfs

FORWARD = True
BACKWARD = False

class MaximumFlow():

    __slots__ = '__G', '__f', '__capacityOriginalEdges', '__G_f', '__G_f_nodes', '__G_f_edges', '__G_f_corr'

    def __init__(self, G, capacity=None):
        """It constructs the residual graph associated with the original graph G"""
        self.__G = G                                    #Represents the original graph
        self.__capacityOriginalEdges = capacity         #Represents the capacity of the edges of the original graph. If it is defined, it means that all edges of the original graph have 
                                                        #the same capacity

        #I initialize f(e) = 0 for all edges e in G
        self.__f = {}               #f is a flow in G
        for originalEdge in self.__G.edges():
            self.__f[originalEdge] = 0
        
        #I construct the residual graph G_f
        self.__G_f = Graph(True)
        self.__G_f_nodes = {}       #It's a dictionary that contains the corrispondences bewtween nodes of original graph and nodes of residual graph
        #k = original node, v = residual node
        self.__G_f_corr = {}        #It's a dictionary that contains the corrispondences bewtween edges of orignal graph and a list of edges of residual graph
        #k = original node, v = [residual forward edge, residual backward edge]
        #residual forward edge and residual backward edge are None if edge doesn't exist
        self.__G_f_edges = {}       #It's a dictionary that contains the corrispondences bewtween edges of residual graph and edges of original graph
        #k = residual edge, v = original edge

        #The set of nodes in G_f is the same as that of G
        for u in self.__G.vertices():
            self.__G_f_nodes[u] = self.__G_f.insert_vertex(u.element())             #I also populate G_f_nodes dictionary

        #The set of edges in G_f is the same as that of G, but I have to distinguish between forward and backword edges
        for originalEdge in self.__G.edges():
            (s, d) = originalEdge.endpoints()                                       #end points of edge e in the original graph
            source, dest = self.__G_f_nodes[s], self.__G_f_nodes[d]                 #corrispondent edges of s and d in the residual graph 
            self.__G_f.insert_edge(source, dest, ['f', originalEdge.element()])     #I insert all forward edges with the original capacity
            #I populate my support structures
            residualEdge = self.__G_f.get_edge(source, dest)
            self.__G_f_corr[originalEdge] = [residualEdge, None]
            self.__G_f_edges[residualEdge] = originalEdge


    def maxFlow(self, S, T):
        """Given a flow network G, find a flow of maximum value in G
        S is the source node in the original graph
        T is the sink node in the original graph"""                
        diz = {}

        #while there is a S-T path in G_f
        while(dfs.DFS_simple(self.__G_f, self.__G_f_nodes[S], self.__G_f_nodes[T], diz)):       #DFS_simple returns True if a path between S and T exists
            P = dfs.construct_path(self.__G_f_nodes[S], self.__G_f_nodes[T], diz)               #P is a simple path from S to T
            
            newF = self.__augment(P)                                                            #Augment f by putting as much flow on P as possible

            self.__updateG_f(newF)                                                              #Update G_f

            diz = {}                                                                            #I calculate a new simple path from S to T

        return self.__f


    def __augment(self, P):
        """Augment f by putting as much flow on P as possible and it returns a new f with only edges that have been updated
        P is a S-T simple path in G_f"""
        #b is the bottleneck on the path P  
        if(self.__capacityOriginalEdges is not None):
            b = self.__capacityOriginalEdges            #If capacityOriginalEdges is not None, it represents the bottleneck of the path beacuse if a path exists, the maximum flow
                                                        #for an edge is its capacity (for construction all edges have the same capacity)        
        else:
            b = self.__bottleneck(P)                    #Otherwise I calculate it

        f = {}                                                      #I create a new f in order to store the edges that have changed the value of their capacity

        #for each edge(u, v) ∈ P
        for i in range(len(P)-1):
            residualEdge = self.__G_f.get_edge(P[i], P[i+1]) 
            originalEdge = self.__G_f_edges[residualEdge]

            #if (u, v) is a forward edge
            if(self.__isForwardEdge(residualEdge)):
                f[originalEdge] = self.__f[originalEdge] + b         #f((u, v)) = f((u, v)) + b
            
            #else if (u, v) is a backward edge
            elif(self.__isBackwardEdge(residualEdge)):
                f[originalEdge] = self.__f[originalEdge] - b         #f((u, v)) = f((u, v)) - b

        return f


    def __isForwardEdge(self, residualEdge):
        """It returns True if residualEdge is a forward edge, False otherwise"""
        return residualEdge.element()[0] == 'f'


    def __isBackwardEdge(self, residualEdge):
        """It returns True if residualEdge is a backward edge, False otherwise"""
        return residualEdge.element()[0] == 'b'


    def __bottleneck(self, P):
        """Returns the minimum capacity of the edges used along path P (in the residual graph)        
        P is a S-T simple path in G_f"""   

        min = self.__G_f.get_edge(P[0], P[1]).element()[1]

        for i in range(1, len(P)-1, 1):
            C_e = self.__G_f.get_edge(P[i], P[i+1]).element()[1]
            if(C_e < min):
                min = C_e

        return min      


    def __updateG_f(self, newF):
        """Update the residual graph based on the values of f"""
        #I iterate over the edges of G and I create/update/delete forward and backward edges
        for originalEdge in self.__G.edges():                                       #For each edge e = (𝑢,𝑣) in G
            try:
                self.__f[originalEdge] = newF[originalEdge]             #I update an edge of residual graph only if the value of f[originalEdge] is effectly changed               
                self.__update_edge(originalEdge, FORWARD)                           #if 𝑓(𝑒) < 𝑐_𝑒 there is a directed forward edge (𝑢,𝑣) in 𝐺𝑓 with capacity 𝑐_𝑒 - 𝑓(𝑒)                                    
                self.__update_edge(originalEdge, BACKWARD)                          #if 𝑓(𝑒) > 0 there is a directed backward edge (𝑢,𝑣) in 𝐺𝑓 with capacity 𝑓(𝑒)
            except(KeyError):
                pass
                    
    
    def __update_edge(self, originalEdge, forward):
        """Update the edge between source and dest in the residual graph with capacity passed as first paramter.
        If capacity is 0, the edge between source and dest nodes is deleted.
        capacity is the new capacity of the edge between source and dest nodes in the residual graph.
        source and dest are respectively the source and destination node of the edge that you want to update.
        originalEdge is the edge between source and dest nodes in the original graph.
        forward is True if edge is a forward edge, false otherwise. 
        """
        if(forward):
            capacity = originalEdge.element() - self.__f[originalEdge]              #if 𝑓(𝑒) < 𝑐_𝑒 there is a directed forward edge (𝑢,𝑣) in 𝐺𝑓 with capacity 𝑐_𝑒 - 𝑓(𝑒)
            ind = 0         #0 if it is a forward edge
        else:
            capacity = self.__f[originalEdge]                                       #if 𝑓(𝑒) > 0 there is a directed backward edge (𝑢,𝑣) in 𝐺𝑓 with capacity 𝑓(𝑒)
            ind = 1         #1 otherwise

        residualEdge = self.__G_f_corr[originalEdge][ind]                           #It is a forward edge if forward is True, it is a backward edge otherwise
        
        if(capacity == 0):
            if(residualEdge is not None):
                #I delete edge between source and dest
                (source, dest) = residualEdge.endpoints()
                self.__G_f.delete_edge(source, dest)
                #I update my support structures
                self.__G_f_corr[originalEdge][ind] = None                           #I set to None the referement to residual edge that I've deleted
                del self.__G_f_edges[residualEdge]                                  #I also delete the correspondence between the edge of G and the corresponding edge in G_f
        else:
            if(residualEdge is None):
                #I insert an edge
                (s, d) = originalEdge.endpoints()                                   #end points of edge e in the original graph
                source, dest = self.__G_f_nodes[s], self.__G_f_nodes[d]             #corrispondent edges of s and t in the residual graph 
                if(forward):
                    #I insert an edge between source and dest
                    self.__G_f.insert_edge(source, dest, ['f', capacity])
                    residualEdge = self.__G_f.get_edge(source, dest)
                else: 
                    #I insert an edge between dest and source
                    self.__G_f.insert_edge(dest, source, ['b', capacity])
                    residualEdge = self.__G_f.get_edge(dest, source)
                #I update my support structures
                self.__G_f_corr[originalEdge][ind] = residualEdge                   #I set to the new residualEdge the referement to residual edge that I've inserted
                self.__G_f_edges[residualEdge] = originalEdge                       #I also create the correspondence between the edge of G and the corresponding edge in G_f
            elif(self.__capacityOriginalEdges is None):
                #I update edge between source and dest with the new capacity
                residualEdge.element()[1] = capacity
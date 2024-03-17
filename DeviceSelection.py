from Collections.graphs.graph import Graph
from maximum_flow import MaximumFlow

CAPACITY = 1

class DeviceSelection:

    __slots__ = '__graph', '__setA', '__setB', '__dictA', '__dictB', '__P', '__C', '__iterators'

    def __init__(self,N, X, data):
        """DeviceSelection(N, X, data), where N is a tuple of strings identifying the
        devices, X is an integer, and data is a dictionary whose keys are the elements
        of N, and whose values are tuples of X-2 elements describing the
        performances of the corresponding device over sentences from 3-term to
        X-term;"""

        #Starting from a bipartite graph containing only devices that dominates at least another device in the first set and only devices that are dominated at least from another device in 
        #the second set (each node per side represents a device) - it exists a directed edge between node u and node v only if u represents a device that dominates the device 
        #represented by v.
        #The idea is to create a flow network G containing the bipartite graph previously exposed plus a source node S and a sink node T.
        #There is a directed edge from node S to each node belonging to the first set of the bipartite graph and there is a directed edge from each node belonging to the second set of the 
        #bipartite graph to node T.
        self.__graph = Graph(True)
        self.__setA = set()
        self.__setB = set()
        self.__dictA = {}
        self.__dictB = {}
        
        nodeS = self.__graph.insert_vertex('S')
        nodeT = self.__graph.insert_vertex('T')

        domination = []

        for a in N:
            for b in N:
                if(a != b):
                    if(self.__dominates(data[a], data[b])):
                            self.__setA.add(a)
                            self.__setB.add(b)
                            domination.append((a, b))

        for a in self.__setA:
            vertex = self.__graph.insert_vertex(a) 
            self.__dictA[a] = vertex
            self.__graph.insert_edge(nodeS, vertex, CAPACITY)

        for b in self.__setB:
            vertex = self.__graph.insert_vertex(b + ' B') 
            self.__dictB[b] = vertex
            self.__graph.insert_edge(vertex, nodeT, CAPACITY)

        for (a, b) in domination:
            self.__graph.insert_edge(self.__dictA[a], self.__dictB[b], CAPACITY)

        """
        In the example of the test {'Device 1': (100, 99, 85, 77, 63), 'Device 2': (101, 88, 82, 75, 60), 'Device 3': (98, 89, 84, 76, 61), 'Device 4': (110, 65, 65, 67, 80), 'Device 5': (95, 80, 80, 63, 60)},
        we have:
        
                 First set           Second set
            - - > Device 1    - - >   Device 3 - -
          /                   \                    \
        S                      \                    - - > T     
          \                     \                  /
            - - > Device 3    - - ->  Device 5 - -         
                              
        edges: S -> Device 1, S -> Device 3, Device 1 -> Device 3, Device 3 -> Device 5, Device 1 -> Device 5, Device 3 -> T, Device 5 -> T                      
        """

        #I apply the Maximum flow algorithm on G in order to find a flow of maximum value in G
        maximumFlow = MaximumFlow(self.__graph, CAPACITY)
        f = maximumFlow.maxFlow(nodeS, nodeT)       #f is a flow in G

        #Now I can start to create the partition
        self.__P = []

        #From the result of the maximum flow algorithm, I select only the edges with the maximum capacity and and which do not include node S or node T
        for e in f.keys():
            if(f[e] == CAPACITY):
                (source, dest) = e.endpoints()
                if(source != nodeS and dest != nodeT):
                    self.__P.append([source.element(), dest.element()[:-2]])

        #So I have a partition consisting of two devices per subset
        
        """
        In the previous example, I have only the subsets ['Device 1', 'Device 3'] and ['Device 3', 'Device 5']
        """
         
        #From these subsets, I merge the subsets that have devices in common in order to minimize the number of subsets
        modified = True
        while(modified):
            modified = False
            for subset1 in self.__P:
                for subset2 in self.__P:
                    if(subset1 != subset2):
                        if(subset1[-1] == subset2[0]):
                            for elem in subset2[1:]:
                                subset1.append(elem)
                            self.__P.remove(subset2)
                            modified = True
                            break
                        elif(subset1[0] == subset2[-1]):
                            for elem in subset1[1:]:
                                subset2.append(elem)
                            self.__P.remove(subset1)
                            modified = True
                            break
                if(modified):
                    break

        """
        In the previous example, I have only the following subset: ['Device 1', 'Device 3', 'Device 5']
        """

        #Then I add all the devices not included in any subset, namely devices that are not dominated and do not dominate each of the remaining devices
        for device in N:
            found = False
            for list in self.__P:
                if device in list:
                    found = True
                    break
            if(not(found)):
                self.__P.append([device])
        
        """
        In the previous example, I have the following subsets: ['Device 1', 'Device 3', 'Device 5'], ['Device 2'], ['Device 4']
        """
        self.__C = len(self.__P)                                    #C represents the number of different subsets in the partition
        self.__iterators = [iter(subset) for subset in self.__P]    #iterators represents a list of iterators; the i-th iterator iterates on the i-th subset
        

    def __dominates(self, a, b):
        """Returns True if performances of the first device dominates performances of the second device, otherwise it returns False"""
        done = True
        for i in range(len(a)):
            if a[i] <= b[i]:
                done = False
                break
        return done
        

    def countDevices(self):
        """countDevices(), that returns the minimum number C of devices for which we
        need to run the expensive tests. That is, C is the number of subsets in which
        the devices are partitioned so that every subset satisfies the non-interleaving
        property;"""
        return self.__C


    def nextDevice(self,i):
        """nextDevice(i), that takes in input an integer i between 0 and C-1, and returns
        the string identifying the device with highest rank in the i-th subset that has
        been not returned before, or None if no further device exists (e.g., the first call
        of nextDevice(0) returns the device with the highest rank in the first subset,
        i.e., the one that dominates all the remaining devices in this subset, the
        second call returns the device with the second highest rank, and so on). The
        method throws an exception if the value in input is not in the range [0, C-1]."""
        if (i < 0 or i >= self.__C):
            raise Exception

        return next(self.__iterators[i], None)
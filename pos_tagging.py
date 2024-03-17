def pos_tagging(R, S, T, E):
    """
    Dynamic Programming
    1) Define sub-problems: speech of fewer words
    2) Define cases:
        -case 1: i=0  -> word is the first word of the speech
        -case 2: i!=0 -> word is not the first word of the speech
    The characteristic equation is:

                     ('Start', prob)    con prob = T['Start'][R[k]] * E[S[i]][R[k]]                 if prob>0, i=0, 0<=k<=m 
                    /
        P[i][k] = --
                    \
                     (R[j], prob)       con prob = max(P[i-1][j][1]*T[R[j]][R[k]]*E[S[i]][R[k]])    if prob>0, i!=0, 0<=k<=m, 0<=j<=m   

    3) Define boundary (initial) conditions: 
        -speech of one word
    4) Define the order of resolution: from the last row to the first row
    """

    result = dict()                             #dict containing the solution
    n, m = len(S), len(R)                       #introduce convenient notations 
    P = [[('', 0)] * m for i in range(n)]       #n x m table: this table contains for all cells a tuple of:
                                                #(previous role visited, probability = prob that word in the i-th row is the role contained in the j-th column *
                                                #                                      prob that I pass from the previous role visited to the role contained in the j-th column)
                                                #Es. Will is a Noun = 1/4 * After Start I have a Noun = 3/4 -> ('Start', 0.1875)
    """
    In this example
    P =
    [         Noun     Modal     Verb
    Will    [('', 0), ('', 0), ('', 0)], 
    Mary    [('', 0), ('', 0), ('', 0)], 
    Spot    [('', 0), ('', 0), ('', 0)], 
    Jane    [('', 0), ('', 0), ('', 0)]
    ]
    """

    for i in range(n):                                                      #For all words
        for k in range(m):                                                  #for all roles
            #First case
            if(i == 0):                                                     #If I am analizyng first word in the speech
                prob = T['Start'][R[k]] * E[S[i]][R[k]]                         #I calculate its probability
                if(prob > 0):                                                   #If this probability is positive
                    P[i][k] = ('Start', prob)                                       #I update the tuple into the table
            #Second case
            else:                                                           #Else, for all the other words
                max = ('', 0)                                                   #I initialize a tuple containing the max probabilitiy
                for j in range(m):                                              #for all roles that can precede the current role
                    if(P[i-1][j] != ('',0)):                                        #If the tuple contained in the previous row is not the initial tuple
                        prevRole=R[j]                                       
                        prevProb=P[i-1][j][1]
                        prob = prevProb*T[prevRole][R[k]]*E[S[i]][R[k]]                 #I calculate the new probability multiplying with the previous one
                        if(prob > max[1]):                                              #If the current probability is the maximum probability
                            max = (prevRole, prob)                                          #I update max
                if(max[1] > 0):                                                 #At the end of all roles for the current word, If max is positive
                    P[i][k] = max                                                   #I update the tuple into the table                                 
                
    """
    So after all the iterations on the first word, I have:
    Will ->
    Noun : prob = 1/4 * 3/4 = 1/36 = 0.1875     probabilità che Will sia un Noun e che una frase inizi con un Noun
    Modal: prob = 3/4 * 1/4 = 3/16 = 0.1875     probabilità che Will sia un Modal e che una frase inizi con un Modal
    Verb : prob =  0  *  0  = 0                 probabilità che Will sia un Verb e che una frase inizi con un Verb
    
    So in this moment, I have:
    P = 
    [               Noun                  Modal               Verb
    Will    [('Start', 0.1875),     ('Start', 0.1875),      ('', 0)],
    Mary    [     ('', 0),               ('', 0),           ('', 0)], 
    Spot    [     ('', 0),               ('', 0),           ('', 0)], 
    Jane    [     ('', 0),               ('', 0),           ('', 0)]
    ]
    
    At the end, I have:
    P = 
    [               Noun                      Modal               Verb
    Will    [('Start', 0.1875),         ('Start', 0.1875),      ('', 0)     ], 
    Mary    [('Modal', 0.046875),            ('', 0),           ('', 0)     ],      <- tra le varie alternative che ho, prendo solo quella che massimizza la probabilità
    Spot    [ ('Noun', 0.0026),              ('', 0),       ('Noun', 0.0026)], 
    Jane    [ ('Verb', 0.0026),              ('', 0),           ('', 0)     ]       <- tra le varie alternative che ho, prendo solo quella che massimizza la probabilità
    ]
    """

    #now I need to see what is the probability that the last word is the end of the speech
    #so I loop this for the last word

    max = ('', 0)                                           #I initialize a maximum
    for j in range(m):                                      #For all roles
        if(P[n-1][j] != ('',0)):                            #If the tuple in the j-th column is not the initial tuple
            currentRole=R[j]                                #I retrieve the current role 
            prob = P[n-1][j][1]*T[currentRole]['End']       #And I calculate the probability that the speech ends with this role (also taking into account all the previously calculated probabilities)
            if(prob > max[1]):                              #If the current probability is the maximum probability
                max = (currentRole, prob)                   #I update the max

    """
    max = ('Noun', 0.001157)    <- considera anche la probabilità che una frase termina con un Noun (di questa ne avrò sicuramente una sola!)
    """

    if(max[1] == 0):                    #At the end of this loop, If the maximum probability is 0
        return result                   #then neither path is correct

    prevRole = max[0]                   #Role of the last word in contained in the max tuple, in position 0
    result[S[-1]] = max[0]     

    """
    result = 
    {
    'Jane': 'Noun'
    }
    """

            #range(start, stop, step)
    for i in range(n-1, 0, -1):         #For all words        
        for k in range(m):              #For all roles
            if(R[k] == prevRole):       #If the current role is the role that I am searching
                ind = k                 #I take its index
                break
        prevRole = P[i][k][0]           #And I use it to retriev the previous role
        result[S[i-1]] = prevRole       #then I can add it into the result dictionary assiociated with the correct word

    """
    result = 
    {
    'Jane': 'Noun', 
    'Spot': 'Verb', 
    'Mary': 'Noun', 
    'Will': 'Modal'
    }
    """

    return result       #I return the result dictionary
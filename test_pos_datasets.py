from pos_tagging import pos_tagging
from time import perf_counter

def read_data(folder):
    f = open(folder + "/transition",'r')
    t = dict()
    t["Start"] = dict()
    words = f.readline().split()
    r = open(folder + "/roles", 'r')
    roles=[]
    for i in range(len(words)-1):
        roles.append(r.readline())
    r.close()
    for i in range(len(words)-1):
        t['Start'][roles[i]]=float(words[i])
    t['Start']['End']=float(words[len(words)-1])
    j=0
    for line in f:
        t[roles[j]]=dict()
        words = line.split()
        for i in range(len(words)-1):
            t[roles[j]][roles[i]]=float(words[i])
        t[roles[j]]['End']=float(words[len(words)-1])
        j += 1
    f.close()

    f = open(folder + "/emission",'r')
    s = open(folder + "/sentence",'r')
    e = dict()
    j = s.readline()
    for line in f:
        e[j] = dict()
        words = line.split()
        for i in range(len(words)):
            e[j][roles[i]] = float(words[i])
        j = s.readline()
    f.close()
    s.close()

    return t, e

def read_sol(folder, r_num):
    f = open(folder + "/" + "sol",'r')
    r = open(folder + "/" + "roles", 'r')
    w = open(folder + "/" + "sentence",'r')
    s = dict()
    words = f.readline().split()
    roles=[]
    for i in range(r_num):
        roles.append(r.readline())
    r.close()
    for i in range(len(words)):
        s[w.readline()]=roles[int(words[i])]
    f.close()
    w.close()

    return s


folders = ['datasets/pos_datasets/pos_dataset1', 'datasets/pos_datasets/pos_dataset2', 'datasets/pos_datasets/pos_dataset3']

for i in range(3):
    T, E = read_data(folders[i])
    R = tuple(T.keys())[1:len(T)]
    S = tuple(E.keys())
    start = perf_counter()
    sol = pos_tagging(R, S, T, E)
    end = perf_counter()-start
    out = read_sol(folders[i], len(T)-1)

    if sol != out:
        print('FAIL')
    else:
        print('True')
        print(end)
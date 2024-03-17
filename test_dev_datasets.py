from DeviceSelection import DeviceSelection
from time import perf_counter

def dominates(a, b):
    done = True
    for i in range(len(a)):
        if a[i] <= b[i]:
            done = False
            break
    return done

def verify(data,partition):
    try:
        devices = list(data.keys())
        for sets in partition:
            for i in range(len(sets)-1):
                if not dominates(data[sets[i]], data[sets[i+1]]):
                    return False
                devices.remove(sets[i])
            devices.remove(sets[len(sets)-1])
        if len(devices) != 0:
            return False
    except:
        return False
    return True

def dev_read_data(folder):
    data = dict()
    f = open(folder + "/data",'r')
    for line in f:
        sline=line.split()
        data[sline[0].strip()] = []
        for i in range(1, len(sline)):
            data[sline[0].strip()].append(int(sline[i]))
    f.close()
    return data

def dev_read_sol(folder):
    sol = []
    f = open(folder + "/devsol",'r')
    for line in f:
        sline=line.split()
        subset=[]
        for dev in sline:
            subset.append(dev.strip())
        sol.append(subset)
    f.close()
    return sol

folders = ['datasets/dev_datasets/dev_dataset1', 'datasets/dev_datasets/dev_dataset2', 'datasets/dev_datasets/dev_dataset3']

for j in range(3):
    data = dev_read_data(folders[j])
    N = tuple(data.keys())
    X = len(data['D0']) + 2
    start = perf_counter()
    ds=DeviceSelection(N, X, data)
    C=ds.countDevices()
    subsets = [[] for i in range(C)]
    for i in range(C):
        dev = ds.nextDevice(i)
        while dev is not None:
            subsets[i].append(dev)
            dev = ds.nextDevice(i)
    end=perf_counter()-start
    #print(sorted(subsets))

    partition = dev_read_sol(folders[j])
    if not verify(data, subsets) or C > len(partition):
        print('FAIL')
    else:
        print('True')
        print(end)

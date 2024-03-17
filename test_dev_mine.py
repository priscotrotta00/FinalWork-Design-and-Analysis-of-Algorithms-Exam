from DeviceSelection import DeviceSelection
from time import perf_counter

#Testing DeviceSelection
def test(N, X, data, partition):
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
    if sorted(subsets) != sorted(partition):
        print('FAIL')
    else:
        print('True')
        print(end)

N1 = ('Device 1', 'Device 2', 'Device 3', 'Device 4')
X1 = 4
data1 = {'Device 1': (3, 3), 'Device 2': (2, 1), 'Device 3': (1, 2), 'Device 4': (4, 2)}
partition1 = [['Device 1', 'Device 3'], ['Device 4', 'Device 2']]
test(N1, X1, data1, partition1)

N2 = ('Device 4', 'Device 2', 'Device 3', 'Device 1')
X2 = 4
data2 = {'Device 1': (3, 3), 'Device 2': (2, 1), 'Device 3': (1, 2), 'Device 4': (4, 2)}
partition2 = [['Device 1', 'Device 3'], ['Device 4', 'Device 2']]
test(N2, X2, data2, partition2)

#DOUBLE CHANCES

def test2(N, X, data, partition1, partition2):
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
    #print(subsets)
    if (sorted(subsets) != sorted(partition1) and sorted(subsets) != sorted(partition2)):
        print('FAIL')
    else:
        print('True')
        print(end)

N3 = ('Device 1', 'Device 2', 'Device 3')
X3 = 4
data3 = {'Device 1': (4, 4), 'Device 2': (2, 1), 'Device 3': (1, 2)}
partition3 = [['Device 1', 'Device 2'], ['Device 3']]
partition3_2 = [['Device 1', 'Device 3'], ['Device 2']]
test2(N3, X3, data3, partition3, partition3_2)

N4 = ('Device 1', 'Device 2', 'Device 3', 'Device 4')
X4 = 5
data4 = {'Device 1': (100, 90, 200), 'Device 4': (90, 100, 90), 'Device 2': (50, 70, 50), 'Device 3': (90, 89, 100)}
partition4 = [['Device 4', 'Device 2'], ['Device 1', 'Device 3']]
partition4_2 = [['Device 4'], ['Device 1', 'Device 3', 'Device 2']]
test2(N4, X4, data4, partition4, partition4_2)

#FOUR CHANCES

def test3(N, X, data, partition):
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
    #print(subsets)
    if (len(subsets) != 4):
        print('FAIL')
    else:
        print('True')
        print(end)

N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5', 'Device 6', 'Device 7', 'Device 8')
X = 4
data = {'Device 1': (3, 3), 'Device 2': (2, 1), 'Device 3': (1, 2), 'Device 4': (4, 2), 'Device 5': (1, 1), 'Device 6': (4, 3), 'Device 7': (2, 2), 'Device 8': (1, 1)}
partition = [['Device 1', 'Device 7', 'Device 5'], ['Device 4', 'Device 2'], ['Device 6', 'Device 3'], ['Device 8']]
test3(N, X, data, partition)

#SIX CHANCES

def test4(N, X, data, partition):
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
    #print(subsets)
    if (len(subsets) != 6):
        print('FAIL')
    else:
        print('True')
        print(end)

N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5', 'Device 6', 'Device 7', 'Device 8', 'Device 9', 'Device 10')
X = 5
data = {'Device 1': (11, 20, 8), 'Device 2': (12, 0, 2), 'Device 3': (48, 1, 1), 'Device 4': (10, 9, 8), 'Device 5': (10, 10, 6), 'Device 6': (1, 32, 0), 'Device 7': (5, 7, 9), 'Device 8': (4, 6, 3), 'Device 9': (7, 12, 18), 'Device 10': (0, 1, 1)}
partition = [['Device 4', 'Device 8', 'Device 10'], ['Device 1', 'Device 5'], ['Device 9', 'Device 7'], ['Device 2'], ['Device 3'], ['Device 6']]
c = test4(N, X, data, partition)
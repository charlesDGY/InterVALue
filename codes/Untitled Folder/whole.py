import lcm
import quicksort
import remove_repeat
import floyd

#the state in the FSM
class State(object):

    #def __init__(self, name = 'S', block = None, range = '', ins = 0):
    def __init__(self, name = 'S', block = None, range = ''):
        self.name = name
        self.succs = {}
        self.block = block
        self.range = range


    #def add_succ(self, job, edge):
        #self.succs[job] = edge

    def set_block(self, block):
        self.block = block

    def get_block(self):
        return self.block

#transition/edge in the FSM
class Edge(object):

    def __init__(self, event = ['name', 1], action = ['name', 0], output = 'o', guard = '', start = None, end = None, block = None):
        self.event = event
        self.action = action
        self.output = output
        self.guard = guard
        self.start = start
        self.end = end
        self.block = block

    def set_block(self, block):
        self.block = block

    def get_block(self):
        return self.block

#define the state in the reachbility graph
class Rea_state(object):

    def __init__(self, name = '', block = None, range = '', ins = 0):
        self.name = name
        self.succs = {}
        self.block = block
        self.range = range
        self.ins = ins

    def add_succ(self, job, wcet):
        self.succs[job] = wcet

    def set_block(self, block):
        self.block = block

    def get_block(self):
        return self.block




#kkall instants needed in the reachability graph
def find_ins(E, LCM):
    ins = []
    for i in range(0, LCM, 1):
        for e in range(len(E)):
            if (i% E[e] == 0) & (i not in ins):
                ins.append(i)


    return ins


# define the reachability graph as a class, its two attributes: 1. all states with their instants
#2 the periods of events in it.
class Rgraph(object):

    def __init__(self, matrix = [], events = []):
        self.matrix = matrix
        self.events = events

class Block(object):

    def __init__(self, states, edges, name='B', periods = []):
        self.states = set(states)
        self.edges = set(edges)
        for s in states:
            s.set_block(self)
        for e in edges:
            e.set_block(self)
        self.name = name
        self.periods = periods
        #for e in edges:
            #if e.event[-1] not in self.periods:
                #self.periods.append(e.event[-1])
        #self.reset()



    # get all edges starting with certain state
    def get_state_edge(self, state):
        succs = []
        for edge in self.edges:
            if edge.start == state:
                succs.append(edge)
        return  succs



#transform state name to corresponding position in matrix.
    def trans_to_num(self, name):
        total = 0
        for n in name:
            total = total + ord(n)
        return total - 164


#transform an FSM to a reachbility graph, p is the system hyperperiod
    def trans_to_rea(self, P):
        ins = []
        for p in range(P + 1):
            for period in self.periods:
                if p % period == 0:
                    ins.append(p)

        ins = remove_repeat.remove_repeat(ins)
        ins_to_matrix = {}
        c = 0
        for ii in ins:
            ins_to_matrix[ii] = c
            c = c + 1
        store = []
        for s in self.states:
            store.append(s)
        RG = Rgraph()
        #RG.matrix = [[None for x in range(len(store))] for y in range(len(ins))]
        RG.matrix = [[None for x in range(len(ins))] for y in range(len(store))]
        #for i in range(len(store)):
            #for j in range(P):
                #RG.matrix[i][j] = None
        RG.events = ins
        time = 0
        #temp = 0
        while(ins[time] < P):
            if len(store) != 0:
                #source = store.pop()
                cs = 0
                while(cs < len(store)):
                    source = store[cs]
                    edges = self.get_state_edge(source)
                    for edge in edges:
                #i = 0
                        if ins[time] % edge.event[-1] == 0:
                    #i = i + 1
                            #store.append(edge.end)
                            r = 0
                            #for rl in RG.matrix[time]:
                            for p in range(len(store)):
                                rl = RG.matrix[p][time]
                                if rl is None:
                                    r = r + 1
                                elif rl.name == source.name + str(time) and rl.block == source. block and rl.range == source.range and rl.ins == time:
                                    s = rl
                                else:
                                    r = r + 1
                            if r == len(store):
                                s = Rea_state(source.name + str(time), block = source. block, range = source.range, ins = time)
                        #RG.matrix[self.trans_to_num(source.name)][temp] = s
                                #RG.matrix[time][self.trans_to_num(source.name)] = s
                                RG.matrix[self.trans_to_num(source.name)][time] = s


                            r_e = 0
                            n = time + 1
                            for p_e in range(len(store)):
                                rl_e = RG.matrix[p_e][n]
                                if rl_e is None:
                                    r_e = r_e + 1
                                elif rl_e.name == edge.end.name + str(n) and rl_e.block == source. block and rl_e.range == source.range and rl_e.ins == n:
                                    e = rl_e
                                else:
                                    r_e = r_e + 1
                            if r_e == len(store):
                                e = Rea_state(edge.end.name + str(n), block = edge.end.block, range = edge.end.range, ins = n)
                        #RG.matrix[self.trans_to_num(edge.end.name)][time] = e
                                #RG.matrix[n][self.trans_to_num(edge.end.name)] = e
                                RG.matrix[self.trans_to_num(edge.end.name)][n] = e

                            if e.name in s.succs:
                                wcet = min(s.succs[e.name], edge.action[-1])
                                s.add_succ(e.name, wcet)
                            else:
                                s.add_succ(e.name, -(edge.action[-1]))
                        #store.remove(source)
                                #del store[0]
                    cs = cs + 1

            #else:
                time = time + 1
                #break#if i == len(edges):







                #break
        for x in range(len(store)):
            for y in range(len(ins)):
                if RG.matrix[x][y] == None:
                    RG.matrix[x][y] = Rea_state('s' + str(x + 1) + str(y), block = None, range = '', ins = y)


        for x in range(len(store)):
            for y in range(len(ins) - 1):
                RG.matrix[x][y].add_succ(RG.matrix[x][y + 1].name, 0)


        return RG




class TestBlock(Block):

    def __init__(self, name = 'B1'):
        s1 = State('s1', None, 'x > 1')
        s2 = State('s2', None, 'x > 1')
        s3 = State('s3', None, 'x > 1')
        edge1 = Edge(['e1',4] , ['a1', 2.1], 'o1', '', s1, s2)
        edge2 = Edge(['e1',4] , ['a2', 0.9], 'o2', '', s3, s2)
        edge3 = Edge(['e1',4] , ['a3', 1.5], 'o1', '', s2, s3)
        edge4 = Edge(['e1',4] , ['a4', 1.2], 'o2', '', s2, s1)
        #edge5 = Edge(['e2',5] , ['a5', 0.15], 'o2', '', s1, s2)
        periods = [4]

        super(TestBlock, self).__init__([s1, s2, s3], [edge1, edge2, edge3, edge4], name, periods)



class TestBlock1(Block):

    def __init__(self, name = 'B1'):
        s1 = State('s1', None, 'x > 1')
        s2 = State('s2', None, 'x > 1')
        s3 = State('s3', None, 'x > 1')
        s4 = State('s4', None, 'x > 1')
        edge1 = Edge(['e1',2] , ['a1', 0.9], 'o1', '', s1, s2)
        edge2 = Edge(['e2',2] , ['a2', 1.5], 'o2', '', s2, s3)
        edge3 = Edge(['e1',2] , ['a3', 0.5], 'o1', '', s3, s2)
        edge4 = Edge(['e2',2] , ['a4', 0.8], 'o2', '', s2, s4)
        edge5 = Edge(['e2',2] , ['a4', 1.2], 'o2', '', s3, s1)
        edge5 = Edge(['e2',2] , ['a4', 1.2], 'o2', '', s4, s3)
        periods = [2]

        super(TestBlock1, self).__init__([s1, s2, s3, s4], [edge1, edge2, edge3, edge4, edge5], name, periods)


class TestBlock2(Block):

    def __init__(self, name = 'B1'):
        s1 = State('s1', None, 'x > 1')
        s2 = State('s2', None, 'x > 1')
        s3 = State('s3', None, 'x > 1')
        edge1 = Edge(['e1',3] , ['a1', 0.9], 'o1', '', s1, s2)
        edge2 = Edge(['e2',3] , ['a2', 0.9], 'o2', '', s2, s1)
        edge3 = Edge(['e1',3] , ['a3', 0.9], 'o1', '', s1, s1)
        #edge4 = Edge(['e2',3] , ['a4', 0.9], 'o2', '', s2, s3)
        periods = [3]

        super(TestBlock2, self).__init__([s1, s2, s3], [edge1, edge2, edge3], name, periods)

#combine periods of different state transition graphs
def combine_periods(stateflow):
    period = []
    for s in stateflow:
        for p in s.periods:
            if p not in period:
                period.append(p)
    period = quicksort.qsort(0, len(period) - 1, period)
    period = remove_repeat.remove_repeat(period)
    return period

#combine event instants of different reachability graphs
def combine_instant(stateflow):
    instants = []
    for s in stateflow:
        for p in s.events:
            if p not in instants:
                instants.append(p)
    period = quicksort.qsort(0, len(instants) - 1, instants)
    period = remove_repeat.remove_repeat(period)
    return period

#get the adjacent matrix of a reachbility graph, return the matrix and the match between reachbility graph and matrix
def get_floyd_matrix(RG):
    length = len(RG.matrix) * len(RG.events)
    floyd_matrix = [[float('inf') for x in range(length)] for y in range(length)]
    rea_to_floyd = {}
    z = 0

    while(z <= length - 1):
        for x in range(len(RG.matrix)):
            for y in range(len(RG.events)):
                rea_to_floyd[RG.matrix[x][y].name] = z
                z = z +1

        for x in range(len(RG.matrix)):
            for y in range(len(RG.events) - 1):
                keys = RG.matrix[x][y].succs.keys()
                for key in keys:
                    floyd_matrix[rea_to_floyd[RG.matrix[x][y].name]][rea_to_floyd[key]] = RG.matrix[x][y].succs[key]

        print floyd_matrix

    floyd_matrix = floyd.floyd(floyd_matrix)
    return  [floyd_matrix, rea_to_floyd]

# start, end are event release instant, not the index of the matrix
def compute_dbf(start, end, l):
    dbf = []
    for i in range(len(RG_LIST[l].matrix[0])):
        if start <= RG_LIST[l].events[i] <= end:
            for j in range(len(RG_LIST[l].matrix)):
                print RG_LIST[l].events
                values = RG_LIST[l].matrix[j][i].succs.values()
                for v in values:
                    dbf.append(v)

    return  min(dbf)

# start, end are event release instant, not the index of the matrix
def compute_rbf(start, end, RG, floyd):
    rbf = []
    for p in range(len(RG.events)):
        if RG.events[p] == start:
            st = p
        if RG.events[p] == end:
            ed = p
    for i in range(len(RG.matrix)):
        for j in range(len(RG.matrix)):

            ss = floyd[-1][RG.matrix[i][st].name]
            ee = floyd[-1][RG.matrix[j][ed].name]
            rbf.append(floyd[0][ss][ee])

    return  min(rbf)



#the maximum speed up factor----l_max
l_max = 1
B1 = TestBlock()
B2 = TestBlock1()
B3 = TestBlock2()
#B4 = TestBlock2()
stateflow = [B1, B2, B3]
all_periods = combine_periods(stateflow)
P = lcm.LCM(all_periods)
#RG1 = B1.trans_to_rea(P)
#RG2 = B1.trans_to_rea(P)
#RG3 = B1.trans_to_rea(P)
RG_LIST = []
stateflow_to_RG = {}
floyd_list = []
RG_to_floyd = {}
for s in stateflow:
    RG = s.trans_to_rea(P)
    RG_LIST.append(RG)
    stateflow_to_RG[s] = RG
    f = get_floyd_matrix(RG)
    floyd_list.append(f)
    RG_to_floyd[RG] = f


#compute all instants of the system
instant = []
for rgl in RG_LIST:
    for e in rgl.events:
        if e in instant:
            pass
        else:
            instant.append(e)

instant = quicksort.qsort(0, len(instant) - 1, instant)

#create a new matrix, its first row are all instants of the the system
matrix = [[None for x in range(len(instant))] for y in range(len(RG_LIST) + 1)]
for t in range(len(instant)):
    matrix[0][t] = instant[t]
for i in range(len(RG_LIST)):
    for t in range(len(instant)):
        if instant[t] in RG_LIST[i].events:
            matrix[i + 1][t] = instant[t]
        else:
            matrix[i + 1][t] = -1


for l in range(1, len(RG_LIST)):
    start_times = combine_instant(RG_LIST[0:l])
    match = {}
    for i in range(len(start_times)):
        match[start_times[i]] = i
    for s in start_times[:-2]:
        if s > RG_LIST[l].events[-2]:
            break
        if s in RG_LIST[l].events:
            for e in RG_LIST[l].events:
                if e > s:
                    t = e
                    break

        else:
            c = 0
            for e in RG_LIST[l].events:
                if e > s:
                    if e == P:
                        t = P
                        break
                    else:
                        c = c + 1
                        if c == 2:
                            t = e
                            break

        print s
        print t
        dbf = -compute_dbf(s, t, l)
        t_plus = []
        for t in instant:
            if t > s and t <= e:
                t_plus.append(t)
        n = 0
        local = []
        for tp in t_plus:
            rbf = 0
            for t in range(len(instant)):
                if instant[t] == s:
                    i = t

                if instant[t] == tp:
                    j = t

            #for high in RG_LIST[0: l -1]:
            for high in range(l):
                if i == j - 1:
                    start = matrix[high + 1][i]
                else:
                    for x in range(i, j - 1):
                        if matrix[high + 1][x] != 1:
                            start = matrix[high + 1][x]
                            #s = x
                            break

                if start != -1:
                    x = j
                    while(matrix[high + 1][x] == -1):
                        x = x + 1
                    end = matrix[high + 1][x]
                    #e = x

                    new = -compute_rbf(start, end, RG_LIST[high], RG_to_floyd[RG_LIST[high]])
                    rbf = rbf + new



            if dbf + rbf <= tp - s:
                break
            else:
                n = n + 1
                speedup = (dbf + rbf)/(tp - s)
                local.append(speedup)

        if n == len(t_plus):
            l_max = max(l_max, min(local))


print l_max

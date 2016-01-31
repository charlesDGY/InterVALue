import valueanalysis
import remove_repeat
from ctypes import *
import copy
import lcm
import quicksort
import floyd

libc = CDLL("/home/dgy/Programming/VInterval/libnew_range_analysis.so")
libc.make_context.restype = POINTER(valueanalysis.edge_context)
libc.make_node.restype = POINTER(valueanalysis.interval_node)
libc.make_node.argtype = valueanalysis.interval

libc.new_range_analysis.restype = POINTER(valueanalysis.edge_context)
libc.new_range_analysis.argtypes = [POINTER(valueanalysis.edge_context), c_int, POINTER(POINTER(valueanalysis.cfg_func_t)), c_int]

libc.get_cfg.restype = POINTER(POINTER(valueanalysis.cfg_func_t))
libc.get_cfg.argtypes = [c_char_p, POINTER(c_int)]

libc.get_max_value.restype = c_double

libc.union_context_new.restype = POINTER(valueanalysis.edge_context)
libc.union_context_new.argtypes = [POINTER(valueanalysis.edge_context), POINTER(valueanalysis.edge_context), c_int *1]

libc.is_context_equal.restype = c_int
libc.is_context_equal.argtypes = [POINTER(valueanalysis.edge_context), POINTER(valueanalysis.edge_context)]

libc.copy_context.restype = POINTER(valueanalysis.edge_context)
libc.copy_context.argtype = POINTER(valueanalysis.edge_context)

class State(object):


    def __init__(self, range, name = 'S', block = None):
        self.name = name
        self.succs = {}
        self.block = block
        self.range = range


    def set_block(self, block):
        self.block = block

    def get_block(self):
        return self.block

#transition/edge in the FSM
class Edge(object):

    def __init__(self,  cfg_list, event = ['name', 1], action = ['name', 0], output = 'o', guard = '', start = None, end = None, block = None):
        self.event = event
        self.action = action
        self.output = output
        self.guard = guard
        self.start = start
        self.end = end
        self.block = block
        self.cfg_list = cfg_list

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

    def add_succ(self, job, wcet, condition):
        self.succs[job] = [wcet, condition]

    def set_block(self, block):
        self.block = block

    def get_block(self):
        return self.block


#transition/edge in the reachability graph
class Rea_edge(object):

    def __init__(self, source, guard , start = None, end = None, block = None, range_analysis = None, wcet = 0):
        self.source = source
        self.guard = guard
        self.start = start
        self.end = end
        self.block = block
        self.range_analysis = range_analysis
        self.wcet = wcet

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


def get_state_edge_rea(edges, state):
        succs = []
        if state != None:
            for edge in edges:
                if edge.start.name == state.name:
                    succs.append(edge)
        return  succs

# define the reachability graph as a class, its two attributes: 1. all states with their instants
#2 the periods of events in it.
class Rgraph(object):

    def __init__(self, matrix = [], events = [], edges = []):
        self.matrix = matrix
        self.events = events
        self.edges = edges


class Block(object):

    def __init__(self, states = [], edges = [], name='B', periods = []):
        self.states = states
        self.edges = edges
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




    def trans_to_rea(self, P):
            ins = []
            for p in range(P):
                for period in self.periods:
                    if p % period == 0:
                        ins.append(p)

            ins = remove_repeat.remove_repeat(ins)
            ins_to_matrix = {}

            store = []
            for s in self.states:
                store.append(s)
            RG = Rgraph(matrix = [], events = [], edges = [])
            RG.matrix = [[None for x in range(len(ins) + 1)] for y in range(len(store))]
            RG.events = []
            RG.edges = []

            cycle = 0
            while(True):
                if cycle != 0:
                    print cycle
                    r = 0

                    for i in range(len(store)):
                        if RG.matrix[i][cycle] != None:
                            r = r + 1
                    if r == len(store):
                        eql = 0
                        for s in range(len(store)):
                            print 'low'
                            print RG.matrix[s][cycle *len(ins)].range.contents.next.contents.value_set.contents.next.contents.item.low_value
                            print 'up'
                            print RG.matrix[s][cycle *len(ins)].range.contents.next.contents.value_set.contents.next.contents.item.up_value
                            print RG.matrix[s][0].range.contents.next.contents.value_set.contents.next.contents.item.low_value
                            print RG.matrix[s][0].range.contents.next.contents.value_set.contents.next.contents.item.up_value
                            RG.matrix[s][cycle *len(ins)].range.contents.next.contents.next = POINTER(valueanalysis.edge_context)()
                            RG.matrix[s][0].range.contents.next.contents.next = POINTER(valueanalysis.edge_context)()

                            if libc.is_context_equal(RG.matrix[s][cycle *len(ins)].range, RG.matrix[s][0].range) :
                                eql = eql + 1
                        if eql == len(store):
                            break



                     #ext_matrix =  [None for x in range(len(ins))]
                    for l in range(len(store)):
                         num = 0
                         while(num < len(ins)):

                            RG.matrix[l].append( None)
                            num = num + 1
                     #for l in range(len(store)):
                         #RG.matrix[l][cycle*len(ins) ] = Rea_state(name = store[l].name + str(cycle*len(ins)), block = store[l].block, range = RG.matrix[l][(cycle - 1)*len(ins)].range, ins = cycle*len(ins))
                    pos = 0
                    time = cycle * P + ins[pos]
                    RG.events.append(time)
                    while(time < (cycle + 1) *P):
                     #while(pos <= len(ins)):
                         ins_to_matrix[time] = pos + cycle* len(ins)
                         cs = 0
                         while(cs < len(store)):
                             source = store[cs]
                             edges = self.get_state_edge(source)
                             for edge in edges:

                                 if time % edge.event[-1] == 0:

                                     #end_context = POINTER(valueanalysis.edge_context)
                                     #if (edge.guard != ''):

                                         #print edge.start.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                         #print edge.start.range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                         #end_context = libc.new_range_analysis(edge.start.range, c_int(0), edge.cfg_list[0][0], edge.cfg_list[0][1])
                                     #else:
                                         #end_context = libc.copy_context(edge.start.range)
                                     #if bool(end_context.contents.next):
                                         #print end_context.contents.next.contents.value_set.contents.next.contents.item.low_value
                                         #print end_context.contents.next.contents.value_set.contents.next.contents.item.up_value
                                         #end_context.contents.next.contents.next = POINTER(valueanalysis.edge_context)()


                                         count = (cycle* len(ins)) +pos

                                         #rl = RG.matrix[self.trans_to_num(source.name)][pos]
                                         temp = RG.matrix[self.trans_to_num(source.name)][count]

                                         if temp != None:
                                             end_context = POINTER(valueanalysis.edge_context)
                                             if (edge.guard != ''):
                                                print temp.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                print temp.range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                                end_context = libc.new_range_analysis(temp.range, c_int(0), edge.cfg_list[0][0], edge.cfg_list[0][1])

                                             else:
                                                 end_context = libc.copy_context(temp.range)


                                             if bool(end_context.contents.next):
                                                 print end_context.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                 print end_context.contents.next.contents.value_set.contents.next.contents.item.up_value
                                                 end_context.contents.next.contents.next = POINTER(valueanalysis.edge_context)()
                                                 if bool(end_context.contents.next.contents.next):
                                                     print 5




                                                     #if RG.matrix[self.trans_to_num(source.name)][count] is None:

                                                         #newname = source.name + str(count)
                                                         #rl = Rea_state(name = newname, block = source. block, range = source.range, ins = cycle* len(ins) + pos)
                                                         #RG.matrix[self.trans_to_num(source.name)][count]
                                                         #s = rl
                                                         #print s.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                         #print s.range.contents.next.contents.value_set.contents.next.contents.item.up_value



                                                 s = RG.matrix[self.trans_to_num(source.name)][count]
                                                 print s.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                 print s.range.contents.next.contents.value_set.contents.next.contents.item.up_value


                                                 #run action program

                                                 n = count + 1
                                                 next_input_range = POINTER(valueanalysis.edge_context)
                                                #rl_e = RG.matrix[self.trans_to_num(edge.end.name)][n]
                                                 if (edge.action[0] !=''):
                                                    next_input_range = libc.new_range_analysis(end_context, c_int(1), edge.cfg_list[1][0], edge.cfg_list[1][1])
                                                    print next_input_range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                    print next_input_range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                                 else:
                                                    next_input_range = libc.copy_context(end_context)
                                                    print next_input_range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                    print next_input_range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                                 next_input_range.contents.next.contents.next = POINTER(valueanalysis.edge_context)()
                                                 #rl_e = RG.matrix[self.trans_to_num(edge.end.name)][n]
                                                 #next_input_range = POINTER(valueanalysis.edge_context)
                                                 #next_input_range = libc.new_range_analysis(end_context, c_int(1), edge.cfg_list[1][0], edge.cfg_list[1][1])
                                                 #if len(RG.matrix[self.trans_to_num(edge.end.name)]) < cycle* len(ins) + n + 1:
                                                 if RG.matrix[self.trans_to_num(edge.end.name)][n] is None:
                                                 #if rl_e is None:
                                                     rl_e = Rea_state(name = edge.end.name + str( n), block = edge.end.block, range = next_input_range, ins =  n)
                                                     RG.matrix[self.trans_to_num(edge.end.name)][n]= rl_e
                                                     e = rl_e
                                                     print e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                     print e.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                                 else:
                                                     rl_e = RG.matrix[self.trans_to_num(edge.end.name)][n]

                                                     type_array = c_int * 1
                                                     ii = type_array(c_int(6))
                                                     newrange = libc.union_context_new(rl_e.range, next_input_range, ii)  #source.range-->edge.guard-->action
                                                     print 'no'
                                                     rl_e.range = newrange
                                                     e = rl_e
                                                     print e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                                     print e.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                             #edges = get_state_edge_rea(RG.edges, s)
                                             #if len(edges) != 0:
                                                 #for eg in edges:
                                                     #if libc.is_context_equal(eg.guard, edge.guard):
                                                         #eg.wcet = max(eg.wcet, edge.action[-1])

                                                     #else:
                                                         #RG.edges.append(Rea_edge(guard = edge.guard, start = s, end = e, wcet =edge.action[-1] ))

                                             #else:
                                                 RG.edges.append(Rea_edge(source = edge, guard = edge.guard, start = s, end = e, wcet =edge.action[-1] ))



                             cs = cs + 1






                         pos = pos + 1
                         if pos >= len(ins):
                             pos = 0
                             break
                         else:
                             time = cycle * P + ins[pos]

                    cycle = cycle + 1


                else:
                    print cycle
                    pos = 0
                    time = cycle * P + ins[pos]
                    #if cycle == 0:
                        #for l in range(len(store)):
                            #RG.matrix[l][0] = Rea_state(name = store[l].name + str(0), block = store[l].block, range = store[l].range, ins = 0)

                    while(time < (cycle + 1) *P):
                        RG.events.append(time)
                    #while(pos <= len(ins)):
                        ins_to_matrix[time] = pos + cycle* len(ins)
                        cs = 0
                        while(cs < len(store)):
                            source = store[cs]
                            edges = self.get_state_edge(source)
                            for edge in edges:

                                if time % edge.event[-1] == 0:
                                    end_context = POINTER(valueanalysis.edge_context)
                                    if (edge.guard != ''):

                                        print edge.start.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                        print edge.start.range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                        #print edge.guard.contents.next.contents.value_set.contents.next.contents.item.low_value
                                        #print edge.guard.contents.next.contents.value_set.contents.next.contents.item.up_value
                                        end_context = libc.new_range_analysis(edge.start.range, c_int(0), edge.cfg_list[0][0], edge.cfg_list[0][1])

                                    else:
                                        end_context = libc.copy_context(edge.start.range)

                                    #print end_context.contents.next.contents.value_set.contents.next.contents.item.low_value
                                    #print end_context.contents.next.contents.value_set.contents.next.contents.item.up_value
                                    if bool(end_context.contents.next):
                                        'print end_context.contents.next.contents.value_set.contents.next.contents.item.low_value'
                                        'print end_context.contents.next.contents.value_set.contents.next.contents.item.up_value'
                                        end_context.contents.next.contents.next = POINTER(valueanalysis.edge_context)()

                                        count = cycle* len(ins) +pos

                                        #rl = RG.matrix[self.trans_to_num(source.name)][pos]
                                        if RG.matrix[self.trans_to_num(source.name)][count] is None:

                                            newname = source.name + str(count)
                                            rl = Rea_state(name = newname, block = source. block, range = source.range, ins = cycle* len(ins) + pos)
                                            RG.matrix[self.trans_to_num(source.name)][count]= rl
                                            s = rl
                                            print s.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print s.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                        else:
                                            s = RG.matrix[self.trans_to_num(source.name)][count]
                                            print s.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print s.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                        #run action program

                                        n = count + 1


                                        next_input_range = POINTER(valueanalysis.edge_context)
                                        #rl_e = RG.matrix[self.trans_to_num(edge.end.name)][n]
                                        if (edge.action[0] !=''):
                                            next_input_range = libc.new_range_analysis(end_context, c_int(1), edge.cfg_list[1][0], edge.cfg_list[1][1])
                                            print next_input_range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print next_input_range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                        else:
                                            next_input_range = libc.copy_context(end_context)
                                            print next_input_range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print next_input_range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                        next_input_range.contents.next.contents.next = POINTER(valueanalysis.edge_context)()

                                        #if len(RG.matrix[self.trans_to_num(edge.end.name)]) < cycle* len(ins) + n + 1:
                                        if RG.matrix[self.trans_to_num(edge.end.name)][n] is None:
                                        #if rl_e is None:
                                            rl_e = Rea_state(name = edge.end.name + str( n), block = edge.end.block, range = next_input_range, ins =  n)
                                            RG.matrix[self.trans_to_num(edge.end.name)][n]= rl_e
                                            e = rl_e
                                            print e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print e.range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                        else:
                                            rl_e = RG.matrix[self.trans_to_num(edge.end.name)][n]
                                            print 'no'
                                            print rl_e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print rl_e.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                            type_array = c_int * 1
                                            ii = type_array(c_int(0))
                                            print rl_e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print rl_e.range.contents.next.contents.value_set.contents.next.contents.item.up_value
                                            print next_input_range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print next_input_range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                            newrange = libc.union_context_new(rl_e.range, next_input_range, ii)

                                            #source.range-->edge.guard-->action
                                            rl_e.range = newrange
                                            e = rl_e
                                            print rl_e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print rl_e.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                            print e.range.contents.next.contents.value_set.contents.next.contents.item.low_value
                                            print e.range.contents.next.contents.value_set.contents.next.contents.item.up_value

                                        #edges = get_state_edge_rea(RG.edges, s)
                                        #if len(edges) != 0:
                                            #for eg in edges:
                                                #if libc.is_context_equal(eg.guard, edge.guard):
                                                    #eg.wcet = max(eg.wcet, edge.action[-1])

                                                #else:
                                                    #RG.edges.append(Rea_edge(guard = edge.guard, start = s, end = e, wcet =edge.action[-1] ))

                                        #else:
                                        RG.edges.append(Rea_edge(source = edge, guard = edge.guard, start = s, end = e, wcet = edge.action[-1] ))



                            cs = cs + 1






                        pos = pos + 1
                        if pos >= len(ins):
                            pos = 0
                            break
                        else:
                            time = cycle * P + ins[pos]

                    cycle = cycle + 1
            RG.events.append(cycle * P)
            return RG

#def modify_state_graph(self):
    #for state in self.states:
        #edge = Edge(event = ['name', gcd()], action = ['name', 0], output = 'o', guard = '', start = state, end = state, block = None)
        #self.edges.append(edge)




#get the adjacent matrix of a reachability graph, return the matrix and the match between reachability graph and matrix
def get_floyd_matrix(RG):
    length = 0

    rea_to_floyd = {}
    z = 0
    for x in range(len(RG.matrix)):
            for y in range(len(RG.events)):
                if RG.matrix[x][y] != None:
                    length = length + 1

    floyd_matrix = [[float('inf') for x in range(length)] for y in range(length)]

    while(z <= length - 1):
        for x in range(len(RG.matrix)):
            for y in range(len(RG.events)):
                if RG.matrix[x][y] != None:
                    rea_to_floyd[RG.matrix[x][y].name] = z
                    z = z +1

    for x in range(len(RG.matrix)):
        for y in range(len(RG.events) - 1):
            key = RG.matrix[x][y]
            for edge in get_state_edge_rea(RG.edges, key):
                if key != None:
                    if floyd_matrix[rea_to_floyd[RG.matrix[x][y].name]][rea_to_floyd[edge.end.name]] == float('inf'):
                        floyd_matrix[rea_to_floyd[RG.matrix[x][y].name]][rea_to_floyd[edge.end.name]] = -edge.wcet
                    else:
                        floyd_matrix[rea_to_floyd[RG.matrix[x][y].name]][rea_to_floyd[edge.end.name]] = min(floyd_matrix[rea_to_floyd[RG.matrix[x][y].name]][rea_to_floyd[edge.end.name]], -edge.wcet )

        print floyd_matrix
        floyd.floyd(floyd_matrix)
    return  [floyd_matrix, rea_to_floyd]



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





#copy the hyperperiod to make up the whole system hyperperiod
def copy_periods(RG, sp):
    new_RG = Rgraph(matrix = [], events = [], edges = [])
    l = len(RG.matrix[0]) + (sp/RG.events[-1] - 1) * (len(RG.matrix[0]) - 1)
    new_RG.matrix = [[None for x in range(l)] for y in range(len(RG.matrix))]
    p = RG.events[-1]
    n = sp/RG.events[-1]
    for i in range(len(RG.matrix)):
        for j in range((len(RG.matrix[0]) - 1), l):
            #new_RG.matrix[i][j] = RG.matrix[i][j % len(RG.matrix[0])]
            if RG.matrix[i][j % (len(RG.matrix[0]) - 1)] != None:
                new_RG.matrix[i][j] = State(range, name = RG.matrix[i][j % (len(RG.matrix[0]) - 1)].name, block= RG.matrix[i][j % (len(RG.matrix[0]) - 1)].block)

                c = (j - j% (len(RG.matrix[0]) - 1))/(len(RG.matrix[0]) - 1)
                new_RG.matrix[i][j].name = new_RG.matrix[i][j].name[:2] + str(int(new_RG.matrix[i][j].name[2:]) + c * (len(RG.matrix[0]) - 1))
                if new_RG.matrix[i][j] != None:
                    new_RG.matrix[i][j].range = libc.copy_context(RG.matrix[i][j % (len(RG.matrix[0]) - 1)].range)


    for i in range(len(RG.matrix)):
        for j in range(0, (len(RG.matrix[0]) - 1)):
            #new_RG.matrix[i][j] = RG.matrix[i][j]
            if RG.matrix[i][j % (len(RG.matrix[0]) - 1)] != None:
                new_RG.matrix[i][j] = State(range, name = RG.matrix[i][j % (len(RG.matrix[0]) - 1)].name, block= RG.matrix[i][j % (len(RG.matrix[0]) - 1)].block)
                if new_RG.matrix[i][j] != None:
                    new_RG.matrix[i][j].range = libc.copy_context(RG.matrix[i][j].range)

    for c in range(1, n):
        for e in range(len(RG.events)):
            new_RG.events.append(RG.events[e] + c * p)

    #new_RG.events.append(sp)
    remove_repeat.remove_repeat(new_RG.events)
    new_RG.events = RG.events[:-1] + new_RG.events


    #for edge in RG.edges:
        #new_RG.edges.append(None)

    #for i in range(len(RG.edges)):
        #new_RG.edges[i] = RG.edges[i]

    new_RG.edges = []

    for edge in RG.edges:
        for c in range(0, n):
            newstart = State(range, name = edge.start.name, block= edge.start.block)
            newend = State(range, name = edge.end.name, block= edge.end.block)
            newedge = Rea_edge(source = edge.source, guard = edge.guard, start = newstart, end = newend, wcet= edge.wcet, block = edge.block, range_analysis= edge.range_analysis)
            #newedge.block = copy.deepcopy(edge.block)
            #newedge.guard = copy.deepcopy(edge.guard)
            #newedge.wcet = copy.deepcopy(edge.wcet)
            #newedge.range_analysis = copy.deepcopy(edge.range_analysis)
            #newedge.start = edge.start
            #newedge.end = edge.end
            #newedge.source = edge.source

            #newedge.start.block = edge.start.block
            #newedge.start.ins = edge.start.ins
            #newedge.start.name = edge.start.name[:2] + str(int(newedge.start.name[2:]) + c * len(RG.matrix[0]))
            #newedge.start.succs = edge.start.succs
            newedge.start.range = libc.copy_context(edge.start.range)
            newedge.start.name = newedge.start.name[:2] + str(int(newedge.start.name[2:]) + c * (len(RG.matrix[0]) - 1))


            #newedge.end.block = edge.end.block
            #newedge.end.ins = edge.end.ins
            #newedge.end.name = edge.end.name[:2] + str(int(newedge.end.name[2:]) + c * len(RG.matrix[0]))
            #newedge.end.succs = edge.end.succs
            newedge.end.range = libc.copy_context(edge.end.range)
            newedge.end.name = newedge.end.name[:2] + str(int(newedge.end.name[2:]) + c * (len(RG.matrix[0]) - 1))


            new_RG.edges.append(newedge)


    return  new_RG


class TestBlock(Block):

    def __init__(self, name = 'B1'):


        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(2), c_double(3))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i


        s1 = State(input_value_range,'s1', None)

        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(1), c_double(2))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i



        s2 = State(input_value_range,'s2', None)

        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(2), c_double(3))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i



        s3 = State(input_value_range,'s3', None)

        edge1 = Edge([], ['e1',4] , ['1_action2', 2.1],  'o1', '', s1, s2, None)
        edge2 = Edge([], ['e1',4] , ['1_action3', 0.9], 'o2', '1_condition3', s2, s3, None)
        edge3 = Edge([],['e1',4] , ['1_action4', 1.5], 'o1', '', s3, s2, None)
        edge4 = Edge([],['e1',4] , ['1_action1', 1.2], 'o2', '1_condition1', s2, s1, None)
        #edge5 = Edge(['e2',5] , ['a5', 0.15], 'o2', '', s1, s2)
        periods = [4]

        super(TestBlock, self).__init__([s1, s2, s3], [edge1, edge2, edge3, edge4], name, periods)


class TestBlock1(Block):

    def __init__(self, name = 'B2'):


        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(3), c_double(3))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i


        s1 = State(input_value_range,'s1', None)

        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(1), c_double(1))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i



        s2 = State(input_value_range,'s2', None)

        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(0), c_double(0))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i



        s3 = State(input_value_range,'s3', None)

        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(0), c_double(0))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i



        s4 = State(input_value_range,'s4', None)

        edge1 = Edge([], ['e3',2] , ['', 0.9], 'o1', '', s1, s2)
        edge2 = Edge([],['e3',2] , ['2_action2', 1.5], 'o2', '2_condition2', s2, s3)
        edge3 = Edge([],['e3',2] , ['2_action1', 0.5], 'o1', '2_condition1', s3, s2)
        edge4 = Edge([],['e3',2] , ['2_action5', 0.8], 'o2', '2_condition5', s2, s4)
        edge5 = Edge([],['e3',2] , ['2_action3', 1.2], 'o2', '2_condition3', s3, s1)
        edge6 = Edge([],['e3',2] , ['', 1.2], 'o2', '', s4, s3)
        #edge5 = Edge(['e2',5] , ['a5', 0.15], 'o2', '', s1, s2)
        periods = [2]

        super(TestBlock1, self).__init__([s1, s2, s3, s4], [edge1, edge2, edge3, edge4, edge5, edge6], name, periods)

class TestBlock2(Block):

    def __init__(self, name = 'B3'):


        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(1), c_double(libc.get_max_value()))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i


        s1 = State(input_value_range,'s1', None)

        input_value_range = libc.make_context()
        input_i = libc.make_context()
        input_i.contents.name_d = c_int(0)
        item = valueanalysis.interval(c_double(4), c_double(libc.get_max_value()))
        input_i.contents.value_set.contents.next = libc.make_node(item)
        input_value_range.contents.next = input_i



        s2 = State(input_value_range,'s2', None)



        edge1 = Edge([],['e4',3] , ['', 0.9], 'o1', '3_condition2', s1, s2)
        edge2 = Edge([],['e4',3] , ['3_action3', 0.9], 'o2', '', s2, s1)
        edge3 = Edge([],['e5',3] , ['3_action1', 0.9], 'o1', '3_condition1', s1, s1)

        #edge5 = Edge(['e2',5] , ['a5', 0.15], 'o2', '', s1, s2)
        periods = [3]

        super(TestBlock2, self).__init__([s1, s2], [edge1, edge2, edge3], name, periods)



r = "/home/dgy/Programming/VInterval/codes/"


B2 = TestBlock1()
B3 = TestBlock2()
B1 =TestBlock()


for f1 in range(len(B1.edges)):
    edge = B1.edges[f1]
    if (edge.guard != ''):
        location = r + edge.guard + ".c.004t.gimple"
        fp = c_char_p(location)
        print location

        condition_cfg = POINTER(POINTER(valueanalysis.cfg_func_t))
        num = POINTER(c_int)(c_int(0))
        condition_cfg = libc.get_cfg(fp, num)

        edge.cfg_list.append([condition_cfg, num.contents])
    else:
        edge.cfg_list.append([1, 1])

    if (edge.action[0] != ''):
        location = r + edge.action[0] + ".c.004t.gimple"
        print location
        fp = c_char_p(location)

        action_cfg = POINTER(POINTER(valueanalysis.cfg_func_t))
        num = POINTER(c_int)(c_int(0))
        action_cfg = libc.get_cfg(fp, num.contents)

        edge.cfg_list.append([action_cfg, num.contents])


for f2 in range(len(B2.edges)):
    edge = B2.edges[f2]
    if (edge.guard != ''):
        location = r + edge.guard + ".c.004t.gimple"
        fp = c_char_p(location)
        print location

        condition_cfg = POINTER(POINTER(valueanalysis.cfg_func_t))
        num = POINTER(c_int)(c_int(0))
        condition_cfg = libc.get_cfg(fp, num)

        edge.cfg_list.append([condition_cfg, num.contents])
    else:
        edge.cfg_list.append([1, 1])

    if (edge.action[0] != ''):
        location = r + edge.action[0] + ".c.004t.gimple"
        print location
        fp = c_char_p(location)

        action_cfg = POINTER(POINTER(valueanalysis.cfg_func_t))
        num = POINTER(c_int)(c_int(0))
        action_cfg = libc.get_cfg(fp, num.contents)

        edge.cfg_list.append([action_cfg, num.contents])


for f in range(len(B3.edges)):
    edge = B3.edges[f]
    if (edge.guard != ''):
        location = r + edge.guard + ".c.004t.gimple"
        fp = c_char_p(location)
        print location

        condition_cfg = POINTER(POINTER(valueanalysis.cfg_func_t))
        num = POINTER(c_int)(c_int(0))
        condition_cfg = libc.get_cfg(fp, num)

        edge.cfg_list.append([condition_cfg, num.contents])
    else:
        edge.cfg_list.append([1, 1])

    if (edge.action[0] != ''):
        location = r + edge.action[0] + ".c.004t.gimple"
        print location
        fp = c_char_p(location)

        action_cfg = POINTER(POINTER(valueanalysis.cfg_func_t))
        num = POINTER(c_int)(c_int(0))
        action_cfg = libc.get_cfg(fp, num.contents)

        edge.cfg_list.append([action_cfg, num.contents])


#rg = B1.trans_to_rea(4)
#result = get_floyd_matrix(rg)
#copy_periods(rg, 24)

#print result




#the maximum speed up factor----l_max
l_max = 1
#B1 = TestBlock()
#B2 = TestBlock1()
#B3 = TestBlock2()
#B4 = TestBlock2()
stateflow = [B1, B2, B3]
RG2_A = B2.trans_to_rea(2)
RG1_A = B1.trans_to_rea(4)

RG3_A = B3.trans_to_rea(3)

P = lcm.LCM([RG1_A.events[-1], RG2_A.events[-1], RG3_A.events[-1]])
RG1 = copy_periods(RG1_A, P)
RG2 = copy_periods(RG2_A, P)
RG3 = copy_periods(RG3_A, P)


RG_LIST = [RG1, RG2, RG3]
#RG1 = B1.trans_to_rea(P)
#RG2 = B1.trans_to_rea(P)
#RG3 = B1.trans_to_rea(P)
#RG_LIST = []
stateflow_to_RG = {}
floyd_list = []
RG_to_floyd = {}
stateflow_to_RG = {B1:RG1, B2:RG2, B3:RG3 }
floyd_list = [get_floyd_matrix(RG1), get_floyd_matrix(RG2), get_floyd_matrix(RG3)]
RG_to_floyd = {RG1:floyd_list[0], RG2:floyd_list[1], RG3:floyd_list[2]}
#for s in stateflow:
    #RG = s.trans_to_rea(P)
    #RG_LIST.append(RG)
    #stateflow_to_RG[s] = RG
    #f = get_floyd_matrix(RG)
    #floyd_list.append(f)
    #RG_to_floyd[RG] = f


#compute all instants of the system
instant = []
for rgl in RG_LIST:
    for e in rgl.events:
        if e in instant:
            pass
        else:
            instant.append(e)

instant = quicksort.qsort(0, len(instant) - 1, instant)
# start, end are event release instant, not the index of the matrix
def compute_dbf(start, end, l):
    dbf = []
    for i in range(len(RG_LIST[l].matrix[0])):
        if start <= RG_LIST[l].events[i] <= end:
            for j in range(len(RG_LIST[l].matrix)):
                print RG_LIST[l].events
                for edge in get_state_edge_rea(RG_LIST[l].edges, RG_LIST[l].matrix[j][i]):
                    dbf.append(edge.wcet)
                #values = RG_LIST[l].matrix[j][i].succs.values()
                #for v in values:
                    #dbf.append(v)

    return  min(dbf)

# start, end are event release instant, not the index of the matrix
def compute_rbf(start, end, RG):

    for p in range(len(RG.events)):
        if RG.events[p] == start:
            st = p
        if RG.events[p] == end:
            ed = p

    fresh = []
    store = []
    interval = RG.events[1] - RG.events[0]
    for i in range(len(RG.matrix)):
        for edge in get_state_edge_rea(RG.edges, RG.matrix[i][st]):
            fresh.append([0, start, RG.matrix[i][st].name,RG.matrix[i][st].range])

    while(True):
        if len(fresh) != 0:
            path = fresh.pop()
            store.append(path)

            for edge in RG.edges:
                if edge.start.name == path[2]:
                    if path[1] + interval <= end:
                        if (edge.guard != ''):

                            end_context = libc.new_range_analysis(path[-1], c_int(0), edge.source.cfg_list[0][0], edge.source.cfg_list[0][1])

                        else:
                            end_context = libc.copy_context(path[-1])


                        if bool(end_context.contents.next):
                            store.append(path)
                            end_context.contents.next.contents.next = POINTER(valueanalysis.edge_context)()
                            next_input_range = POINTER(valueanalysis.edge_context)
                                        #rl_e = RG.matrix[self.trans_to_num(edge.end.name)][n]
                            if (edge.source.action[0] !=''):
                                next_input_range = libc.new_range_analysis(end_context, c_int(1), edge.source.cfg_list[1][0], edge.source.cfg_list[1][1])

                            else:
                                next_input_range = libc.copy_context(valueanalysis.end_context)
                            print 'gogogo'
                            next_input_range.contents.next.contents.next = POINTER(valueanalysis.edge_context)()
                            fresh.append([edge.wcet, path[1] + interval, edge.end.name, next_input_range])

        else:
            break
    result = []
    for s in store:
        result.append(s[0])
    return  max(result)


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
        dbf = compute_dbf(s, t, l)
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

                    #new = -compute_rbf(start, end, RG_LIST[high], RG_to_floyd[RG_LIST[high]])
                    print 111111111111
                    new = compute_rbf(start, end, RG_LIST[high])
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


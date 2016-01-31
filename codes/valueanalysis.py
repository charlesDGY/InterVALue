'''class ReachabilityGraph(object):

    def __init__(self, stategraph):
        self.stategraph = stategraph
        self.get_ReachabilityGraph()
        print self.stategraph
        print self.reachabilitygraph

    def get_ReachabilityGraph(self):
'get reachability graph'
        self.reachabilitygraph = [1]

    def get_WeightMatrix(self):

class ScheduleAnalysis(object):

    def __init__(self):
        print 3

    def method1_analysis(self):

    def mathod2_analysis(self):

    def method3_analysis(self):


re = ReachabilityGraph(4)'''

'''class interval(object):

    def __init__(self, low_value = 0, up_value = 0):
        self.low = low_value
        self.up = up_value

    def get_low(self):
        return self.low

    def get_up(self):
        return self.up

class intervalset(object):

    def __init__(self, intervalset):
        self.intervalset = intervalset

    def get_intervalset(self):
        return self.intervalset

class edgenode(object):

    def __init__(self, intervalset, name = 0):
        self.name = name
        self.intervalset = intervalset

    def get_edgenodename(self):
        return self.name

    def get_edgenodeintervalset(self):
        return self.intervalset

class edgecontext(object):

    def __init__(self, edgenodes):
        self.edgecontext = edgenodes

    def get_edgecontext(self):
        return self.edgecontext
'''

from ctypes import *

class interval(Structure):
    _fields_ = [("low_value", c_double),("up_value", c_double)]

class interval_node(Structure):
    pass
interval_node._fields_ = [("item", interval),("next", POINTER(interval_node))]

class edge_context(Structure):
    pass
edge_context._fields_ = [("name_d", c_int),
                         ("value_set", POINTER(interval_node)),
                         ("next", POINTER(edge_context))]

class declaration_t(Structure):
    _fields_ = [("name",c_char_p),
                ("variable_type",c_int),
                ("is_pointer",c_int),
                ("is_array",c_int),
                ("is_struct",c_int),
                ("struct_name",c_char_p),
                ("is_static",c_int),
                ("array_len",c_int),
                ("effect_domain",c_int)]

class assignment_t(Structure):
    _fields_ = [("dst_name",c_int),
                ("operator_a",c_char_p),
                ("operator_b",c_char_p),
                ("operand",c_char_p),
                ("is_type_convert",c_int),
                ("a_is_var",c_int),
                ("b_is_var",c_int),
                ("has_array",c_int),
                ("array_offset",c_char_p),
                ("offset_is_var",c_int)]


class if_test_t(Structure):
    _fields_ = [("cmp_a",c_char_p),
                ("cmp_b",c_char_p),
                ("cmp_operand",c_char_p),
                ("a_is_var",c_int),
                ("b_is_var",c_int)]

class case_t(Structure):
    _fields_ = [("case_number",c_int),
                ("token_name",c_char_p)]

class switch_test_t(Structure):
    _fields_ = [("switch_var",c_int),
                ("case_chain",POINTER(case_t)*128),
                ("case_num",c_int)]

class call_argument(Structure):
    _fields_ = [("arg_name",c_char_p),
                ("arg_type",c_int),
                ("is_pointer",c_int),
                ("is_struct",c_int),
                ("struct_name",c_char_p)]

class call_parameter(Structure):
    _fields_ = [("var_number",c_char_p),
                ("is_var",c_int)]

class call_t(Structure):
    _fields_ = [("dst_name",c_int),
                ("func_number",c_int),
                ("parameter_num",c_int),
                ("actual_parameter",POINTER(call_parameter) *20)]



class return_t(Structure):
    _fields_ = [("return_num",c_char_p),
                ("return_is_var",c_int)]

class cfg_edge_t(Structure):
    pass
class cfg_node_t(Structure):
    pass

cfg_edge_t._fields_ = [("edge_id", c_int),
                       ("start_node", POINTER(cfg_node_t)),
                       ("end_node", POINTER(cfg_node_t)),
                       ("context_set",POINTER(edge_context))]

cfg_node_t._fields_ = [("node_id", c_int),
                       ("pre_edges_num", c_int),
                       ("succ_edges_num", c_int),
                       ("pre_edges",POINTER(cfg_edge_t) *64),
                       ("succ_edges", POINTER(cfg_edge_t) *64),
                       ("node_type",c_int),
                       ("is_if_junction",c_int),
                       ("loop_times",c_int),
                       ("call_i",POINTER(call_t)),
                       ("assignment_i", POINTER(assignment_t)),
                       ("if_test_i", POINTER(if_test_t)),
                       ("switch_test_i", POINTER(switch_test_t)),
                       ("return_i", POINTER(return_t))]


class token_list(Structure):
    _fields_ = [("token_name",c_char_p),
                ("pointer",POINTER(cfg_node_t)),
                ("while_pointer",POINTER(cfg_node_t))]

class cfg_func_t(Structure):
    _fields_ = [("func_name",c_char_p),
                ("func_num",c_int),
                ("edge_num",c_int),
                ("node_num",c_int),
                ("var_num",c_int),
                ("all_edges",POINTER(cfg_edge_t) *64),
                ("all_nodes",POINTER(cfg_node_t) *64),
                ("input_argument", POINTER(call_argument) *20),
                ("func_vars_table", POINTER(declaration_t) *1024),
                ("pre_entry",POINTER(cfg_edge_t)),
                ("exist_token_num",c_int),
                ("need_token_num",c_int),
                ("exist_tokens",POINTER(token_list) *1024),
                ("need_tokens",POINTER(token_list) *1024)]


libc = CDLL("/home/dgy/Programming/VInterval/libnew_range_analysis.so")
libc.make_context.restype = POINTER(edge_context)
libc.make_node.restype = POINTER(interval_node)
libc.make_node.argtype = interval

libc.new_range_analysis.restype = POINTER(edge_context)
libc.new_range_analysis.argtypes = [POINTER(edge_context), c_int, POINTER(POINTER(cfg_func_t)), c_int]

libc.get_cfg.restype = POINTER(POINTER(cfg_func_t))
libc.get_cfg.argtypes = [c_char_p, POINTER(c_int)]

libc.get_max_value.restype = c_double

libc.union_context_new.restype = POINTER(edge_context)
libc.union_context_new.argtypes = [POINTER(edge_context), POINTER(edge_context), c_int *1]

libc.is_context_equal.restype = c_int
libc.is_context_equal.argtypes = [POINTER(edge_context), POINTER(edge_context)]

libc.copy_context.restype = POINTER(edge_context)
libc.copy_context.argtype = POINTER(edge_context)



fp = c_char_p("/home/dgy/Programming/VInterval/simpletest.c.004t.gimple")

'func_actual_arg = POINTER(edge_context)'
'input_i = POINTER(edge_context)'

result_cfg = POINTER(POINTER(cfg_func_t))
num = POINTER(c_int)(c_int(1))

result_cfg = libc.get_cfg(fp, num)



func_actual_arg = libc.make_context()
input_i = libc.make_context()
input_i.contents.name_d = c_int(0)
item = interval(c_double(-5), c_double(10))
input_i.contents.value_set.contents.next = libc.make_node(item)
func_actual_arg.contents.next = input_i

end_context = POINTER(edge_context)
end_context = libc.new_range_analysis(func_actual_arg, c_int(0), result_cfg, num.contents)
end_context2 = POINTER(edge_context)
end_context2 = libc.copy_context(end_context)
end_context3 = POINTER(edge_context)

type_array = c_int * 1
ii = type_array(c_int(6))
end_context3 = libc.union_context_new(end_context, end_context2, ii)
if (libc.is_context_equal(end_context2, end_context3)):
    print "4444"
print end_context.contents.next.contents.value_set.contents.next.contents.item.low_value



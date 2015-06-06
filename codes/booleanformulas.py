import subprocess

def list_to_str(l):

    if len(l) == 0:
        return ""
    tmp = l[0].__str__()
    for s in l[1:]:
        tmp = tmp + ", " + s.__str__()
    return tmp

substcounter = 0

def newsubst(fstring="SUBST%d"):
    global substcounter

    substcounter = substcounter + 1
    return BF_variable(fstring % substcounter)


def makevar(x):

    if x.is_literal():
        return ([], x)
    
    # Now x is BF_and or BF_or.

    if (type(x) != BF_and) and (type(x) != BF_or):
        raise RuntimeError("Unknown node type.")

    clauses = []
    newchilds = []
    for c in x.childs:
        (addclauses, newc) = makevar(c)
        newchilds.append(newc)
        clauses = clauses + addclauses

    s = newsubst()

    if type(x) == BF_and:
        clauses.append(BF_or([s] + [BF_not(c) for c in newchilds]))
        clauses = clauses + [BF_or([BF_not(s), c]) for c in newchilds]

    elif type(x) == BF_or:
        clauses.append(BF_or([BF_not(s)] + newchilds))
        clauses = clauses + [BF_or([s, BF_not(c)]) for c in newchilds]

    return (clauses, s)


class BF(object):
    """Represents a boolean formula which is a DAG of
    AND, OR, NOT and Variable vertices with leaf iff Variable.
    """

    def __init__(self):
        self.childs = []
        self.satmap = None

    def treeapply(self, fbefore=lambda o, r: r, fafter=lambda o, r: r, startval=None, tf=lambda o, r: True):
        """ Applies fbefore on node before and fafter on node after 
        calling treeapply() on all children. 
        Returns the result of fafter after that call.
        Assumes that fbefore and fafter have signature f(obj, res) with:
         * obj is a tree node
         * res is result of previous treeapply
        Supplies startval as initial result.
        Optional tf a test whether to actually deal with this 
        node or abort instead. Signature tf(obj, res).
        """
        if tf(self, startval):
#            print "[DEBUG] Working on this node: ", self
            res = startval
            res = fbefore(self, res)
            res = fafter(self, res)
            return res
        else:
#            print "[DEBUG] Skipping this node: ", self
            return startval

    def dagapply(self, fbefore=lambda o, r: r, fafter=lambda o, r: r, startval=None):

        def newfbefore(obj, newres):
            (res, visited) = newres
            res = fbefore(obj, res)
            return (res, visited)

        def newfafter(obj, newres):
            (res, visited) = newres
            res = fafter(obj, res)
            visited.add(obj)
            return (res, visited)

        def tf(obj, res):
            (_, visited) = res
#            if obj in visited:
#                print "[DEBUG] This test succeeded: ", obj
#            else:
#                print "[DEBUG] This test failed: ", obj
            return not (obj in visited)

#        return self.treeapply(newf, (startval, set()), tf)
        (res, _) = self.treeapply(newfbefore, newfafter, (startval, set()), tf)
        return res


    def is_CNF(self):
        return False

    def is_clause(self):
        return False

    def is_literal(self):
        return False

    def is_variable(self):
        return False

    def collect_variables(self):
        def f(o, r): 
            if o.is_variable(): 
                r.add(o)
            return r
        return self.dagapply(f, startval=set())

    def to_smt2_str(self):
        def f1(obj, res):
            if isinstance(obj, BF_variable):
                return res + (" (%s)" % obj.name)
            elif isinstance(obj, BF_and):
                return res + " (and"
            elif isinstance(obj, BF_or):
                return res + " (or"
            elif isinstance(obj, BF_not):
                return res + " (not"
            else:
                return res
        
        def f2(obj, res):
            if isinstance(obj, BF_and):
                return res + ")"
            elif isinstance(obj, BF_or):
                return res + ")"
            elif isinstance(obj, BF_not):
                return res + ")"
            else:
                return res
        
        return self.treeapply(fbefore = f1, fafter = f2, startval = "")


    def CNF(self, debug=False):
        """ Returns a CNF version of the formula which is equisatisfiable.
        Steps are:
        (1) Remove/propagate constants.
        (2) Push negations as far down as possible.
        (3) Flatten the AND/OR structure (e.g. flatten nested ANDs).
        (4) Apply Tseitin transformation.
        (5) Clean up double negated variables.
        """

        f0 = self.remove_constants()
        f1 = f0.negations_downwards()
        f2 = f1.flatten_and_or()
        f3 = f2.tseitinize()
        # We may have double negated variables at this point.
        f4 = f3.negations_downwards()
        
        if debug:
            return (self, f0, f1, f2, f3, f4)
        else:
            return f4


    def is_satisfiable_naive(self):
        """ Checks satisfiability of boolean formula. Naive brute force.
        """
        def sat(f, m, v):
            """ Returns whether f is satisfiable with partial variable 
            assignment m and free variables v
            """

            if len(v) == 0:
#                if f.value(m):
#                    print m
                if f.value(m):
                    self.satmap = m
                    return True
                else:
                    return False

            v2 = v.copy()
            x = v2.pop()
            m2 = m.copy()
#            print "Setting %s to True." % x
            m2[x] = True
            if sat(f, m2, v2):
                return True
#            print "Setting %s to False." % x
            m2[x] = False
            if sat(f, m2, v2):
                return True
            return False

        v = self.collect_variables()

        return sat(self, {}, v)


    def is_satisfiable_minisat(self):
        """ Checks satisfiability of boolean formula by calling minisat solver.
        """

        if not self.is_CNF():
            raise RuntimeError("Formula not in CNF.")

        vs = self.collect_variables()

        if len(vs) == 0:
            # This formula does not contain variables.
            if self.value({}):
                self.satmap = {}
                return True
            else:
                return False

        i = 1
        ids = {}
        ids_reverse = {}
        for v in vs:
            ids[v] = i
            ids_reverse[i] = v
            i = i + 1

        minisat_infile = "/tmp/minisat-in"
        minisat_outfile = "/tmp/minisat-out"
        with open(minisat_infile, "w") as f:
            f.write("p cnf %d %d\n" % (len(vs), len(self.childs)))

            for c in self.childs:
                for l in c.childs:
                    if l.is_variable():
                        f.write("%d " % ids[l])
                    else:
                        f.write("-%d " % ids[l.childs[0]])
                f.write("0\n")

        r = subprocess.call(["minisat", minisat_infile, minisat_outfile])

        if r == 10:
            # Formula was satisfiable. Extract variable assignment.

            with open(minisat_outfile, "r") as f:
                m = {}
                if f.readline() == "SAT\n":
                    a = f.readline()
                    i = 1
                    for x in a.split(' ', len(vs)+1):
                        if x == str(i):
                            m[ids_reverse[i]] = True
                        elif x == "-" + str(i):
                            m[ids_reverse[i]] = False
                        elif i <= len(vs):
                            raise RuntimeError("Couldn't parse '%s' in %s." %
                                (x, minisat_outfile))
                        i = i + 1
                    self.satmap = m
                else:
                    raise RuntimeError("Unexpected contents of minisat result file.")

            return True
        elif r == 20:
            return False
        else:
            raise RuntimeError("Error in minisat call.")

    def is_satisfiable(self):

        myvars = self.collect_variables()
        if self.is_CNF():
            f = self
        else:
            f = self.CNF()
        result = f.is_satisfiable_minisat()

        if result and f != self:
            self.satmap = dict()
            for v in myvars:
                if not v in f.satmap:
                    raise RuntimeError("Odd, %s is not a variable in f.satmap." % str(v))
                self.satmap[v] = f.satmap[v]
        if not result:
            self.satmap = None

        return result

    def get_satmap(self):

        return self.satmap
        
    def value(self, m):
        raise NotImplementedError

    def remove_constants(self):
        return self.dagapply(
            fafter=remove_constants_traversal, 
            startval=dict())[self]

    def negations_downwards(self):
        (d, _) = self.dagapply(fafter=negations_downwards_traversal, 
            startval=(dict(), dict()))
        return d[self]

    def flatten_and_or(self):
        return self.dagapply(
            fafter=flatten_and_or_traversal, 
            startval=dict())[self]

    def simplify(self):
        return self.remove_constants().negations_downwards().flatten_and_or()

    def tseitinize(self):

        f = self

        # Trivial cases: leafs or literals
        if type(f) == BF_leaf or f.is_literal():
            return BF_and([BF_or([f])])
    
        # Make sure we have a top-most AND.
        if type(f) == BF_or:
            f = BF_and([f])

        # Now we are BF_and. Just turn all childs into clauses.

        subst = dict()
        clauses = []

        # First, handle literals and clauses

        for c in filter(lambda c: c.is_clause(), f.childs):
            clauses.append(c)
        for c in filter(lambda c: c.is_literal(), f.childs):
            clauses.append(BF_or([c]))

        # Second, handle remaining non-clauses

        for c in filter(lambda c: not (c.is_clause() or c.is_literal()), f.childs):

            # Sanity check: c must be BF_or here.
            if type(c) != BF_or:
                raise RuntimeError("Unexpected node type.")

            # Create substitute variables (and clauses) for all nodes below c
            (subst, clauses) = c.dagapply(
                fafter=tseitinize_traversal, 
                startval=(subst, clauses))

            # Create actual clause using substitutes for its child nodes
            clauses.append(BF_or([subst[c2] for c2 in c.childs]))

        return BF_and(clauses)


 

class BF_innernode(BF):

    def treeapply(self, fbefore=lambda o, r: r, fafter=lambda o, r: r, startval=None, tf=lambda o, r: True):
        if tf(self, startval):
#            print "[DEBUG] Working on this node: ", self
            res = startval
            res = fbefore(self, res)
            for c in self.childs:
                res = c.treeapply(fbefore, fafter, res, tf)
            res = fafter(self, res)
            return res
        else:
#            print "[DEBUG] Skipping this node: ", self
            return startval


class BF_leaf(BF):

    def is_literal(self):
        return True


class BF_variable(BF_leaf):

    def __init__(self, name):
        super(BF_variable, self).__init__()
        self.name = name

    def __str__(self):
        return "<" + self.name + ">"

    def is_variable(self):
        return True

    def value(self, m):
        return m[self];


class BF_constant(BF_leaf):

    def is_variable(self):
        return False


class BF_true(BF_constant):

    def __str__(self):
        return "TRUE"

    def value(self, m):
        return True;


class BF_false(BF_constant):

    def __str__(self):
        return "FALSE"

    def value(self, m):
        return False;


class BF_and(BF_innernode):

    def __init__(self, childs):
        super(BF_and, self).__init__()
        if type(childs) != list:
            childs = [childs]
        self.childs = childs

    def __str__(self):
        return "AND (" + list_to_str(self.childs) + ")"

    def is_CNF(self):
        return reduce(lambda x, y: x and y.is_clause(), self.childs, True)

    def value(self, m):
        return reduce(lambda x, y: x and y.value(m), self.childs, True)


class BF_or(BF_innernode):

    def __init__(self, childs):
        super(BF_or, self).__init__()
        if type(childs) != list:
            childs = [childs]
        self.childs = childs

    def __str__(self):
        return "OR (" + list_to_str(self.childs) + ")"

    def is_clause(self):
        return reduce(lambda x, y: x and y.is_literal(), self.childs, True)

    def value(self, m):
        return reduce(lambda x, y: x or y.value(m), self.childs, False)


class BF_not(BF_innernode):

    def __init__(self, child):
        super(BF_not, self).__init__()
        self.childs = [child]

    def __str__(self):
        return "NOT " + self.childs[0].__str__()

    def is_literal(self):
        return self.childs[0].is_variable()

    def value(self, m):
        return not self.childs[0].value(m)


def BF_iff(a, b):

    return BF_and([BF_or([BF_not(a), b]), BF_or([a, BF_not(b)])])

def is_equivalent(a, b):

    return not BF_not(BF_iff(a, b)).is_satisfiable()


def BF_pattern1(a, b, c, d):
    """ Returns a set of clauses representing a IFF ((b AND c) OR d)
    if all parameters are literals.
    """

    clauses = []

    clauses.append(BF_or([BF_not(a), b, d]))
    clauses.append(BF_or([BF_not(a), c, d]))
    clauses.append(BF_or([a, BF_not(b), BF_not(c)]))
    clauses.append(BF_or([a, BF_not(d)]))

    return clauses


def BF_pattern2(a, b, c, d):
    """ Returns a set of clauses representing a IFF ((b AND c) OR (NOT b AND d))
    if all parameters are literals.
    """

    clauses = []

    clauses.append(BF_or([BF_not(a), b, d]))
    clauses.append(BF_or([BF_not(a), BF_not(b), c]))
    clauses.append(BF_or([BF_not(a), c, d]))
    clauses.append(BF_or([a, BF_not(b), BF_not(c)]))
    clauses.append(BF_or([a, b, BF_not(d)]))

    return clauses


def BF_pattern3(a, b):
    """ Returns a set of clauses representing a IFF (b[0] AND ... AND b[-1])
    if all parameters are literals.
    """

    clauses = []

    clauses += [BF_or([BF_not(a), x]) for x in b]
    clauses.append(BF_or([a] + [BF_not(x) for x in b]))

    return clauses


def BF_atleast(k, v):
    """ True iff at least k of the vars in v are true.
    """

    # We do this iteratively since a recursive version could hit
    # Pythons maximal recursion depth. Likely faster anyway.
    bigtable = {}

    for l in range(len(v) + 1):
        for j in range(k + 1):
            if j > l:
                bigtable[(j, l)] = BF_false()
            elif j == 0:
                bigtable[(j, l)] = BF_true()
            else:
                # 0 < j <= l
                bigtable[(j, l)] = BF_or([BF_and([v[l-1], bigtable[(j-1, l-1)]]),
                    bigtable[(j, l-1)]])

    return bigtable[(k, len(v))]


def BF_atmost(k, v):
    """ True iff at most k of the vars in v are true.
    """

    bigtable = {}

    # We do this iteratively since a recursive version could hit
    # Pythons maximal recursion depth. Likely faster anyway.
    for l in range(len(v) + 1):
        for j in range(k + 1):
            if j > l or l == 0:
                bigtable[(j, l)] = BF_true()
            elif j == 0:
                bigtable[(j, l)] = BF_not(BF_or(v[:l]))
            else:
                # 0 < j <= l
                bigtable[(j, l)] = BF_or([BF_and([BF_not(v[l-1]), bigtable[(j, l-1)]]),
                    bigtable[(j-1, l-1)]])

    return bigtable[(k, len(v))]


def BF_atmost_CNF(k, v):
    """ Satisfiable iff at most k of the vars in v are true.
    Returns a formula in CNF.
    """

    bigtable_clauses = {}
    bigtable_vars = {}

    for l in range(len(v) + 1):
        # Only include the ones that we really need.
        for j in range(max(0, k-len(v)+l), min(k, l+1) + 1):
#        for j in range(0, k + 1):
            me = newsubst("(%d,%d)-%%d" % (j, l))
            bigtable_vars[(j, l)] = me
            if j > l or l == 0:
                bigtable_clauses[(j, l)] = [BF_or([me])]
            elif j == 0:
                bigtable_clauses[(j, l)] = BF_pattern3(me, [BF_not(x) for x in v[:l]])
            else:
                # 0 < j <= l
                bigtable_clauses[(j, l)] = BF_pattern1(me,
                    BF_not(v[l-1]), bigtable_vars[(j, l-1)], bigtable_vars[(j-1, l-1)])

    # All clauses created, collect them.

    clauses = reduce(lambda x, y: x+y, bigtable_clauses.values(), list())
    clauses += [BF_or([bigtable_vars[(k, len(v))]])]

    # Now just wrap up in an AND and remove multiple negations.

    return BF_and(clauses).negations_downwards()
            

def BF_exactly(k, v):
    """ True iff exactly k of the vars in v are true.
    """

    bigtable = {}

    # We do this iteratively since a recursive version could hit
    # Pythons maximal recursion depth. Likely faster anyway.
    for l in range(len(v) + 1):
        for j in range(k + 1):
            if j == 0:
                bigtable[(j, l)] = BF_not(BF_or(v[:l]))
            elif j > l or l == 0:
                bigtable[(j, l)] = BF_false()
            else:
                # 0 < j <= l
                bigtable[(j, l)] = BF_or([BF_and([v[l-1], bigtable[(j-1, l-1)]]),
                    BF_and([BF_not(v[l-1]), bigtable[(j, l-1)]])])

    return bigtable[(k, len(v))]


def BF_exactly_CNF(k, v):
    """ Satisfiable iff exactly k of the vars in v are true.
    Returns a formula in CNF.
    """

    bigtable_clauses = {}
    bigtable_vars = {}

    for l in range(len(v) + 1):
        # Only include the ones that we really need.
        for j in range(max(0, k-len(v)+l), min(k, l+1) + 1):
#        for j in range(k + 1):
            me = newsubst("(%d,%d)-%%d" % (j, l))
            bigtable_vars[(j, l)] = me
            if j == 0:
                bigtable_clauses[(j, l)] = BF_pattern3(me, [BF_not(x) for x in v[:l]])
            elif j > l or l == 0:
                bigtable_clauses[(j, l)] = [BF_or([BF_not(me)])]
            else:
                # 0 < j <= l
                bigtable_clauses[(j, l)] = BF_pattern2(me,
                    v[l-1], bigtable_vars[(j-1, l-1)], bigtable_vars[(j, l-1)])

    # All clauses created, collect them.

    clauses = reduce(lambda x, y: x+y, bigtable_clauses.values(), list())
    clauses += [BF_or([bigtable_vars[(k, len(v))]])]

    # Now just wrap up in an AND and remove multiple negations.

    return BF_and(clauses).negations_downwards()
            

def remove_constants_traversal(o, r):
    """ Helper for dagapply to remove constants by propagating them
    as far as possible (includes empty and singleton AND/OR);
    Creates in r a dict which contains replacements for all nodes,
    in particular for root, representing the cleaned dag.
    Call with d = formula.dagapply(fafter=clean_traversal, startval=dict()) and use with
    newformula = d[formula].
    """

#    print "[DEBUG] Working on ", o

    if type(o) == BF_not:
        c = r[o.childs[0]]
        if type(c) == BF_false:
            newme = BF_true()
        elif type(c) == BF_true:
            newme = BF_false()
        # Now, child is not a constant, so don't change ourselves
        elif c != o.childs[0]:
            # Child changed, so we also "change".
            newme = BF_not(c)
        else:
            newme = o

    elif type(o) == BF_and:

        # We can assume that all childs have replacements
        # (possibly themselves)
        newchilds = [r[c] for c in o.childs]
        if BF_false in map(type, newchilds):
            newme = BF_false()
        elif BF_true in map(type, newchilds) or len(newchilds) <= 1:
            newchilds = filter(lambda c: type(c) != BF_true, newchilds)
            if len(newchilds) == 0:
                newme = BF_true()
# This could destroy CNF-ness.
#            elif len(newchilds) == 1:
#                newme = newchilds[0]
            else:
                newme = BF_and(newchilds)
        elif newchilds != o.childs:
            # A child changed, so we also "change".
            newme = BF_and(newchilds)
        else:
            newme = o

    elif type(o) == BF_or:

        newchilds = [r[c] for c in o.childs]
        if BF_true in map(type, newchilds):
            newme = BF_true()
        elif BF_false in map(type, newchilds) or len(newchilds) <= 1:
            newchilds = filter(lambda c: type(c) != BF_false, newchilds)
            if len(newchilds) == 0:
                newme = BF_false()
# This could destroy CNF-ness.
#            elif len(newchilds) == 1:
#                newme = newchilds[0]
            else:
                newme = BF_or(newchilds)
        elif newchilds != o.childs:
            # A child changed, so we also "change".
            newme = BF_or(newchilds)
        else:
            newme = o

    else:
        newme = o

#    print "[DEBUG] .. replace with ", newme

    r[o] = newme

    return r
        

def negations_downwards_traversal(o, r):
    """ Helper for dagapply to push negations as far downwards as possible
    Result/parameter r is a tuple (replace_pos, replace_neg) with
    * replace_pos is a dictionary providing the unnegated replacement
    * replace_neg is a dictionary providing the negated replacement.
    Call with (d, _) = formula.dagapply(fafter=negationsdownwards_traversal, startval=(dict(), dict())) and use with newformula = d[formula].
    """

#    print "[DEBUG] Working on ", o

    (replace_pos, replace_neg) = r

    if type(o) == BF_not:

        if isinstance(o.childs[0], BF_leaf):
            # We are a negation of a leaf, so let's make things easy to avoid
            # creating a new path upwards
            newme_pos = o
        else:
            newme_pos = replace_neg[o.childs[0]]

        newme_neg = replace_pos[o.childs[0]]
            
    elif type(o) == BF_and:

        # Only create new positive replacement node if some child changed
        newchilds = [replace_pos[c] for c in o.childs]
        if newchilds == o.childs:
            newme_pos = o
        else:
            newme_pos = BF_and(newchilds)

        newme_neg = BF_or([replace_neg[c] for c in o.childs])

    elif type(o) == BF_or:

        # Only create new positive replacement node if some child changed
        newchilds = [replace_pos[c] for c in o.childs]
        if newchilds == o.childs:
            newme_pos = o
        else:
            newme_pos = BF_or(newchilds)

        newme_neg = BF_and([replace_neg[c] for c in o.childs])

    elif isinstance(o, BF_leaf):

        newme_pos = o
        # This one won't be used if we already are a negated leaf
        newme_neg = BF_not(o)

    else:

        raise RuntimeError("Unknown node type: %s" % str(type(o)))

#    print "[DEBUG] .. positive replacement: ", newme_pos
#    print "[DEBUG] .. negative replacement: ", newme_neg

    replace_pos[o] = newme_pos
    replace_neg[o] = newme_neg

    return (replace_pos, replace_neg)

       
def flatten_and_or_traversal(o, r): 
    """ Helper for dagapply to flatten out AND/OR in a BF dag.
    Creates in r a dict which contains replacements for all nodes,
    in particular for root, representing the cleaned dag.
    Call with d = formula.dagapply(fafter=flatten_traversal, startval=dict()) and use with
    newformula = d[formula].
    """

#    print "[DEBUG] Working on", o

    if type(o) == BF_and:

        flatchilds = [r[c] for c in o.childs]
        if BF_and in map(type, flatchilds): 
            newchilds = []
            for c in flatchilds:
                if type(c) == BF_and:
                    newchilds = newchilds + c.childs
                else:
                    newchilds.append(c)
            newme = BF_and(newchilds)
        elif flatchilds != o.childs:
            # A child changed, so we also "change".
            newme = BF_and(flatchilds)
        else:
            newme = o

    elif type(o) == BF_or:

        flatchilds = [r[c] for c in o.childs]
        if BF_or in map(type, flatchilds):
            newchilds = []
            for c in flatchilds:
                if type(c) == BF_or:
                    newchilds = newchilds + c.childs
                else:
                    newchilds.append(c)
            newme = BF_or(newchilds)
        elif flatchilds != o.childs:
            # A child changed, so we also "change".
            newme = BF_or(flatchilds)
        else:
            newme = o

    elif type(o) == BF_not:

        c = o.childs[0]
        if r[c] != c:
            # A child changed, so we also "change".
            newme = BF_not(r[c])
        else:
            newme = o

    else:

        newme = o

    r[o] = newme

#    if newme != o:
#        print "[DEBUG] .. replacement:", newme

    return r


def tseitinize_traversal(o, r):
    """ Helper for dagapply to turn a formula into a set of clauses via
    Tseitin transformation.
    Creates in r a tuple (subst, clauses) with
    * subst is a dict giving a substitution variable for each non-literal
    * clauses is a dict collecting the new clauses
    Skips the node if subst is already defined and if o is a literal.
    """

    (subst, clauses) = r

    if o in subst:
        # We already created a substitution and corresponding 
        # clauses for this node.
        return r

    if o.is_literal():
        # Nothing to do either, just substitute literal with itself.
        # No new clauses.
        subst[o] = o
        return (subst, clauses)

    # Now o is BF_and or BF_or

#    print "[DEBUG] Working on", o

    s = newsubst()
    subst[o] = s

#    print "[DEBUG] .. new variable:", s

    # Create a set of clauses representing "s iff o" where we already
    # use the substitutions of the child nodes of o

    substchilds = [subst[c] for c in o.childs]

    if type(o) == BF_and:
        clauses.append(BF_or([s] + [BF_not(c) for c in substchilds]))
        clauses = clauses + [BF_or([BF_not(s), c]) for c in substchilds]

    elif type(o) == BF_or:
        clauses.append(BF_or([BF_not(s)] + substchilds))
        clauses = clauses + [BF_or([s, BF_not(c)]) for c in substchilds]
    
    return (subst, clauses)
    


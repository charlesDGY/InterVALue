import path
import heapq

from debug import debug_print as dp

class DiscardingDbfStore(path.PathStore):

    """ A store for dbf computations which discards dominated paths. 
    Optimized version by only keeping one path per e and end vertex.
    Should work with all path abstractions (fullpath, triple)
    NOT to be used for marked paths. Use DiscardingMarkedDbfStore instead!
    """

    def __init__(self, D):
        super(DiscardingDbfStore, self).__init__()
        self.D = D
        self.stored = set()
        self.fresh = set()
        self.index = dict()
        self.indexwitnesses = dict()

    def pop_fresh(self):
        if len(self.fresh) > 0:
            path = self.fresh.pop()
            self.stored.add(path)
            return path
        else:
            return None

    def add_paths(self, paths):
        for path in paths:
            v = path.get_end()
            if v not in self.index:
                self.index[v] = [None] * (self.D + 1)
                self.indexwitnesses[v] = [None] * (self.D + 1)
            if self.should_be_stored(path):
                self.fresh.add(path)
                dp(4, 0, "Stored %s." % path)
                e = path.get_e()
                d = path.get_d()
                while (e >= 0 and (self.index[v][e] is None or 
                        d < self.index[v][e])):
                    oldwitness = self.indexwitnesses[v][e]
                    for s in (self.fresh, self.stored):
                        if (oldwitness in s and path > oldwitness):
                            s.remove(oldwitness)
                            dp(4, 1, "Removed dominated %s." % oldwitness)
                            dp(4, 2, "<%d, %d> dominates <%d, %d>." % 
                                (e, d, oldwitness.get_e(), oldwitness.get_d()))
                    self.index[v][e] = d
                    self.indexwitnesses[v][e] = path
                    e = e - 1
                #dp(4, 2, "Index: %s" % str(self.index))
            else:
                dp(4, 0, "Discarded %s." % path)
                dp(4, 1, "Reason: %s." % self.reason(path))

    def get_stored_num(self):
        return len(self.stored)

    def get_fresh_num(self):
        return len(self.fresh)

    def get_paths(self):
#        return self.stored
        # For iterative solvers it could actually be that we
        # have to return paths here which are not in self.stored yet.
        return list(self.stored) + list(self.fresh)

    def should_be_stored(self, path):
        e = path.get_e()
        d = path.get_d()
        v = path.get_end()
        return (d <= self.D
            and (self.index[v][e] is None or d < self.index[v][e]))
            
    def reason(self, path):
        e = path.get_e()
        d = path.get_d()
        v = path.get_end()
        if d > self.D:
            return "d = %d > %d = D" % (d, self.D)
        if self.index[v][e] is not None and d >= self.index[v][e]:
            dpath = self.indexwitnesses[v][e]
            return "dominated by <%d, %d> via %s" % (dpath.get_e(), 
                dpath.get_d(), dpath)
        return "No reason to remove"
       

class DiscardingSortedDbfStore(DiscardingDbfStore):

    """ 
    Same as DiscardingDbfStore, except that it keeps the fresh
    list sorted by d of paths and always pops the shortest one.
    """

    def __init__(self, D):
        super(DiscardingSortedDbfStore, self).__init__(D)
        self.fresh = list()
        self.freshcounter = 0
        self.current_limit = 0

    def pop_fresh(self):
        # There might be some removed paths. Pop until head isn't one.
        while len(self.fresh) > 0 and self.fresh[0][2] == "REMOVED":
            heapq.heappop(self.fresh)
        if len(self.fresh) > 0:
            (_, _, path) = heapq.heappop(self.fresh)
            self.stored.add(path)
            return path
        else:
            return None

    def add_paths(self, paths):
        for path in paths:
            v = path.get_end()
            if v not in self.index:
                self.index[v] = [None] * (self.D + 1)
                self.indexwitnesses[v] = [None] * (self.D + 1)
            if self.should_be_stored(path):
                e = path.get_e()
                d = path.get_d()
                heapq.heappush(self.fresh, [d, self.freshcounter, path])
                (self.current_limit, _, _) = self.fresh[0]
                self.freshcounter += 1
                dp(4, 0, "Stored %s." % path)
                while (e >= 0 and (self.index[v][e] is None or 
                        d < self.index[v][e])):
                    oldwitness = self.indexwitnesses[v][e]
                    freshset = set(p for (_, _, p) in self.fresh)
                    for s in (freshset, self.stored):
                        if (oldwitness in s and path > oldwitness):
                            s.remove(oldwitness)
                            dp(4, 1, "Removed dominated %s." % oldwitness)
                            dp(4, 2, "<%d, %d> dominates <%d, %d>." % 
                                (e, d, oldwitness.get_e(), oldwitness.get_d()))
                    for freshtuple in self.fresh:
                        (_, _, p) = freshtuple
                        if not p in freshset:
                            freshtuple[2] = "REMOVED"
                    self.index[v][e] = d
                    self.indexwitnesses[v][e] = path
                    e = e - 1
                #dp(4, 2, "Index: %s" % str(self.index))
            else:
                dp(4, 0, "Discarded %s." % path)
                dp(4, 1, "Reason: %s." % self.reason(path))

    def get_paths(self):
#        return self.stored
        # For iterative solvers it could actually be that we
        # have to return paths here which are not in self.stored yet.
        return list(self.stored) + [p for (_, _, p) in self.fresh if p != "REMOVED"]


 

class DiscardingSortedDbfStoreNoD(DiscardingSortedDbfStore):

    """ 
    Same as DiscardingSortedDbfStore, except that it does not 
    have a self.D, stores everything without limit.
    """

    def __init__(self):
        super(DiscardingSortedDbfStoreNoD, self).__init__(None)

    def add_paths(self, paths):
        for path in paths:
            v = path.get_end()
            D = path.get_e()
            if v not in self.index:
                self.index[v] = [None] * (D + 1)
                self.indexwitnesses[v] = [None] * (D + 1)
            while len(self.index[v]) < D+1:
                self.index[v].append(None)
            while len(self.indexwitnesses[v]) < D+1:
                self.indexwitnesses[v].append(None)
            if self.should_be_stored(path):
                e = path.get_e()
                d = path.get_d()
                heapq.heappush(self.fresh, [d, self.freshcounter, path])
                (self.current_limit, _, _) = self.fresh[0]
                self.freshcounter += 1
                dp(4, 0, "Stored %s." % path)
                while (e >= 0 and (self.index[v][e] is None or 
                        d < self.index[v][e])):
                    oldwitness = self.indexwitnesses[v][e]
                    freshset = set(p for (_, _, p) in self.fresh)
                    for s in (freshset, self.stored):
                        if (oldwitness in s and path > oldwitness):
                            s.remove(oldwitness)
                            dp(4, 1, "Removed dominated %s." % oldwitness)
                            dp(4, 2, "<%d, %d> dominates <%d, %d>." % 
                                (e, d, oldwitness.get_e(), oldwitness.get_d()))
                    for freshtuple in self.fresh:
                        (_, _, p) = freshtuple
                        if not p in freshset:
                            freshtuple[2] = "REMOVED"
                    self.index[v][e] = d
                    self.indexwitnesses[v][e] = path
                    e = e - 1
                #dp(4, 2, "Index: %s" % str(self.index))
            else:
                dp(4, 0, "Discarded %s." % path)
                dp(4, 1, "Reason: %s." % self.reason(path))

    def get_paths(self):
#        return self.stored
        # For iterative solvers it could actually be that we
        # have to return paths here which are not in self.stored yet.
        return list(self.stored) + [p for (_, _, p) in self.fresh if p != "REMOVED"]

    def should_be_stored(self, path):
        e = path.get_e()
        d = path.get_d()
        v = path.get_end()
        return self.index[v][e] is None or d < self.index[v][e]
            
    def reason(self, path):
        e = path.get_e()
        d = path.get_d()
        v = path.get_end()
        if self.index[v][e] is not None and d >= self.index[v][e]:
            dpath = self.indexwitnesses[v][e]
            return "dominated by <%d, %d> via %s" % (dpath.get_e(), 
                dpath.get_d(), dpath)
        return "No reason to remove"
 

class DiscardingMarkedDbfStore(DiscardingDbfStore):

    """ A store for dbf computations which discards dominated paths.
    Version for marked paths, i.e., arbitrary deadlines.
    Optimized version by only keeping one path per e and end vertex
    for end-marked paths. 
    End-nonmarked paths are always stored, so path creation should be
    sufficiently restrictive.
    """

    def __init__(self, D):
        super(DiscardingMarkedDbfStore, self).__init__(D)

    def should_be_stored(self, path):
        if not path.is_endmarked():
            return True
        e = path.get_e()
        d = path.get_d()
        v = path.get_end()
        return (d <= self.D
            and (self.index[v][e] is None or d < self.index[v][e]))
            
 
class DiscardingUtilizationStore(path.PathStore):

    """ A store for utilization computations which discards dominated paths. 
    Optimized version by only keeping one path per start and end vertex.
    Should work with all path abstractions (fullpath, triple)
    """

    def __init__(self, maxlen):
        super(DiscardingUtilizationStore, self).__init__()
        self.maxlen = maxlen
        self.stored = set()
        self.fresh = set()
        self.index = dict()
        self.indexwitnesses = dict()

    def pop_fresh(self):
        if len(self.fresh) > 0:
            path = self.fresh.pop()
            self.stored.add(path)
            return path
        else:
            return None

    def add_paths(self, paths):
        for path in paths:
            u = path.get_start()
            v = path.get_end()
            if (u, v) not in self.index:
                self.index[(u, v)] = None
            if self.should_be_stored(path):
                self.fresh.add(path)
                dp(4, 0, "Stored %s." % path)
                if path.get_p() > 0:
                    oldwitness = self.index[(u, v)]
                    self.index[(u, v)] = path
                    if oldwitness is not None:
                        dp(4, 1, "Removed dominated %s." % oldwitness)
                        dp(4, 2, "<%d, %d> dominates <%d, %d>." % 
                            (path.get_e2(), path.get_p(), oldwitness.get_e2(), 
                            oldwitness.get_p()))
                #dp(4, 2, "Index: %s" % str(self.index))
            else:
                dp(4, 0, "Discarded %s." % path)
                dp(4, 1, "Reason: %s." % self.reason(path))

    def get_stored_num(self):
        return len(self.stored)

    def get_fresh_num(self):
        return len(self.fresh)

    def get_paths(self):
        return self.stored

    def should_be_stored(self, path):
        l = len(path)
        u = path.get_start()
        v = path.get_end()
        return (l <= self.maxlen 
            and (self.index[(u, v)] is None or path > self.index[(u, v)]))
            
    def reason(self, path):
        l = len(path)
        u = path.get_start()
        v = path.get_end()
        if l > self.maxlen:
            return "l = %d > %d = maxlen" % (l, self.maxlen)
        if self.index[(u, v)] is not None and self.index[(u, v)] >= path:
            dpath = self.index[(u, v)]
            return "dominated by <%d, %d> via %s" % (dpath.get_e2(), 
                dpath.get_p(), dpath)
        return "No reason to remove"
        


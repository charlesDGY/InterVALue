import path
import heapq

from debug import debug_print as dp

class RequestTriple(path.Path):

    """RequstTriple stores paths abstracted as request triples, i.e.,
    as triples <e, p, v> of execution time, duration and last vertex.

    Note: Semantics is different from Demand Triples. p=10 for a request triple
    means that *in time slot 10*, the request is e, i.e., effective at t=11
    if we focus on integers.
    d=10 for a demand triple means that *for 10 time slots*.
    So, rbf(11) >= e but dbf(10) >= e.
    """

    def __init__(self, jobs, e=None, p=None):
        if e is None:
            self.e = sum([job.get_e() for job in jobs])
        else:
            self.e = e

        if p is None:
            self.p = 0
            for i in xrange(len(jobs) - 1):
                self.p += jobs[i].succs[jobs[i + 1]]
        else:
            self.p = p

        self.last = jobs[-1]

    def get_e(self):
        return self.e

    def get_p(self):
        return self.p

    def get_end(self):
        return self.last

    def get_extended(self, job):
        e = self.e + job.get_e()
        p = self.p + self.last.succs[job]
        return [RequestTriple([job], e, p)]

    def __ge__(self, o):
        return (self.last == o.last and self.e >= o.e and self.p <= o.p)

    def __gt__(self, o):
        return (self >= o and (self.get_e() != o.get_e()
            or self.get_p() != o.get_p()))

    def __str__(self):
        return '<%d, %d, %s>' % (self.e, self.p, self.last)



class DiscardingSortedRbfStoreNoD(path.PathStore):

    """ 
    Just like DiscardingSortedDbfStoreNoD but for request paths.
    """

    def __init__(self):
        super(DiscardingSortedRbfStoreNoD, self).__init__()
        self.stored = set()
        self.index = dict()
        self.indexwitnesses = dict()
        self.fresh = list()
        self.freshcounter = 0
        self.current_limit = -1

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
                p = path.get_p()
                heapq.heappush(self.fresh, [p, self.freshcounter, path])
                dp(6, 1, "Pushed to fresh: '%s'" % str([p, self.freshcounter, str(path)]))
                dp(6, 1, "Contents now: %s " % str(self.fresh))
                (self.current_limit, _, _) = self.fresh[0]
                self.freshcounter += 1
                dp(4, 0, "Stored %s." % path)
                while (e >= 0 and (self.index[v][e] is None or 
                        p < self.index[v][e])):
                    oldwitness = self.indexwitnesses[v][e]
                    freshset = set(p for (_, _, p) in self.fresh)
                    for s in (freshset, self.stored):
                        if (oldwitness in s and path > oldwitness):
                            s.remove(oldwitness)
                            dp(4, 1, "Removed dominated %s." % oldwitness)
                            dp(4, 2, "<%d, %d> dominates <%d, %d>." % 
                                (e, p, oldwitness.get_e(), oldwitness.get_p()))
                    for freshtuple in self.fresh:
                        (_, _, freshpath) = freshtuple
                        if not freshpath in freshset:
                            freshtuple[2] = "REMOVED"
                    self.index[v][e] = p
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
        return list(self.stored) + [p for (_, _, p) in self.fresh if p != "REMOVED"]

    def should_be_stored(self, path):
        e = path.get_e()
        p = path.get_p()
        v = path.get_end()
        return self.index[v][e] is None or p < self.index[v][e]
            
    def reason(self, path):
        e = path.get_e()
        p = path.get_p()
        v = path.get_end()
        if self.index[v][e] is not None and p >= self.index[v][e]:
            dpath = self.indexwitnesses[v][e]
            return "dominated by <%d, %d> via %s" % (dpath.get_e(), 
                dpath.get_e(), dpath)
        return "No reason to remove"
 


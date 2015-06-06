import path
import path.discardingstores


class DemandTriple(path.DbfPath):

    """DemandTriple stores paths abstracted as demand triples, i.e.,
    as triples <e, d, v> of execution time, deadline and last vertex.
    """

    def __init__(self, jobs, e=None, d=None):
        if e is None:
            self.e = sum([job.get_e() for job in jobs])
        else:
            self.e = e

        if d is None:
            self.d = 0
            for i in xrange(len(jobs) - 1):
                self.d += jobs[i].succs[jobs[i + 1]]
            self.d += jobs[-1].get_d()
        else:
            self.d = d

        self.last = jobs[-1]

    def get_e(self):
        return self.e

    def get_d(self):
        return self.d

    def get_end(self):
        return self.last

    def get_extended(self, job):
        e = self.e + job.get_e()
        d = self.d - self.last.get_d() + self.last.succs[job] + job.get_d()
        return [DemandTriple([job], e, d)]

    def __ge__(self, o):
        return (self.last == o.last and self.e >= o.e and self.d <= o.d)

    def __gt__(self, o):
        return (self >= o and (self.get_e() != o.get_e()
            or self.get_d() != o.get_d()))


    def __str__(self):
        return '<%d, %d, %s>' % (self.e, self.d, self.last)


class UtilizationTriple(path.UtilizationPath):

    """UtilizationTriple stores paths abstracted as utilization triples, i.e.,
    as triples <e, p, (u, v)> of execution time (minus that of the first
    vertex, i.e., "e2"), duration and first and last vertices.
    """

    def __init__(self, jobs, e2=None, p=None, length=None):
        if e2 is None:
            self.e2 = sum([job.get_e() for job in jobs[1:]])
        else:
            self.e2 = e2

        if p is None:
            self.p = 0
            for i in xrange(len(jobs) - 1):
                self.p += jobs[i].succs[jobs[i + 1]]
        else:
            self.p = p
        
        self.first = jobs[0]
        self.last = jobs[-1]

        if length is None:
            self.length = len(jobs) - 1
        else:
            self.length = length

    def get_p(self):
        return self.p

    def get_e2(self):
        return self.e2

    def get_start(self):
        return self.first

    def get_end(self):
        return self.last

    def get_extended(self, job):
        e2 = self.e2 + job.get_e()
        p = self.p + self.last.succs[job]
        return [UtilizationTriple([self.first, job], e2, p, self.length + 1)]

    def __len__(self):
        return self.length

    def __ge__(self, o):
        return (self.get_start() == o.get_start()
            and self.get_end() == o.get_end() 
            and self.get_e2() * o.get_p() >= o.get_e2() * self.get_p())
			
    def __gt__(self, o):
        return (self >= o 
            and (self.get_e2() * o.get_p() > o.get_e2() * self.get_p()))

    def __str__(self):
        return '<%d, %d, (%s, %s)>' % (self.e2, self.p, self.first, self.last)


class OLD_DemandTripleStore(path.PathStore):
    
    """A PathStore for DemandTriples. Includes discarding via simple domination 
    check. Should be superseeded by DiscardingDbfStore."""

    def __init__(self, D):
        self.D = D
        super(DemandTripleStore, self).__init__()

    def should_be_stored(self, path):
        if path.get_d() > self.D:
            return False
        
        newstored = set()
        newfresh = set()
        for triple in self.stored:
            if triple >= path:
                return False
            if not path >= triple:
                newstored.add(triple)
        for triple in self.fresh:
            if triple >= path:
                return False
            if not path >= triple:
                newfresh.add(triple)
        self.stored = newstored
        self.fresh = newfresh
        
        return True


class OLD_UtilizationTripleStore(path.PathStore):
    
    """A PathStore for UtilizationTriples.
    Superseeded by DiscardingUtilizationStore."""

    def __init__(self, maxlen):
        self.maxlen = maxlen
        super(UtilizationTripleStore, self).__init__()

    def should_be_stored(self, path):
        # TODO: Add discarding.
        return len(path) <= self.maxlen


# Export path abstractions and stores in the standard format.
DbfPath = DemandTriple
UtilizationPath = UtilizationTriple
DbfStore = path.discardingstores.DiscardingDbfStore
UtilizationStore = path.discardingstores.DiscardingUtilizationStore


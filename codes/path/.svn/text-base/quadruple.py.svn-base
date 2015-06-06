import path


class DemandQuadruple(path.DbfPath):

    """DemandQuadruple stores paths abstracted as demand quadruples, i.e.,
    as triples <e, d, p, v> of execution time, deadline and duration last
    vertex.
    """

    def __init__(self, jobs, e=None, d=None, p=None):
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

        if p is None:
            self.p = 0
            for i in xrange(len(jobs) - 1):
                self.p += jobs[i].succs[jobs[i + 1]]
        else:
            self.p = p

        self.last = jobs[-1]

    def get_e(self):
        return self.e

    def get_d(self):
        return self.d

    def get_p(self):
        return self.p

    def get_end(self):
        return self.last

    def get_extended(self, job):
        """ Demand quadruples are abstractions of *marked* paths, so there are
        two extensions possible: marked and non-marked"""
        e = self.e + job.get_e()
        d = max(self.d, self.p + self.last.succs[job] + job.get_d())
        p = self.p + self.last.succs[job]
        dq1 = DemandQuadruple([job], e, d, p)

        e = self.e
        d = self.d
        p = self.p + self.last.succs[job]
        dq2 = DemandQuadruple([job], e, d, p)

        return [dq1, dq2]

    def __ge__(self, o):
        """ Domination relation unclear for demand quadruples. """
#        return (self.last == o.last and self.e >= o.e and self.d <= o.d)
        raise NotImplementedError

    def __str__(self):
        return '<%d, %d, %d, %s>' % (self.e, self.d, self.p, self.last)


class DemandQuadrupleStore(path.PathStore):
    
    """A PathStore for DemandQuadruples."""

    def __init__(self, D):
        self.D = D
        super(DemandQuadrupleStore, self).__init__()

    def should_be_stored(self, path):
        if (path.get_d() > self.D or path.get_p() > self.D):
            return False
       
        # Basically unimplemented because of missing < relation
        return True



# Export path abstractions and stores in the standard format.
DbfPath = DemandQuadruple
UtilizationPath = path.triple.UtilizationTriple
DbfStore = DemandQuadrupleStore
UtilizationStore = path.UtilizationPathStore


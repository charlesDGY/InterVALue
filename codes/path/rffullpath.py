import path
from debug import debug_print as dp


class FullRfPath(path.RfPath):

    """Stores entire concrete paths (i.e., it performs no
    abstractions at all). Domination relation on rf.
    
    max_horizon is an optional parameter used for domination relation.
    (Size of maximum rf prefix to be considered.)
    """

    def __init__(self, jobs, max_horizon = None, rf = None, horizon = None):
        super(FullRfPath, self).__init__(jobs)
        self.max_horizon = max_horizon
        self.rf = rf or self.recompute_rf()
        self.horizon = horizon or self.recompute_horizon()
        if self.horizon > self.max_horizon:
            self.horizon = self.max_horizon
        # Invariant: self.horizon <= self.max_horizon
        

    def get_end(self):
        return self.jobs[-1]

    def get_extended(self, job):
#        return [FullRfPath(self.jobs[:] + [job], max_horizon = self.max_horizon)]
        newjobs = self.jobs[:] + [job]
        # TODO: Using self.rf[-1] assumes non-zero edge labels.
        newrf = (self.rf[:] + 
            [self.rf[-1]] * (self.jobs[-1].succs[job] - self.jobs[-1].mindelay) +
            [self.rf[-1] + job.get_e()] * job.mindelay)[:self.max_horizon]
        newhorizon = min(self.horizon + 
            self.jobs[-1].succs[job] - self.jobs[-1].mindelay +
            job.mindelay, self.max_horizon)
        return [FullRfPath(newjobs, max_horizon = self.max_horizon,
            rf = newrf, horizon = newhorizon)]
        
    def recompute_rf(self):
        dp(5, 1, "Recomputing RF.")
        rf = list()
        c = 0
        for (i, v) in enumerate(self.jobs):
            c += v.get_e()
            if i == len(self.jobs) - 1:
                rf.extend([c] * v.get_mindelay())
            else:
                rf.extend([c] * v.succs[self.jobs[i + 1]])
        return rf[:self.max_horizon]

    def get_rf(self):
        return self.rf

    def recompute_horizon(self):   
        dp(5, 1, "Recomputing horizon.")
        h = 0
        for (i, v) in enumerate(self.jobs):
            if i == len(self.jobs) - 1:
                h += v.get_mindelay()
            else:
                h += v.succs[self.jobs[i + 1]]
        return min(h, self.max_horizon)
         
    def get_horizon(self):
        return self.horizon

    def __len__(self):
        return len(self.jobs) - 1

    def __ge__(self, o):
        # A (weakly) dominates B iff (1) OR (2) with
        # (1a) A.endvertex == B.endvertex, and
        # (1b) A.rfendpoint dominates B.rfendpoint, and
        # (1c) A >= B in all points up to A.horizon;
        # (2a) B.horizon >= max_horizon, and
        # (2b) A.endpoint (latest max_horizon-1) at least like B[max_horizon-1], and
        # (2c) A >= B in all points up to min(A.horizon,max_horizon).
        # Assumption: o.max_horizon >= self.max_horizon
        #H = min(self.get_horizon(), self.max_horizon)
        H = self.get_horizon()
        condition1 = (self.get_end() == o.get_end() and
            self.get_horizon() <= o.get_horizon() and
            self.get_rf()[-1] >= o.get_rf()[-1] and
            all([self.get_rf()[i] >= o.get_rf()[i] for i in xrange(H)]))
        condition2 = (self.max_horizon is not None and
            o.get_horizon() >= self.max_horizon and
            self.get_rf()[H-1] >= o.get_rf()[self.max_horizon-1] and
            all([self.get_rf()[i] >= o.get_rf()[i] for i in xrange(H)]))
        return condition1 or condition2
            
    def __gt__(self, o):
        # Like __ge__ except that at SOME point, A and B differ.
        #H = min(self.get_horizon(), self.max_horizon, o.get_horizon())
        H = min(self.get_horizon(), o.get_horizon())
        return (self >= o and
            not all([self.get_rf()[i] == o.get_rf()[i] for i in xrange(H)]))

    def __str__(self):
        return ('[' + ' -> '.join(map(str, self.jobs)) + ']' + ', ' + 
            str(self.get_rf()) + ", " + str(len(self.get_rf())))


class AbstractRfPath(path.RfPath):

    """Stores abstract rf paths, i.e., just rf.
    """

    def __init__(self, max_horizon = None, rf = None, horizon = None,
            childs = None, spread = None):
        if rf is None:
            raise RuntimeError("AbstractRfPath needs rf to be not None!")
        super(AbstractRfPath, self).__init__([])
        self.max_horizon = max_horizon
        self.rf = rf
        self.horizon = horizon or len(rf)
        self.childs = childs
        self.spread = spread

    def get_end(self):
        raise RuntimeError("AbstractRfPath doesn't have jobs.")

    def get_extended(self, job):
        raise RuntimeError("AbstractRfPath doesn't have jobs.")
        
    def recompute_rf(self):
        raise RuntimeError("AbstractRfPath doesn't have jobs.")

    def get_rf(self):
        return self.rf

    def recompute_horizon(self):   
        raise RuntimeError("AbstractRfPath doesn't have jobs.")
         
    def get_horizon(self):
        return self.horizon

    def __len__(self):
        raise RuntimeError("AbstractRfPath doesn't have jobs.")

    def __ge__(self, o):
        # Abstract path A (weakly) dominates B iff (2) with
        # (2a) B.horizon >= max_horizon, and
        # (2b) A.endpoint (latest max_horizon-1) at least like B[max_horizon-1], and
        # (2c) A >= B in all points up to min(A.horizon,max_horizon).
        # Assumption: o.max_horizon >= self.max_horizon
        #H = min(self.get_horizon(), self.max_horizon)
        H = self.get_horizon()
        condition2 = (self.max_horizon is not None and
            o.get_horizon() >= self.max_horizon and
            self.get_rf()[min(H, self.max_horizon)-1] >= o.get_rf()[self.max_horizon-1] and
            all([self.get_rf()[i] >= o.get_rf()[i] for i in xrange(min(H, self.max_horizon))]))
        return condition2
            
    def __gt__(self, o):
        # Like __ge__ except that at SOME point, A and B differ.
        #H = min(self.get_horizon(), self.max_horizon, o.get_horizon())
        H = min(self.get_horizon(), o.get_horizon())
        return (self >= o and
            not all([self.get_rf()[i] == o.get_rf()[i] for i in xrange(H)]))

    def __str__(self):
        return ('[ABSTRACT]' + ', ' + 
            str(self.get_rf()) + ", " + str(len(self.get_rf())))



class DiscardingRfStore(path.RfPathStore):
    
    """A basic PathStore for Paths in rf computations. Discard all
    dominated paths.
    """

    def __init__(self, D):
        self.D = D
        self.stored = set()
        self.fresh = set()
        super(DiscardingRfStore, self).__init__(D)

    def pop_fresh(self):
        """Return one path on the 'frontier' of the explored paths, i.e.,
        one that has not previously been extended. Afterwards the path is
        discarded!
        """
        if len(self.fresh) > 0:
            path = self.fresh.pop()
            #self.stored.add(path)
            return path
        return None


    def add_paths(self, paths):
        """Add the paths in the list <paths> to the store.
        If path does not exceed horizon yet, store it in fresh set.
        If we are dominated by stored path, discard us.
        If already stored path is dominated, remove it.
        """
        for path in paths:

            # Check if path is dominated by a stored path
            dominated = False
            for p in self.fresh.union(self.stored):
                dominated = (p > path)
                if dominated:
                    dp(3, 0, "Not storing %s." % path)
                    dp(4, 1, "Dominated by already stored %s." % p)
                    break
            if dominated:
                continue

            # Remove all paths dominated by path
            # .. in fresh
            for p in tuple(self.fresh):
                dp(4, 1, "Checking for dominance in fresh: %s." % p)
                if path >= p:
                    dp(3, 1, "Remove from fresh now dominated %s." % p)
                    self.fresh.remove(p)

            # .. in stored
            for p in tuple(self.stored):
                dp(4, 1, "Checking for dominance in stored: %s." % p)
                if path >= p:
                    dp(3, 1, "Remove from stored now dominated %s." % p)
                    self.stored.remove(p)

            if self.is_todo(path):
                self.fresh.add(path)
                dp(3, 0, "Store in todo: %s" % path)
            else:
                self.stored.add(path)
                dp(3, 0, "Store in non-todo: %s" % path)


    def is_todo(self, path):
        return path.get_horizon() < self.D



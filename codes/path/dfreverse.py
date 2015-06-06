import path
from debug import debug_print as dp


class DfReversePath(path.DfPath):

    """Stores entire concrete paths together with df. Extends
    paths at the *front*.
    Domination relation on df.
    
    max_horizon is an optional parameter used for domain restriction.
    (Size of maximum df suffix to be computed.)
    """

    def __init__(self, jobs, max_horizon = None, df = None, horizon = None):
        super(DfReversePath, self).__init__(jobs)
        self.max_horizon = max_horizon
        self.df = df or self.recompute_df()
        self.horizon = horizon or self.recompute_horizon()
        if self.horizon > self.max_horizon and self.max_horizon is not None:
            self.horizon = self.max_horizon
        # Invariant: self.horizon <= self.max_horizon (if latter not None)

    def get_start(self):
        return self.jobs[0]

    def get_extended(self, job):
        esum = sum(j.get_e() for j in self.jobs)
        newjobs = [job] + self.jobs[:]
        newdf = (self.df[:] +
            [esum] * (job.succs[self.jobs[0]] - self.jobs[0].get_minprevdelay()) +
            [esum + job.get_e()] * job.get_minprevdelay())
        newhorizon = min(len(newdf), self.max_horizon)
        return [DfReversePath(newjobs, max_horizon = self.max_horizon,
            df = newdf, horizon = newhorizon)]
        
    def recompute_df(self): 
        dp(5, 1, "Recomputing DF.")
        c = 0
        df = [0] * self.jobs[-1].get_d()
        for (i, v) in reversed(list(enumerate(self.jobs))):
            c += v.get_e()
            if i > 0:
                df.extend([c] * self.jobs[i - 1].succs[v])
            else:
                df.extend([c] * v.get_minprevdelay())
        return df[:self.max_horizon]

    def get_df(self):
        return self.df

    def eval_wbf(self, gamma, delta):
        if gamma == 0:
            return 0
        else:
            return self.df[delta]

    def recompute_horizon(self):
        dp(5, 1, "Recomputing horizon.")
        return min(len(self.df), self.max_horizon)
         
    def get_horizon(self):
        return self.horizon

    def __len__(self):
        return len(self.jobs) - 1

    def __ge__(self, o):
        # A (weakly) dominates B iff (1) OR (2) with
        # (1a) A.endvertex == B.endvertex, and
        # (1b) A.dfendpoint dominates B.dfendpoint, and
        # (1c) A >= B in all points up to A.horizon;
        # (2a) B.horizon >= max_horizon, and
        # (2b) A.endpoint (latest max_horizon-1) at least like B[max_horizon-1], and
        # (2c) A >= B in all points up to min(A.horizon,max_horizon).
        # Assumption: o.max_horizon >= self.max_horizon
        #H = min(self.get_horizon(), self.max_horizon)
        H = self.get_horizon()
        condition1 = (self.get_start() == o.get_start() and
            self.get_horizon() <= o.get_horizon() and
            self.get_df()[-1] >= o.get_df()[-1] and
            all([self.get_df()[i] >= o.get_df()[i] for i in xrange(H)]))
        condition2 = (self.max_horizon is not None and
            o.get_horizon() >= self.max_horizon and
            self.get_df()[H-1] >= o.get_df()[self.max_horizon-1] and
            all([self.get_df()[i] >= o.get_df()[i] for i in xrange(H)]))
        return condition1 or condition2
            
    def __gt__(self, o):
        # Like __ge__ except that at SOME point, A and B differ.
        #H = min(self.get_horizon(), self.max_horizon, o.get_horizon())
        H = min(self.get_horizon(), o.get_horizon())
        return (self >= o and
            not all([self.get_df()[i] == o.get_df()[i] for i in xrange(H)]))

    def __str__(self):
        return ('[' + ' -> '.join(map(str, self.jobs)) + ']' + ', ' + 
            str(self.get_df()) + ", " + str(len(self.get_df())))


class AbstractDfReversePath(path.DfPath):

    """Stores abstract rf paths, i.e., just rf.
    """

    def __init__(self, max_horizon = None, df = None, horizon = None,
            childs = None, spread = None):
        if df is None:
            raise RuntimeError("AbstractRfPath needs df to be not None!")
        super(AbstractDfReversePath, self).__init__([])
        self.max_horizon = max_horizon
        self.df = df
        self.horizon = horizon or len(df)
        self.childs = childs
        self.spread = spread

    def get_start(self):
        raise RuntimeError("AbstractDfReversePath doesn't have jobs.")

    def get_end(self):
        raise RuntimeError("AbstractDfReversePath doesn't have jobs.")

    def get_extended(self, job):
        raise RuntimeError("AbstractDfReversePath doesn't have jobs.")
        
    def recompute_df(self):
        raise RuntimeError("AbstractDfReversePath doesn't have jobs.")

    def get_df(self):
        return self.df

    def eval_wbf(self, gamma, delta):
        if gamma == 0:
            return 0
        else:
            return self.df[delta]

    def recompute_horizon(self):   
        raise RuntimeError("AbstractDfReversePath doesn't have jobs.")
         
    def get_horizon(self):
        return self.horizon

    def __len__(self):
        raise RuntimeError("AbstractDfReversePath doesn't have jobs.")

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
            self.get_df()[min(H, self.max_horizon)-1] >= o.get_df()[self.max_horizon-1] and
            all([self.get_df()[i] >= o.get_df()[i] for i in xrange(min(H, self.max_horizon))]))
        return condition2
            
    def __gt__(self, o):
        # Like __ge__ except that at SOME point, A and B differ.
        #H = min(self.get_horizon(), self.max_horizon, o.get_horizon())
        H = min(self.get_horizon(), o.get_horizon())
        return (self >= o and
            not all([self.get_df()[i] == o.get_df()[i] for i in xrange(H)]))

    def __str__(self):
        return ('[ABSTRACT]' + ', ' + 
            str(self.get_df()) + ", " + str(len(self.get_df())))



class DiscardingDfReverseStore(path.rffullpath.DiscardingRfStore):
    
    """A basic PathStore for Paths in dfreverse computations. Discard all
    dominated paths. So far identical to DiscardingRfStore.
    """

    def __init__(self, D):
        super(DiscardingDfReverseStore, self).__init__(D)



import path
import path.rffullpath
from debug import debug_print as dp


class FullRfDfPath(path.RfDfPath):

    """Stores entire concrete paths (i.e., it performs no
    abstractions at all). Domination relation on rf.
    
    max_horizon is an optional parameter used for domination relation.
    (Size of maximum rf and df prefix to be considered.)
    """

    def __init__(self, jobs, max_horizon = None, rfdf = None, 
            horizon = None):
        super(FullRfDfPath, self).__init__(jobs)
        self.max_horizon = max_horizon
        (self.rf, self.df) = rfdf or (self.recompute_rf(), self.recompute_df())
        self.horizon = horizon or self.recompute_horizon()
        if self.horizon > self.max_horizon:
            self.horizon = self.max_horizon
        # Invariant: self.horizon <= self.max_horizon
        

    def get_end(self):
        return self.jobs[-1]

    def get_extended(self, job):
#        return [FullRfPath(self.jobs[:] + [job], max_horizon = self.max_horizon)]
        esum = sum(j.get_e() for j in self.jobs)
        newjobs = self.jobs[:] + [job]
        # TODO: Using self.rf[-1] assumes non-zero edge labels.
        newrf = (self.rf[:] + 
            [self.rf[-1]] * (self.jobs[-1].succs[job] - self.jobs[-1].mindelay) +
            [self.rf[-1] + job.get_e()] * job.mindelay)[:self.max_horizon]
        newdf = (self.df[:] + 
            [esum] * (self.jobs[-1].succs[job] - self.jobs[-1].mindelay + job.get_d()) +
            [esum + job.get_e()] * (job.mindelay - job.get_d()))[:self.max_horizon]
        newhorizon = min(self.horizon + 
            self.jobs[-1].succs[job] - self.jobs[-1].mindelay +
            job.mindelay, self.max_horizon)
        return [FullRfDfPath(newjobs, max_horizon = self.max_horizon,
            rfdf = (newrf, newdf), horizon = newhorizon)]
        
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

    def recompute_df(self):
        dp(5, 1, "Recomputing DF.")
        df = list()
        c = 0
        for (i, v) in enumerate(self.jobs):
            df.extend([c] * v.get_d())
            if i == len(self.jobs) - 1:
                p = v.get_mindelay()
            else:
                p = v.succs[self.jobs[i + 1]]
            c += v.get_e()
            df.extend([c] * (p - v.get_d()))
        return df[:self.max_horizon]

    def get_df(self):
        return self.df

    def get_rfdf(self):
        return (self.rf, self.df)

    def eval_wbf(self, gamma, delta):
        if gamma == 0:
            return 0
        else:
            # We need to reduce gamma by 1 since rf is stored
            # with "time slot" semantics (i.e., rf[1] > 0)
            return min(self.rf[gamma-1], self.df[delta])

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
        # (1b) A.rfdfendpoint dominates B.rfdfendpoint, and
        # (1c) A >= B in all points up to A.horizon;
        # (2a) B.horizon >= max_horizon, and
        # (2b) A.endpoint (latest max_horizon-1) at least like B[max_horizon-1], and
        # (2c) A >= B in all points up to min(A.horizon,max_horizon).
        # Assumption: o.max_horizon >= self.max_horizon
        #H = min(self.get_horizon(), self.max_horizon)
        H = self.get_horizon()
        condition1 = (self.get_end() == o.get_end() and
            self.get_horizon() <= o.get_horizon() and
            self.rf[-1] >= o.rf[-1] and
            self.df[-1] >= o.df[-1] and
            all([self.rf[i] >= o.rf[i] for i in xrange(H)]) and
            all([self.df[i] >= o.df[i] for i in xrange(H)]))
        condition2 = (self.max_horizon is not None and
            o.get_horizon() >= self.max_horizon and
            self.rf[H-1] >= o.rf[self.max_horizon-1] and
            self.df[H-1] >= o.df[self.max_horizon-1] and
            all([self.rf[i] >= o.rf[i] for i in xrange(H)]) and
            all([self.df[i] >= o.df[i] for i in xrange(H)]))
        return condition1 or condition2
            
    def __gt__(self, o):
        # Like __ge__ except that at SOME point, A and B differ on rf or df.
        #H = min(self.get_horizon(), self.max_horizon, o.get_horizon())
        H = min(self.get_horizon(), o.get_horizon())
        return (self >= o and
            not (self.get_rfdf()[0][:H] == o.get_rfdf()[0][:H] and
            self.get_rfdf()[1][:H] == o.get_rfdf()[1][:H]))

    def __str__(self):
        return ('[' + ' -> '.join(map(str, self.jobs)) + ']' + ', ' + 
            str(self.get_rf()) + ", " + 
            str(self.get_df()) + ", " + 
            str(len(self.get_rf())))


class AbstractRfDfPath(path.RfDfPath):

    """Stores abstract rf paths, i.e., just rf and df.
    """

    def __init__(self, max_horizon = None, rfdf = None, horizon = None,
            childs = None, spread = None):
        if rfdf is None:
            raise RuntimeError("AbstractRfDfPath needs rfdf to be not None!")
        super(AbstractRfDfPath, self).__init__([])
        self.max_horizon = max_horizon
        (self.rf, self.df) = rfdf
        self.horizon = horizon or min(len(self.rf), len(self.df))
        self.childs = childs
        self.spread = spread

    def get_end(self):
        raise RuntimeError("AbstractRfDfPath doesn't have jobs.")

    def get_extended(self, job):
        raise RuntimeError("AbstractRfDfPath doesn't have jobs.")
        
    def recompute_rf(self):
        raise RuntimeError("AbstractRfDfPath doesn't have jobs.")

    def get_rf(self):
        return self.rf

    def recompute_df(self):
        raise RuntimeError("AbstractRfDfPath doesn't have jobs.")

    def get_df(self):
        return self.df

    def get_rfdf(self):
        return (self.rf, self.df)

    def eval_wbf(self, gamma, delta):
        if gamma == 0:
            return 0
        else:
            # We need to reduce gamma by 1 since rf is stored
            # with "time slot" semantics (i.e., rf[1] > 0)
            return min(self.rf[gamma-1], self.df[delta])

    def recompute_horizon(self):   
        raise RuntimeError("AbstractRfDfPath doesn't have jobs.")
         
    def get_horizon(self):
        return self.horizon

    def __len__(self):
        raise RuntimeError("AbstractRfDfPath doesn't have jobs.")

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
            self.rf[min(H, self.max_horizon)-1] >= o.rf[self.max_horizon-1] and
            self.df[min(H, self.max_horizon)-1] >= o.df[self.max_horizon-1] and
            all([self.rf[i] >= o.rf[i] for i in xrange(min(H, self.max_horizon))]) and
            all([self.df[i] >= o.df[i] for i in xrange(min(H, self.max_horizon))]))
        return condition2
            
    def __gt__(self, o):
        # Like __ge__ except that at SOME point, A and B differ.
        #H = min(self.get_horizon(), self.max_horizon, o.get_horizon())
        H = min(self.get_horizon(), o.get_horizon())
        return (self >= o and
            not (self.get_rfdf()[0][:H] == o.get_rfdf()[0][:H] and
            self.get_rfdf()[1][:H] == o.get_rfdf()[1][:H]))

    def __str__(self):
        return ('[ABSTRACT]' + ', ' + 
            str(self.get_rf()) + ", " + str(self.get_df()) + ", " + 
            str(len(self.get_rf())))



class DiscardingRfDfStore(path.rffullpath.DiscardingRfStore):
    
    """A basic PathStore for Paths in rf and df computations. Discard all
    dominated paths. So far identical to DiscardingRfStore.
    """

    def __init__(self, D):
        super(DiscardingRfDfStore, self).__init__(D)



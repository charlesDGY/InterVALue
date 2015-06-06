import path


class FullMarkedPath(path.DbfPath):

    """Stores entire concrete marked paths without abstraction.
    Only useful for dbf (utilization does not care about markings).
    """

    def __init__(self, jobs, markings=None):
        """ Initialize marked path. If no markings are given, assume 
        fully marked  path. """
        if markings is None:
            self.markings = [True] * len(jobs)
        else:
            self.markings = markings
        super(FullMarkedPath, self).__init__(jobs)

    def get_e(self):
        return sum([job.get_e() for (job, m) in zip(self.jobs, self.markings) 
            if m])

    def get_p(self):
        p = 0
        
        for i in xrange(len(self.jobs) - 1):
            p += self.jobs[i].succs[self.jobs[i + 1]]
        return p

    def get_d(self):
        dmax = 0
        for j in xrange(len(self.jobs)):
            if self.markings[j]:
                d = 0
                for i in xrange(j):
                    d += self.jobs[i].succs[self.jobs[i + 1]]
                d += self.jobs[j].get_d()
                dmax = max(d, dmax)
        return dmax

    def get_start(self):
        return self.jobs[0]

    def get_end(self):
        return self.jobs[-1]

    def is_endmarked(self):
        return self.markings[-1]

    def get_extended(self, job):
        path1 = FullMarkedPath(self.jobs + [job], self.markings + [True])
        path2 = FullMarkedPath(self.jobs + [job], self.markings + [False])
        return [path1, path2]

    def __len__(self):
        return len(self.jobs) - 1

    def __str__(self):
        jobstrs = []
        for (job, marking) in zip(self.jobs, self.markings):
            if marking:
                jobstrs.append(str(job) + "[x]")
            else:
                jobstrs.append(str(job) + "[o]")
        
        return '[' + ' -> '.join(map(str, jobstrs)) + ']'


class FullMarkedPathOptimized(FullMarkedPath):

    """Stores entire concrete marked paths without abstraction.
    Only useful for dbf (utilization does not care about markings).

    Optimized version, only creating new end-nonmarked paths if:
        - future extensions' deadlines could be hidden, and
        - are not already potentially hidden
    """

    def __init__(self, jobs, markings=None):
        super(FullMarkedPathOptimized, self).__init__(jobs, markings)

    def get_extended(self, job):
        path1 = FullMarkedPath(self.jobs + [job], self.markings + [True])

        if len(job.succs) > 0:
            pmin = min(job.succs.values())
            if (path1.get_d() > pmin) and (self.get_d() <= pmin):
                create = True
            else:
                create = False
        else:
            create = False

        if not create:
            return [path1]
        else:
            path2 = FullMarkedPath(self.jobs + [job], self.markings + [False])
            return [path1, path2]


class FullMarkedPathStore(path.DbfPathStore):
    
    """A basic PathStore for Paths in dbf computations. Only discards paths
    that have a deadline exceeding the bound <D>.
    """

    def should_be_stored(self, path):
        return (path.get_d() <= self.D and path.get_p() <= self.D)



# Export path abstractions and stores in the standard format.
DbfPath = FullMarkedPath
UtilizationPath = path.fullpath.FullUtilizationPath
DbfStore = FullMarkedPathStore
UtilizationStore = path.UtilizationPathStore


import path


class FullDbfPath(path.DbfPath):

    """Stores entire concrete paths (i.e., it performs no
    abstractions at all). Domination relation for dbf computations.
    """

    def get_e(self):
        return sum([job.get_e() for job in self.jobs])

    def get_d(self):
        d = 0
        for i in xrange(len(self.jobs) - 1):
            d += self.jobs[i].succs[self.jobs[i + 1]]
        d += self.jobs[-1].get_d()
        return d

    def get_end(self):
        return self.jobs[-1]

    def get_extended(self, job):
        return [FullDbfPath(self.jobs[:] + [job])]

    def __len__(self):
        return len(self.jobs) - 1

    def __ge__(self, o):
        return (self.get_end() == o.get_end() 
            and self.get_e() >= o.get_e() 
            and self.get_d() <= o.get_d())
			
    def __gt__(self, o):
        return (self >= o and (self.get_e() != o.get_e() 
            or self.get_d() != o.get_d()))

    def __str__(self):
        return '[' + ' -> '.join(map(str, self.jobs)) + ']'


class FullUtilizationPath(path.UtilizationPath):

    """Stores entire concrete paths (i.e., it performs no
    abstractions at all). Domination relation for utilization computations.
    """

    def get_p(self):
        p = 0
        for i in xrange(len(self.jobs) - 1):
            p += self.jobs[i].succs[self.jobs[i + 1]]
        return p

    def get_e2(self):
        return sum([job.get_e() for job in self.jobs[:-1]])

    def get_start(self):
        return self.jobs[0]

    def get_end(self):
        return self.jobs[-1]

    def get_extended(self, job):
        return [FullUtilizationPath(self.jobs[:] + [job])]

    def __len__(self):
        return len(self.jobs) - 1

    def __ge__(self, o):
        return (self.get_start() == o.get_start()
            and self.get_end() == o.get_end() 
            and self.get_e2() * o.get_p() >= o.get_e2() * self.get_p())
			
    def __gt__(self, o):
        return (self >= o 
            and (self.get_e2() * o.get_p() > o.get_e2() * self.get_p()))

    def __str__(self):
        return '[' + ' -> '.join(map(str, self.jobs)) + ']'


# Export path abstractions and stores in the standard format.
DbfPath = FullDbfPath
UtilizationPath = FullUtilizationPath
DbfStore = path.DbfPathStore
UtilizationStore = path.UtilizationPathStore


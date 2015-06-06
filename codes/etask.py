import debug
from debug import debug_print as dp
import task

class EJob(task.Job):

    def __init__(self, E, D, name, origjob, countdowns):
        self.origjob = origjob
        self.countdowns = countdowns
        super(EJob, self).__init__(E, D, name)
        

class ETask(task.Task):

    """An EDRT Task, i.e., graph of jobs with additional inter-release 
    separation constraints. Feasibility analysis is done by reducing to
    ordinary DRT Task.
    """

#    def genTuplesM(lst):
#        return reduce(lambda prev, values: [xs + [i] for xs in prev for i in values], lst, [[]])


    def __init__(self, jobs, C, name='T'):
        """Create the ETask by embedding an ordinary dbf-equivalent task.
        C are the constraints, assumed to be a list of triples (u, v, c)
        """
        k = len(C)
        countdown_values = [range(C[i][2]+1) for i in xrange(k)]
#        countdowns = genTuplesM(countdown_values)
        
        countdowns_lists = reduce(lambda prev, values: [xs + [i] for xs in prev for i in values], countdown_values, [[]])
        countdowns = map(lambda x: tuple(x), countdowns_lists)

        # Contains per job and per countdown combination the corresponding 
        # job object
        jobmatrix = dict()

        # Create new jobs (graph vertices)
        for j in jobs:
            jobmatrix[j] = dict()
            for cd in countdowns:
                # Check whether cd is valid, i.e. maximal for all 
                # outgoing constraints
                if reduce(lambda ok, i: ok and (C[i][0] != j or 
                       C[i][2] == cd[i]), xrange(k), True):
                    newjob = EJob(j.get_e(), j.get_d(), 
                        "(" + j.get_name() + ", " + str(cd) + ")",
                        j, cd)
                    jobmatrix[j][cd] = newjob
        
        # Create edges
        for j in jobs:
            for cd in jobmatrix[j].keys():
                for (j2, sep) in j.succs.items():
                    # Max over sep and all cd components that are incoming
                    # for j2
                    delta = reduce(lambda curmax, i: (max(curmax, cd[i]) if 
                        C[i][1] == j2 else curmax), xrange(k), sep)
                    # Compute new cd2
                    cd2 = tuple((max(0, cd[i] - delta) if C[i][0] != j2 else 
                        C[i][2]) for i in xrange(k))
                    jobmatrix[j][cd].add_succ(jobmatrix[j2][cd2], delta)

        # Generate list of new jobs from jobmatrix
        newjobs = reduce(lambda x, y: x+y.values(), jobmatrix.values(), [])

        dp(2, 0, "Original task has %d jobs and %d constraints." % (len(jobs), 
            len(C)))
        dp(2, 0, "Embedded task will have %d jobs." % len(newjobs))
        dp(1, 0, "Creating now embedded task...")
        debug.down(1)
        self.embtask = task.Task(newjobs, name=("E" + name))
        debug.up(1)

        self.C = C
        super(ETask, self).__init__(jobs, name)

    def clean_embtask(self):
        dp(1, 0, "Cleaning embedded task from unnecessary jobs...")
        dp(2, 1, "Embedded task has %d jobs." % len(self.embtask.jobs))
        
        # Find unnecessary jobs
        unnecessaries = set([])
        for j in self.embtask.jobs:
            # Each countdown i is ok if 
            # * constraint i starts at j.origjob or
            # * countdown i is 0
            if not reduce(lambda ok, i: ok and (self.C[i][0] == j.origjob or 
                   j.countdowns[i] == 0), xrange(len(self.C)), True):
                unnecessaries.add(j)

        # Iterate removal until nothing more removed
        while True:
            aresuccessors = set()
            for j in self.embtask.jobs:
                for succ in j.succs.keys():
                    aresuccessors.add(succ)
            removals = []
            for j in unnecessaries:
                if not j in aresuccessors:
                    # j can be removed
                    removals += [j]
                    dp(3, 2, "Removing job %s." % str(j))
            for j in removals:
                self.embtask.jobs.remove(j)
                unnecessaries.remove(j)
            dp(2, 1, "Removed %d jobs." % len(removals))
            if len(removals) == 0:
                break
        dp(2, 1, "Done. Embedded task has now %d jobs." % 
            len(self.embtask.jobs))
        

    def get_e_sum(self):
        return self.embtask.get_e_sum()

    def get_dbf(self, t):
        return self.embtask.get_dbf(t)

    def get_utilization(self):
        return self.embtask.get_utilization()

    def prepare_dbf(self, D):
        self.embtask.prepare_dbf(D)

    def prepare_utilization(self):
        self.embtask.prepare_utilization()


    def render(self, filename, distance=3):

        import pygraphviz as pgv

        G = pgv.AGraph(directed=True, strict=False)
        for job in self.jobs:
            G.add_node(job.name, label=("%s <%d, %d>" % (job.name, job.get_e(), job.get_d())))
        for job in self.jobs:
            for succ in job.succs.keys():
                G.add_edge(job.name, succ.name, label=job.succs[succ], len=distance)
        for c in self.C:
            G.add_edge(c[0], c[1], label=c[2], len=3, style="dashed")
        G.layout(prog="neato")
        G.draw(filename)


        
    

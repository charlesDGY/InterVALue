import task
import etask
import random

class SimpleETask(etask.ETask):

    def __init__(self, name="SimpleETask"):

        v1 = task.Job(1, 2, 'v1')
        v2 = task.Job(1, 1, 'v2')
        v3 = task.Job(2, 3, 'v3')

        v1.add_succ(v2, 2)
        v2.add_succ(v3, 2)

        C = [(v1, v3, 5)]

        super(SimpleETask, self).__init__([v1, v2, v3], C, name)


class CircularETask(etask.ETask):

    def __init__(self, name="SimpleETask"):

        v1 = task.Job(1, 2, 'v1')
        v2 = task.Job(1, 2, 'v2')
        v3 = task.Job(1, 2, 'v3')

        v1.add_succ(v2, 1)
        v2.add_succ(v3, 2)
        v3.add_succ(v1, 1)

        C = [(v1, v1, 5), (v3, v2, 3)]

        super(CircularETask, self).__init__([v1, v2, v3], C, name)


class DominationDemoETask(etask.ETask):

    def __init__(self, name="SimpleETask"):

        v1 = task.Job(1, 9, 'v1')
        v2 = task.Job(1, 9, 'v2')
        v3 = task.Job(2, 9, 'v3')
        v4 = task.Job(3, 9, 'v4')
        v5 = task.Job(1, 9, 'v5')

        v1.add_succ(v2, 2)
        v1.add_succ(v4, 3)
        v2.add_succ(v3, 4)
        v2.add_succ(v1, 5)
        v3.add_succ(v4, 3)
        v4.add_succ(v5, 3)

        C = [(v1, v5, 10)]

        super(DominationDemoETask, self).__init__([v1, v2, v3, v4, v5], C, name)


class EDRTPaperTask(etask.ETask):

    def __init__(self, name="EDRTPaperTask"):

        v1 = task.Job(4, 5, 'v1')
        v2 = task.Job(2, 4, 'v2')
        v3 = task.Job(2, 5, 'v3')
        v4 = task.Job(1, 5, 'v4')
        v5 = task.Job(1, 3, 'v5')

        v1.add_succ(v2, 5)
        v1.add_succ(v4, 7)
        v2.add_succ(v3, 2)
        v3.add_succ(v5, 2)
        v4.add_succ(v5, 2)
        v5.add_succ(v2, 3)
        v5.add_succ(v4, 2)

        C = [(v4, v2, 6), (v3, v3, 9)]

        super(EDRTPaperTask, self).__init__([v1, v2, v3, v4, v5], C, name)


class EDRTPaperTaskConstrained(etask.ETask):

    def __init__(self, name="EDRTPaperTask"):

        v1 = task.Job(4, 5, 'v1')
        v2 = task.Job(2, 2, 'v2')
        v3 = task.Job(2, 2, 'v3')
        v4 = task.Job(1, 2, 'v4')
        v5 = task.Job(1, 2, 'v5')

        v1.add_succ(v2, 5)
        v1.add_succ(v4, 6)
        v2.add_succ(v3, 2)
        v3.add_succ(v5, 2)
        v4.add_succ(v5, 2)
        v5.add_succ(v2, 3)
        v5.add_succ(v4, 2)

        C = [(v4, v2, 6), (v3, v3, 9)]

        super(EDRTPaperTaskConstrained, self).__init__([v1, v2, v3, v4, v5], C, name)


class EDRTPaperFullDemoTask(etask.ETask):

    def __init__(self, name="EDRTPaperFullDemoTask"):

        v1 = task.Job(1, 2, 'v1')
        v2 = task.Job(1, 3, 'v2')
        v3 = task.Job(2, 3, 'v3')
        v4 = task.Job(2, 4, 'v4')

        v1.add_succ(v2, 0)
        v1.add_succ(v3, 5)
        v2.add_succ(v1, 0)
        v3.add_succ(v4, 2)
        v4.add_succ(v2, 2)

        C = [(v1, v1, 2), (v3, v2, 5)]

        super(EDRTPaperFullDemoTask, self).__init__([v1, v2, v3, v4], C, name)



class PaperTask(task.Task):

    def __init__(self, name='PaperTask'):
        # Create the job types of the example task.
        v1 = task.Job(2, 5, 'v1')
        v2 = task.Job(1, 8, 'v2')
        v3 = task.Job(3, 8, 'v3')
        v4 = task.Job(5, 10, 'v4')
        v5 = task.Job(1, 5, 'v5')

        # Create the connections between them.
        v1.add_succ(v2, 10)
        v1.add_succ(v5, 20)
        v2.add_succ(v3, 15)
        v2.add_succ(v4, 20)
        v3.add_succ(v1, 11)
        v4.add_succ(v2, 20)
        v5.add_succ(v4, 10)

        super(PaperTask, self).__init__([v1, v2, v3, v4, v5], name)


class PaperArbitraryTask(task.Task):

    def __init__(self, name='PaperArbitraryTask'):
        # Create the job types of the example task.
        v1 = task.Job(5, 7, 'v1')
        v2 = task.Job(1, 10, 'v2')
        v3 = task.Job(2, 5, 'v3')

        # Create the connections between them.
        v1.add_succ(v2, 8)
        v2.add_succ(v3, 3)
        v3.add_succ(v1, 1000)

        super(PaperArbitraryTask, self).__init__([v1, v2, v3], name)


class RandomTask(task.Task):

    def __init__(self, size_min, size_max, fanout_min, fanout_max,
            p_min, p_max, e_min, e_max, d_min, d_max, d_implicit=False,
            d_arbitrary=False, connected=True, name='RandomTask'):
        size = random.randint(size_min, size_max)
        """Strategy:
        (1) Create all jobs with uniformly random E (leave D at None for now!)
        (2) Create all edges with uniformly random P
        (2a) First a circle 1->2->3->...->1 if connected
        (2b) Then all remaining edges
        (3) Assign D to all jobs in accordance with d_arbitrary and d_implicit,
                within these bounds do uniform choice.
        """


        # Create all job types with random parameters.
        jobs = []
        for i in xrange(size):
            e = random.randint(e_min, e_max)
            d = None
            jobs.append(task.Job(e, d, '%s_v%d' % (name, i + 1)))

        # Connect job i to job i + 1 (to ensure fully connected graph).
        if connected:
            for i in xrange(size):
                p = random.randint(max(p_min, jobs[i].E), p_max)
                jobs[i].add_succ(jobs[(i + 1) % size], p)

        # Pick the rest of the successors randomly.
        for job in jobs:
            fanout = random.randint(fanout_min, fanout_max) - 1
            while fanout > 0 and len(jobs) > len(job.succs) + 1:
                succ = random.choice(jobs)
                if succ in job.succs:
                    continue
                p = random.randint(max(p_min, job.E), p_max)
                job.add_succ(succ, p)
                fanout -= 1

        # Set deadlines.
        for job in jobs:
            if d_arbitrary:
                job.D = random.randint(max(job.E, d_min), d_max)
            elif d_implicit:
                # Use d_max here also in case job does not have successors
                job.D = min([d_max] + job.succs.values())
            else:
                job.D = random.randint(max(job.E, d_min), min([d_max] + job.succs.values()))

        super(RandomTask, self).__init__(jobs, name)


class RandomTaskNew(task.Task):

    def __init__(self, size_min, size_max, fanout_min, fanout_max,
            p_min, p_max, ratioed_min, ratioed_max, connected=True,
            d_implicit = False,
            name='RandomTask'):
        size = random.randint(size_min, size_max)
        """New strategy:
        (1) Create all edges with uniformly random P
        (2) Create random D for all vertices, bounded by minimal outgoing p
        (3) Create random E for all vertices consistent with given ratio range

        Implicit: Deadlines implicitly constrained but random.
        """

        # Create all job types without parameters for now
        jobs = []
        for i in xrange(size):
            e = None
            d = None
            jobs.append(task.Job(e, d, '%s_v%d' % (name, i + 1)))

        # Connect job i to job i + 1 (to ensure fully connected graph).
        if connected:
            for i in xrange(size):
                p = random.randint(p_min, p_max)
                jobs[i].add_succ(jobs[(i + 1) % size], p)

        # Pick the rest of the successors randomly.
        for job in jobs:
            fanout = random.randint(fanout_min, fanout_max) - 1
            while fanout > 0 and len(jobs) > len(job.succs) + 1:
                succ = random.choice(jobs)
                if succ in job.succs:
                    continue
                p = random.randint(p_min, p_max)
                job.add_succ(succ, p)
                fanout -= 1

        # Set deadlines.
        for job in jobs:
            if d_implicit:
                job.D = min(job.succs.values() + [p_max])
            else:
                job.D = random.randint(min(job.succs.values())/2, min(job.succs.values()))

        # Set execution times.
        for job in jobs:
            job.E = random.randint(max(1, int(job.D * ratioed_min)),
		max(1, int(job.D * ratioed_max)))

        super(RandomTaskNew, self).__init__(jobs, name)


class SODATaskH(task.Task):

    def __init__(self, name='SODATaskH'):
        # Create the job types of the example task.
        v1 = task.Job(3, 4, 'v1')
        v2 = task.Job(5, 8, 'v2')
        v3 = task.Job(1, 15, 'v3')
        v4 = task.Job(1, 16, 'v4')
        v5 = task.Job(1, 17, 'v5')

        # Create the connections between them.
        v1.add_succ(v2, 10)
        v2.add_succ(v3, 11)
        v2.add_succ(v4, 11)
        v1.add_succ(v5, 12)
        v3.add_succ(v1, 20)
        v4.add_succ(v1, 20)
        v5.add_succ(v1, 20)

        super(SODATaskH, self).__init__([v1, v2, v3, v4, v5], name)


class SODATaskL(task.Task):

    def __init__(self, name='SODATaskL'):
        # Create the job types of the example task.
        v1 = task.Job(1, 9, 'v1')
        v2 = task.Job(2, 7, 'v2')
        v3 = task.Job(3, 7, 'v3')
        v4 = task.Job(1, 8, 'v4')
        v5 = task.Job(1, 10, 'v5')

        # Create the connections between them.
        v1.add_succ(v2, 10)
        v2.add_succ(v3, 8)
        v3.add_succ(v4, 7)
        v4.add_succ(v5, 5)
        v5.add_succ(v1, 10)

        super(SODATaskL, self).__init__([v1, v2, v3, v4, v5], name)


class Ex1a(task.Task):

    def __init__(self, name='Ex1a'):
        # Create the job types of the example task.
        v1 = task.Job(3, 5, 'v1')
        v2 = task.Job(2, 5, 'v2')
        v3 = task.Job(1, 3, 'v3')

        # Create the connections between them.
        v1.add_succ(v2, 6)
        v1.add_succ(v3, 5)
        v2.add_succ(v3, 5)
        v3.add_succ(v2, 3)

        super(Ex1a, self).__init__([v1, v2, v3], name)

class Ex1b(task.Task):

    def __init__(self, name='Ex1b'):
        # Create the job types of the example task.
        u = task.Job(5, 10, 'u')

        # Create the connections between them.
        u.add_succ(u, 20)

        super(Ex1b, self).__init__([u], name)

class Ex1(task.TaskSet):

    def __init__(self):
        super(Ex1, self).__init__([Ex1a(), Ex1b()])


class PeriodicTask(task.Task):

    def __init__(self, c, d, p, name, namepattern='v_%s'):

        v = task.Job(c, d, namepattern % name)
        v.add_succ(v, p)

        super(PeriodicTask, self).__init__([v], name)

class GMFTask(task.Task):

    def __init__(self, jtlist, name, namepattern='v_%d'):

        vs = []
        for (i, jt) in zip(range(len(jtlist)), jtlist):
            j = task.Job(jt[0], jt[1], namepattern % i)
            if len(vs) > 0:
                vs[-1].add_succ(j, jtlist[i-1][2])
            vs.append(j)
        vs[-1].add_succ(vs[0], jtlist[-1][2])

        super(GMFTask, self).__init__(vs, name)

class Ex2(task.TaskSet):
    """ This singleton task set causes interference of 12 in a 20 time units
    interval. Thus, interference_test(9, 20) will succeed, but reducing wcet
    to 8 will fail."""

    def __init__(self):

        v1 = task.Job(1, 8, "v1")
        v2 = task.Job(5, 7, "v2")
        v3 = task.Job(2, 4, "v3")

        v1.add_succ(v2, 10)
        v1.add_succ(v3, 8)
        v2.add_succ(v3, 7)
        v3.add_succ(v3, 4)
        v3.add_succ(v1, 12)

        T = task.Task([v1, v2, v3], "T")

        super(Ex2, self).__init__([T])


class Ex3(task.TaskSet):
    """Example for fp schedulability and feasibility.
    In given priority order, task set is fp schedulable.
    In order [T1, T2, T4, T3] it is not.
    In any order, it is fp feasible.
    If you add a PeriodicTask(2, 25, 25, 'T5'), it is feasible but not fp feasible.
    """

    def __init__(self):

        T1 = PeriodicTask(1, 2, 10, "T1", "u_%s")

        v1 = task.Job(1, 8, "v1")
        v2 = task.Job(5, 7, "v2")
        v3 = task.Job(2, 4, "v3")

        v1.add_succ(v2, 10)
        v1.add_succ(v3, 8)
        v2.add_succ(v3, 7)
        v3.add_succ(v3, 4)
        v3.add_succ(v1, 12)

        T2 = task.Task([v1, v2, v3], "T2")

        w1 = task.Job(6, 20, "w1")
        w2 = task.Job(1, 100, "w2")

        w1.add_succ(w2, 50)
        w2.add_succ(w1, 100)

        T3 = task.Task([w1, w2], "T3")

        T4 = PeriodicTask(1, 100, 100, "T4", "x_%s")

        super(Ex3, self).__init__([T1, T2, T3, T4])


class Ex4(task.TaskSet):
    """Example for effectiveness of precision.
    Fails at abstraction level 0
    Succeeds at abstraction level None
    """

    def __init__(self):

        T1 = GMFTask([(1, 4, 4), (2, 6, 6), (4, 10, 10)], "T1")

        T2 = PeriodicTask(6, 12, 100, "T2", "x_%s")

        super(Ex4, self).__init__([T1, T2])


class HMLTaskSet(task.TaskSet):

    def __init__(self):

        Htasks = [RandomTask(size_min=7, size_max=15,
                    fanout_min=1, fanout_max=5,
                    p_min=50, p_max=100,
                    e_min=1, e_max=1,
                    d_min=100, d_max=100,
                    #d_min=100, d_max=400,
                    d_implicit=True,
                    name="HT%d"%i) for i in range(100)]
        Mtasks = [RandomTask(size_min=7, size_max=15,
                    fanout_min=1, fanout_max=5,
                    p_min=100, p_max=200,
                    e_min=1, e_max=2,
                    d_min=200, d_max=200,
                    #d_min=100, d_max=400,
                    d_implicit=True,
                    name="MT%d"%i) for i in range(100)]
        Ltasks = [RandomTask(size_min=7, size_max=15,
                    fanout_min=1, fanout_max=5,
                    p_min=200, p_max=350,
                    e_min=2, e_max=3,
                    d_min=350, d_max=350,
                    #d_min=100, d_max=400,
                    d_implicit=True,
                    name="LT%d"%i) for i in range(100)]

        tasks = [T for l in zip(Htasks, Mtasks, Ltasks) for T in l]

        super(HMLTaskSet, self).__init__(tasks)


class RFExample(task.TaskSet):
    """Example task from RTSS'13 paper."""

    def __init__(self):

        v1 = task.Job(6, 10, "v1")
        v2 = task.Job(5, 25, "v2")
        v3 = task.Job(1, 10, "v3")
        v4 = task.Job(2, 12, "v4")
        v5 = task.Job(10, 50, "v5")

        v1.add_succ(v2, 13)
        v2.add_succ(v3, 29)
        v2.add_succ(v4, 100)
        v3.add_succ(v4, 10)
        v3.add_succ(v5, 18)
        v4.add_succ(v1, 12)
        v4.add_succ(v2, 25)
        v5.add_succ(v5, 50)

        T1 = task.Task([v1, v2, v3, v4, v5], "T1")

        super(RFExample, self).__init__([T1])


class RTATask(task.Task):

    def __init__(self, name="RTATask"):

        v1 = task.Job(3, 10, 'v1')
        v2 = task.Job(4, 10, 'v2')
        v3 = task.Job(1,  3, 'v3')
        v4 = task.Job(6, 12, 'v4')
        v5 = task.Job(4,  8, 'v5')

        v1.add_succ(v2, 10)
        v1.add_succ(v3, 15)
        v2.add_succ(v1, 15)
        v2.add_succ(v4, 17)
        v3.add_succ(v5, 30)
        v4.add_succ(v1, 12)
        v5.add_succ(v4, 8)
        v5.add_succ(v5, 20)

        super(RTATask, self).__init__([v1, v2, v3, v4, v5], name)



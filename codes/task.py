import cPickle
import time
import subprocess
import itertools
import heapq

import engine
import debug
from debug import debug_print as dp
import path.fullpath
import path.fullmarkedpath
import path.triple
import path.quadruple

import path.fullpathdiscard
import path.rffullpath

import path.rbf
import path.rfdf
import path.dfreverse

import booleanformulas as bf

gg_dummy = False
gg_min_swm = 1
gg_loop_once = False
# Size of an exclusion constraint be to be considered, i.e., saved.
# This is size ABOVE number of tasks.
# Too low: Creates too many constraints that don't purge many combinations
# Too high: Overlooks too many interesting constraints, i.e., purging opportunities
xx_ec_threshold = 4
# Number of exclusion constraints to keep. The buffer is FIFO.
# Too low: Discards too many constraints, i.e., purging opportunities
# Too high:
xx_ec_maxsize = 3
# Abstraction levels for (non-iterative) rf solver.
# Legal values are just 0 and None. Method is only complete if None is in the list.
xx_abstraction_levels = [0, None]
#
xx_default_solver = 'rf_iterative'

# Record number of tested path combinations.
xx_stats_combinations_tested = 0
# Record number of skipped path combinations (because of exclusion constraint).
xx_stats_combinations_skipped = 0
#
xx_stats_jobs_tested = 0
xx_stats_jobs_ncj = 0
#
xx_stats_al_testcounts = dict(zip(xx_abstraction_levels,
    [0] * len(xx_abstraction_levels)))
xx_stats_al_nonzero_schedulable = 0

# List of tuples (tested, total) for refinement rt test
xx_stats_combi = []
xx_stats_combi_MAXLEN = 100000

# Total RT computations vs. those improved by abstraction refinement
xx_stats_rt_improved = 0
xx_stats_rt_total = 0
# Record the improvements
xx_stats_rt_improvements = list()

# Statistics for skipx optimization
xx_stats_skipx_skipped = 0
xx_stats_skipx_notskipped = 0


class Job(object):

    """A basic representation of job types. Each job type has an
    execution time requirement, a deadline and any number of successor
    job types. Each successor is associated with a separation time
    (or period).
    """

    def __init__(self, E, D, name='J', task=None):
        self.E = E
        self.D = D
        self.name = name
        self.succs = {}
        self.prevs = None
        self.mindelay = float('Inf')
        self.minprevdelay = None
        self.task = task

    def add_succ(self, job, separation):
        self.succs[job] = separation
        self.mindelay = min(self.mindelay, separation)

    def get_e(self):
        return self.E

    def get_d(self):
        return self.D

    def get_name(self):
        return str(self.name)

    def get_mindelay(self, forced = False):
        if forced:
            self.mindelay = min(self.succs.values())
        return self.mindelay

    def get_prevs(self, forced = False):
        """ Returns list (!) of predecessor vertices. """
        if self.task is None:
            # We need to know all jobs
            return None
        if forced or self.prevs is None:
            self.prevs = [j for j in self.task.jobs if self in j.succs]
        return self.prevs

    def get_minprevdelay(self, forced = False):
        if self.task is None:
            # We need to know all jobs
            return None
        if forced or self.minprevdelay is None:
            self.minprevdelay = float('Inf')
            for prev_job in self.get_prevs():
                self.minprevdelay = min(self.minprevdelay,
                    prev_job.succs[self])
        return self.minprevdelay

    def set_task(self, task):
        self.task = task

    def get_task(self):
        return self.task

    def __str__(self):
#        return str("%(name)s" % self.__dict__)
        return str("%(name)s(%(E)d, %(D)d)" % self.__dict__)

    def dominates(self, j2, strict=False):
        # Let's not get into the business of overloading < and <=
        # or rely on default behavior
        return (((self.E >= j2.E) and (self.D <= j2.D)) if not strict else
            self.dominates(j2) and ((self.E != j2.E) or (self.D != j2.D)))


class Task(object):

    """A Task is a graph of jobs (or job types), for which we can compute
    the utilization and the demand bound function (dbf).
    """

    def __init__(self, jobs, name='T'):
        """Create a TaskSet out of the collection of <jobs>, with an
        optional <name>. The path abstractions to be used can be specified,
        otherwise the fullpath abstraction is used. (Not very abstract then.)
        """
        self.jobs = set(jobs)
        for j in jobs:
            j.set_task(self)
        self.name = name
        self.reset()

        # Determine if this is an arbitrary deadlines task
        self.constrained = True
        for j in self.jobs:
            for sep in j.succs.values():
                if sep < j.get_d():
                    self.constrained = False

        # Set default path abstractions accordingly
        if self.constrained:
            dp(1, 0, "This is a constrained deadlines task.")
            dp(2, 1, "Defaulting to demand triple abstractions:")
            self.dbf_path_class = path.triple.DbfPath
#            self.dbf_store_class = path.triple.DbfStore
            self.dbf_store_class = path.discardingstores.DiscardingSortedDbfStoreNoD
            self.utilization_path_class = path.triple.UtilizationPath
            self.utilization_store_class = path.triple.UtilizationStore
            self.rf_path_class = path.rffullpath.FullRfPath
#            self.rf_store_class = path.RfPathStore
            self.rf_store_class = path.rffullpath.DiscardingRfStore
            self.rfdf_path_class = path.rfdf.FullRfDfPath
            self.rfdf_store_class = path.rfdf.DiscardingRfDfStore
        else:
            dp(1, 0, "This is an arbitrary deadlines task.")
            dp(2, 1, "Defaulting to demand quadruple abstractions:")
            self.dbf_path_class = path.quadruple.DbfPath
            self.dbf_store_class = path.quadruple.DbfStore
            self.utilization_path_class = path.quadruple.UtilizationPath
            self.utilization_store_class = path.quadruple.UtilizationStore
        dp(2, 2, 'Dbf Path class:  %s' % self.dbf_path_class.__name__)
        dp(2, 2, 'Dbf Store class: %s' % self.dbf_store_class.__name__)
        dp(2, 2, 'Utilization Path class:  %s' % self.utilization_path_class.__name__)
        dp(2, 2, 'Utilization Store class: %s' % self.utilization_store_class.__name__)

    def reset(self):
        self.U = None
        self.dbf = None
        self.rbf = None
        self.rfpaths_cache = dict()
        self.rfdfpaths_cache = dict()
        self.dfreversepaths_cache = dict([(v, dict()) for v in self.jobs])
        self.dom_cache = dict()

    def set_dbf_path_abstraction(self, path_class):
        self.dbf_path_class = path_class

    def set_dbf_store_abstraction(self, store_class):
        self.dbf_store_class = store_class

    def set_utilization_path_abstraction(self, path_class):
        self.utilization_path_class = path_class

    def set_utilization_store_abstraction(self, store_class):
        self.utilization_store_class = store_class

    def get_jobs(self):
        """Returns a set containing all jobtypes in this task.
        """
        return self.jobs.copy()

    def get_e_sum(self):
        """Return the sum of the execution times of all the job (types)
        in the Task.
        """
        return sum([job.E for job in self.jobs])

    def reachable(self, jt1, jt2, t):
        """Returns True iff jt1 can reach jt2 within t time units.
        """
        # TODO: test more thoroughly

        min_durations = dict([(j, jt1.succs[j]) if j in jt1.succs else (j, "x")
            for j in self.jobs])
#        print ["%s: %s" % (j, min_durations[j]) for j in self.jobs]

        # At each step, update the dict with new step info. The minimal
        # value will strictly increase and eventually exceed t.
        for i in range(len(self.jobs)):
            # "x" compares larger than all integers
            new_durations = min_durations.copy()
            for job in [j for j in self.jobs if min_durations[j] < "x"]:
                for succ_job in job.succs.keys():
                    new_durations[succ_job] = min(
                        min_durations[job] + job.succs[succ_job],
                        new_durations[succ_job])
#                    dp(2, 2, "Reaching now %s within %d time units." % (succ_job, new_durations[succ_job]))
            min_durations = new_durations.copy()
#            print ["%s: %s" % (j, min_durations[j]) for j in self.jobs]
        return (min_durations[jt2] <= t)

    def get_max_releases(self, t):
        """Returns the maximal number of job releases by this task during
        any interval of size t.
        """
        releases = 0

        # This dict will contain for each job the minimal duration in
        # which the current number of jobs (counted in variable releases)
        # can be releases with this job being the last one.
        min_durations = dict.fromkeys(self.jobs, 0)

        # At each step, update the dict with new step info. The minimal
        # value will strictly increase and eventually exceed t.
        while min(min_durations.values()) <= t:
            releases += 1
#            dp(2, 2, "Step %d" % releases)
            # "x" compares larger than all integers
            new_durations = dict.fromkeys(self.jobs, "x")
            for job in filter(lambda j: min_durations[j] < "x", self.jobs):
                for succ_job in job.succs.keys():
                    new_durations[succ_job] = min(
                        min_durations[job] + job.succs[succ_job],
                        new_durations[succ_job])
#                    dp(2, 3, "Reaching %s from %s in time %d." % (succ_job, job, new_durations[succ_job]))
            min_durations = new_durations.copy()
        return releases

    def get_dominance_sets(self, D, abstraction_level=None, force=False):
        if (D, abstraction_level) in self.dom_cache and not force:
            dp(3, 0, "Using cached dominance sets for task %s." % self.name)
        else:
            dp(3, 0, "Building dominance sets for task %s." % self.name)
            dp(3, 1, "D = %d, abstraction level: %s" % (D, str(abstraction_level)))
            dom = dict()

            debug.down(1)
            rfpaths = self.get_rfpaths(D, abstraction_level)
            debug.up(1)

            for rfpath in rfpaths:
                dp(4, 1, "Path %s: %s." % (rfpath.name, str(rfpath)))
                # i = 0
                dom[(rfpath, 0)] = set([p for p in rfpaths
                    if p.get_rf()[0] <= rfpath.get_rf()[0]])
                for i in xrange(1, D):
                    dom[(rfpath, i)] = set([p for p in dom[(rfpath, i-1)]
                        if p.get_rf()[i] <= rfpath.get_rf()[i]])
                for i in xrange(D):
                    dp(5, 2, "dom(%s, %d) = [%s]" % (rfpath.name, i,
                        ', '.join([p.name for p in dom[(rfpath, i)]])))
            self.dom_cache[(D, abstraction_level)] = dom
        return self.dom_cache[(D, abstraction_level)]


    def get_rfpaths(self, D, abstraction_level=None, force=False):

        def rfs_max(paths, maxD):
            return [max([p.get_rf()[i] for p in paths]) for i in range(maxD)]

        return self.get_paths(D, abstraction_level=abstraction_level, force=force,
            prepare_paths = self.prepare_rfpaths,
            paths_cache = self.rfpaths_cache,
            concrete_path_class = path.rffullpath.FullRfPath,
            abstract_path_class = path.rffullpath.AbstractRfPath,
            paths_max = rfs_max,
            add_to_maxpaths = add_to_maxpaths_rf,
            pathtype_str = 'rf functions')


    def get_rfdfpaths(self, D, abstraction_level=None, force=False):

        def rfdfs_max(paths, maxD):
            return ([max([p.get_rfdf()[0][i] for p in paths]) for i in range(maxD)],
                [max([p.get_rfdf()[1][i] for p in paths]) for i in range(maxD)])

        return self.get_paths(D, abstraction_level=abstraction_level, force=force,
            prepare_paths = self.prepare_rfdfpaths,
            paths_cache = self.rfdfpaths_cache,
            concrete_path_class = path.rfdf.FullRfDfPath,
            abstract_path_class = path.rfdf.AbstractRfDfPath,
            paths_max = rfdfs_max,
            add_to_maxpaths = add_to_maxpaths_rfdf,
            pathtype_str = 'rfdf functions')


    def get_dfreversepaths(self, v, D, abstraction_level=None, force=False):
        def dfreverses_max(paths, maxD):
            return [max([p.get_df()[i] for p in paths]) for i in range(maxD)]

        return self.get_paths(D, abstraction_level=abstraction_level, force=force,
            prepare_paths = (lambda maxD: self.prepare_dfreversepaths(v, maxD)),
            paths_cache = self.dfreversepaths_cache[v],
            concrete_path_class = path.dfreverse.DfReversePath,
            abstract_path_class = path.dfreverse.AbstractDfReversePath,
            paths_max = dfreverses_max,
            add_to_maxpaths = add_to_maxpaths_df,
            pathtype_str = 'dfreverse functions')


    def get_paths(self, D,
            prepare_paths,
            paths_cache,
            concrete_path_class,
            abstract_path_class,
            paths_max,
            add_to_maxpaths,
            pathtype_str,
            abstraction_level=None, force=False):
        """Return the functions as lists for this task. Return only
        full functions with D prefix, i.e., defined on domain [0, D-1].

        Abstraction levels:
        None: Concrete paths
        0: One abstract rfpath which is the maximum over all concrete rfs
        1: Hierarchical abstractions from concrete paths. Still returns
            only one abstract rfpath but this one includes two children from
            which it abstracts. The leaves of this tree are all concrete paths.
        """

        if (D, None) > max(paths_cache.keys() + [(-1, None)]) or force:
            prepare_paths(D)
        elif not (D, None) in paths_cache:
            # There is no cached path set for this D, but we can derive one.
            (maxD, _) = max(paths_cache.keys())
            dp(3, 0, "Deriving %s for task %s for D=%d..." % (pathtype_str, self, D))
            dp(4, 1, "Original set for D=%d:" % maxD)
            for path in paths_cache[(maxD, None)]:
                dp(4, 2, "Path %s: %s." % (path.name, str(path)))

            newpaths = set([concrete_path_class(p.jobs, D)
                for p in paths_cache[(maxD, None)]])
            dp(3, 1, "Deriving from %d paths." % len(newpaths))

            timer = time.time()
            dp(3, 1, "Filtering for maximal relevant paths...")
            maxpaths = set()
            add_to_maxpaths(newpaths, maxpaths, D)
            dp(3, 1, 'Done after %.2f s. %d paths left.' % (time.time() - timer,
                len(maxpaths)))

            dp(4, 1, "Resulting new set for D=%d:" % D)
            for i, p in enumerate(maxpaths):
                p.name = "%s_D%d_p%d" % (self.name, D, i)
                dp(4, 2, "Path %s: %s." % (p.name, str(p)))
            paths_cache[(D, None)] = maxpaths
        else:
            dp(3, 0, "Using cached %s for task %s for D=%d..." %
                (pathtype_str, self, D))

        # Here we have non-abstracted paths in the cache.
        # Take care of abstraction now.
        if not (D, abstraction_level) in paths_cache.keys():
            dp(3, 0, "Creating %s for task %s abstraction level '%s'." %
                (pathtype_str, self, str(abstraction_level)))
            if abstraction_level == 0:
                paths = paths_cache[(D, None)]
                maxf = paths_max(paths, D)
                maxpath = abstract_path_class(D, maxf)
                maxpath.name = "%s_A0_D%d" % (self.name, D)
                dp(4, 1, "Path %s: %s." % (maxpath.name, str(maxpath)))
                paths_cache[(D, 0)] = set([maxpath])
            elif abstraction_level == 1:
                paths = paths_cache[(D, None)].copy()
                while len(paths) > 1:
                    # Compute distance matrix
                    distances = list()
                    #[Robin] Instead by combinations ???
                    for ((i1, p1), (i2, p2)) in itertools.product(
                        enumerate(paths), repeat=2):
                        if i1 < i2:
                            distances.append((p1.distance_to(p2), i1, i2, p1, p2))
                    for (d, _, _, p1, p2) in distances:
                        dp(5, 1, "%s to %s: %.3f" % (p1.name, p2.name, d))

                    # Merge path pair with minimal distances
                    (dist, _, _, p1, p2) = min(distances)
                    dp(5, 1, "Minimum choice: %.3f via (%s, %s)" % (dist, p1.name, p2.name))
                    maxf = paths_max([p1, p2], D)
                    maxpath = abstract_path_class(D, maxf,
                        childs = [p1, p2], spread = dist)
                    maxpath.name = "%s_A1_D%d_p%d" % (self.name, D, len(paths)-2)
                    dp(4, 1, "New path %s: %s." % (maxpath.name, str(maxpath)))

                    # Replace merged paths with maximum
                    paths.remove(p1)
                    paths.remove(p2)
                    paths.add(maxpath)
                paths_cache[(D, 1)] = paths

            else:
                raise RuntimeError("Unsupported path abstraction level: %s" %
                    str(abstraction_level))
        else:
            dp(3, 0, "Using cached %s for abstraction level '%s'." %
                (pathtype_str, str(abstraction_level)))


        return paths_cache[(D, abstraction_level)]


    def get_rfpaths_old(self, D, abstraction_level=None, force=False):
        """Return the request functions as lists for this task. Return only
        full functions with D prefix, i.e., defined on domain [0, D-1].

        Abstraction levels:
        None: Concrete paths
        0: One abstract rfpath which is the maximum over all concrete rfs
        1: Hierarchical abstractions from concrete paths. Still returns
            only one abstract rfpath but this one includes two children from
            which it abstracts. The leaves of this tree are all concrete paths.
        """

        if (D, None) > max(self.rfpaths_cache.keys() + [(-1, None)]) or force:
            self.prepare_rfpaths(D)
        elif not (D, None) in self.rfpaths_cache:
            # There is no cached path set for this D, but we can derive one.
            (maxD, _) = max(self.rfpaths_cache.keys())
            dp(3, 0, "Deriving request functions for task %s for D=%d..." % (self, D))
            dp(4, 1, "Original set for D=%d:" % maxD)
            for rfpath in self.rfpaths_cache[(maxD, None)]:
                dp(4, 2, "Path %s: %s." % (rfpath.name, str(rfpath)))

            newrfpaths = set([path.rffullpath.FullRfPath(p.jobs, D)
                for p in self.rfpaths_cache[(maxD, None)]])
            dp(3, 1, "Deriving from %d paths." % len(newrfpaths))

            timer = time.time()
            dp(3, 1, "Filtering for maximal relevant paths...")
            maxpaths = set()
            add_to_maxpaths_rf(newrfpaths, maxpaths, D)
            dp(3, 1, 'Done after %.2f s. %d paths left.' % (time.time() - timer,
                len(maxpaths)))

            dp(4, 1, "Resulting new set for D=%d:" % D)
            for i, p in enumerate(maxpaths):
                p.name = "%s_D%d_p%d" % (self.name, D, i)
                dp(4, 2, "Path %s: %s." % (p.name, str(p)))
            self.rfpaths_cache[(D, None)] = maxpaths
        else:
            dp(3, 0, "Using cached request functions for task %s for D=%d..." % (self, D))

        # Here we have non-abstracted paths in the cache.
        # Take care of abstraction now.
        if not (D, abstraction_level) in self.rfpaths_cache.keys():
            dp(3, 0, "Creating request functions for task %s abstraction level '%s'." %
                (self, str(abstraction_level)))
            if abstraction_level == 0:
                rfpaths = self.rfpaths_cache[(D, None)]
                maxrf = [max([p.get_rf()[i] for p in rfpaths])
                    for i in range(D)]
                maxrfpath = path.rffullpath.AbstractRfPath(D, maxrf)
                maxrfpath.name = "%s_A0_D%d" % (self.name, D)
                dp(4, 1, "Path %s: %s." % (maxrfpath.name, str(maxrfpath)))
                self.rfpaths_cache[(D, 0)] = set([maxrfpath])
            elif abstraction_level == 1:
                rfpaths = self.rfpaths_cache[(D, None)].copy()
                while len(rfpaths) > 1:
                    # Compute distance matrix
                    distances = list()
                    for ((i1, p1), (i2, p2)) in itertools.product(
                        enumerate(rfpaths), repeat=2):
                        if i1 < i2:
                            distances.append((p1.distance_to(p2), i1, i2, p1, p2))
                    for (d, _, _, p1, p2) in distances:
                        dp(5, 1, "%s to %s: %.3f" % (p1.name, p2.name, d))

                    # Merge path pair with minimal distances
                    (dist, _, _, p1, p2) = min(distances)
                    dp(5, 1, "Minimum choice: %.3f via (%s, %s)" % (dist, p1.name, p2.name))
                    maxrf = [max(p1.get_rf()[i], p2.get_rf()[i]) for i in range(D)]
                    maxrfpath = path.rffullpath.AbstractRfPath(D, maxrf,
                        childs = [p1, p2], spread = dist)
                    maxrfpath.name = "%s_A1_D%d_p%d" % (self.name, D, len(rfpaths)-2)
                    dp(4, 1, "New path %s: %s." % (maxrfpath.name, str(maxrfpath)))

                    # Replace merged paths with maximum
                    rfpaths.remove(p1)
                    rfpaths.remove(p2)
                    rfpaths.add(maxrfpath)
                self.rfpaths_cache[(D, 1)] = rfpaths

            else:
                raise RuntimeError("Unsupported path abstraction level: %s" %
                    str(abstraction_level))
        else:
            dp(3, 0, "Using cached request functions for abstraction level '%s'." %
                str(abstraction_level))


        return self.rfpaths_cache[(D, abstraction_level)]

    def get_rfdfpaths_old(self, D, abstraction_level=None, force=False):
        """Return the request and demand functions as lists for this task. Return only
        full functions with D prefix, i.e., defined on domain [0, D-1].

        Abstraction levels:
        None: Concrete paths
        0: One abstract rfpath which is the maximum over all concrete rfs
        1: Hierarchical abstractions from concrete paths. Still returns
            only one abstract rfpath but this one includes two children from
            which it abstracts. The leaves of this tree are all concrete paths.
        """

        # prepare_rfdfpaths
        # rfdfpaths_cache
        # path.rfdf.FullRfDfPath
        # path.rfdf.AbstractRfDfPath
        # max: compute maximum of two rfdfs
        # max: compute maximum of a set of rfdfs

        if (D, None) > max(self.rfdfpaths_cache.keys() + [(-1, None)]) or force:
            self.prepare_rfdfpaths(D)
        elif not (D, None) in self.rfdfpaths_cache:
            # There is no cached path set for this D, but we can derive one.
            (maxD, _) = max(self.rfdfpaths_cache.keys())
            dp(3, 0, "Deriving rfdfs for task %s for D=%d..." % (self, D))
            dp(4, 1, "Original set for D=%d:" % maxD)
            for rfdfpath in self.rfdfpaths_cache[(maxD, None)]:
                dp(4, 2, "Path %s: %s." % (rfdfpath.name, str(rfdfpath)))

            newrfdfpaths = set([path.rfdf.FullRfDfPath(p.jobs, D)
                for p in self.rfdfpaths_cache[(maxD, None)]])
            dp(3, 1, "Deriving from %d paths." % len(newrfdfpaths))

            timer = time.time()
            dp(3, 1, "Filtering for maximal relevant paths...")
            maxpaths = set()
            add_to_maxpaths_rfdf(newrfdfpaths, maxpaths, D)
            dp(3, 1, 'Done after %.2f s. %d paths left.' % (time.time() - timer,
                len(maxpaths)))

            dp(4, 1, "Resulting new set for D=%d:" % D)
            for i, p in enumerate(maxpaths):
                p.name = "%s_D%d_p%d" % (self.name, D, i)
                dp(4, 2, "Path %s: %s." % (p.name, str(p)))
            self.rfdfpaths_cache[(D, None)] = maxpaths
        else:
            dp(3, 0, "Using cached request functions for task %s for D=%d..." % (self, D))

        # Here we have non-abstracted paths in the cache.
        # Take care of abstraction now.
        if not (D, abstraction_level) in self.rfdfpaths_cache.keys():
            dp(3, 0, "Creating request functions for task %s abstraction level '%s'." %
                (self, str(abstraction_level)))
            if abstraction_level == 0:
                rfdfpaths = self.rfdfpaths_cache[(D, None)]
                maxrfdf = ([max([p.get_rfdf()[0] for p in rfdfpaths]) for i in range(D)],
                    [max([p.get_rfdf()[1] for p in rfdfpaths]) for i in range(D)])
                maxrfdfpath = path.rfdf.AbstractRfDfPath(D, maxrfdf)
                maxrfdfpath.name = "%s_A0_D%d" % (self.name, D)
                dp(4, 1, "Path %s: %s." % (maxrfdfpath.name, str(maxrfdfpath)))
                self.rfdfpaths_cache[(D, 0)] = set([maxrfdfpath])
            elif abstraction_level == 1:
                rfdfpaths = self.rfdfpaths_cache[(D, None)].copy()
                while len(rfdfpaths) > 1:
                    # Compute distance matrix
                    distances = list()
                    for ((i1, p1), (i2, p2)) in itertools.product(
                        enumerate(rfdfpaths), repeat=2):
                        if i1 < i2:
                            distances.append((p1.distance_to(p2), i1, i2, p1, p2))
                    for (d, _, _, p1, p2) in distances:
                        dp(5, 1, "%s to %s: %.3f" % (p1.name, p2.name, d))

                    # Merge path pair with minimal distances
                    (dist, _, _, p1, p2) = min(distances)
                    dp(5, 1, "Minimum choice: %.3f via (%s, %s)" % (dist, p1.name, p2.name))
                    maxrfdf = ([max(p1.get_rfdf()[0][i], p2.get_rfdf()[0][i]) for i in range(D)],
                        [max(p1.get_rfdf()[1][i], p2.get_rfdf()[1][i]) for i in range(D)])
                    maxrfdfpath = path.rfdf.AbstractRfDfPath(D, maxrfdf,
                        childs = [p1, p2], spread = dist)
                    maxrfdfpath.name = "%s_A1_D%d_p%d" % (self.name, D, len(rfdfpaths)-2)
                    dp(4, 1, "New path %s: %s." % (maxrfdfpath.name, str(maxrfdfpath)))

                    # Replace merged paths with maximum
                    rfdfpaths.remove(p1)
                    rfdfpaths.remove(p2)
                    rfdfpaths.add(maxrfdfpath)
                self.rfdfpaths_cache[(D, 1)] = rfdfpaths

            else:
                raise RuntimeError("Unsupported path abstraction level: %s" %
                    str(abstraction_level))
        else:
            dp(3, 0, "Using cached request functions for abstraction level '%s'." %
                str(abstraction_level))


        return self.rfdfpaths_cache[(D, abstraction_level)]

    def prepare_rfpaths(self, D):
        """Compute request functions up to D without abstractions."""
        timer = time.time()
        dp(3, 0, "Computing request functions for task %s..." % self)
        dp(4, 1, 'D:           %d' % D)
        dp(4, 1, 'Path class:  %s' % self.rf_path_class.__name__)
        dp(4, 1, 'Store class: %s' % self.rf_store_class.__name__)

        # Explore task graph.
        debug.down(2)
        store = self.rf_store_class(D)
        path_creator = lambda jlist: self.rf_path_class(jlist, max_horizon = D)
        ee = engine.ExplorationEngine(self, store, path_creator)
        ee.run()
        debug.up(2)
        dp(3, 1, 'Done exploring task graph after %.2f s. %d paths.' %
            (time.time() - timer, len(store.get_paths())))

        timer = time.time()
        dp(3, 1, "Filtering for maximal relevant paths...")
        maxpaths = set()
        add_to_maxpaths_rf(store.get_paths(), maxpaths, D)
        dp(3, 1, 'Done after %.2f s. %d paths left.' % (time.time() - timer,
            len(maxpaths)))

        for i, p in enumerate(maxpaths):
            p.name = "%s_D%d_p%d" % (self.name, D, i)

        self.rfpaths_cache[(D, None)] = maxpaths


    def prepare_rfdfpaths(self, D):
        """Compute request+demand functions up to D without abstractions."""
        timer = time.time()
        dp(3, 0, "Computing rfdf functions for task %s..." % self)
        dp(4, 1, 'D:           %d' % D)
        dp(4, 1, 'Path class:  %s' % self.rfdf_path_class.__name__)
        dp(4, 1, 'Store class: %s' % self.rfdf_store_class.__name__)

        # Explore task graph.
        debug.down(2)
        store = self.rfdf_store_class(D)
        path_creator = lambda jlist: self.rfdf_path_class(jlist, max_horizon = D)
        ee = engine.ExplorationEngine(self, store, path_creator)
        ee.run()
        debug.up(2)
        dp(3, 1, 'Done exploring task graph after %.2f s. %d paths.' %
            (time.time() - timer, len(store.get_paths())))

        timer = time.time()
        dp(3, 1, "Filtering for maximal relevant paths...")
        maxpaths = set()
        add_to_maxpaths_rfdf(store.get_paths(), maxpaths, D)
        dp(3, 1, 'Done after %.2f s. %d paths left.' % (time.time() - timer,
            len(maxpaths)))

        for i, p in enumerate(maxpaths):
            p.name = "%s_D%d_p%d" % (self.name, D, i)

        self.rfdfpaths_cache[(D, None)] = maxpaths


    def prepare_dfreversepaths(self, v, D):
        """Compute dfreverse functions for paths ending in v
        up to D without abstractions."""
        timer = time.time()
        dp(3, 0, "Computing dfreverse functions for task %s..." % self)
        dp(4, 1, 'D:           %d' % D)

        # Explore task graph.
        debug.down(2)
        store = path.dfreverse.DiscardingDfReverseStore(D)
        path_creator = lambda jlist: path.dfreverse.DfReversePath(jlist, max_horizon = D)
        ee = engine.ExplorationEngine(self, store, path_creator,
            start_jobs = [v], backwards = True)
        ee.run()
        debug.up(2)
        dp(3, 1, 'Done exploring task graph after %.2f s. %d paths.' %
            (time.time() - timer, len(store.get_paths())))

        timer = time.time()
        dp(3, 1, "Filtering for maximal relevant paths...")
        maxpaths = set()
        add_to_maxpaths_df(store.get_paths(), maxpaths, D)
        dp(3, 1, 'Done after %.2f s. %d paths left.' % (time.time() - timer,
            len(maxpaths)))

        for i, p in enumerate(maxpaths):
            p.name = "%s_D%d_p%d" % (self.name, D, i)

        self.dfreversepaths_cache[v][(D, None)] = maxpaths


    def get_rbf(self, t, incremental=1000):
        """Return the value rbf(<t>) for this Task.
        Always incremental. (See get_dbf for details.)

        Note: This is about time slots, i.e., rbf(0)>0.
        (In papers we usually define rbf(0)=0, i.e.,
            rbf_paper(t) = rbf_here(t-1).)
        """
        if self.rbf is None:
            dp(1, 0, 'Initialising incremental rbf computation for task %s...' % self)

            # Explore task graph.
            debug.down(2)
            # This expects a store without D
            store = path.rbf.DiscardingSortedRbfStoreNoD()
            ee = engine.IncrementalExplorationEngine(self, store,
                path.rbf.RequestTriple)
            eerunner = ee.run(incremental)
            debug.up(2)
            dp(2, 1, 'Init done.')

            self.rbf = []
            self._store = store
            self._eerunner = eerunner
        else:
            store = self._store
            eerunner = self._eerunner

        if len(self.rbf) <= t:

            timer = time.time()
            while store.current_limit < t:
                dp(2, 2, 'Incremental rbf computation for task %s from %d...' %
                    (self, store.current_limit))
                eerunner.next()
            dp(2, 1, 'Done exploring task graph after %.2f s.' %
                (time.time() - timer))

            # Generate dbf.
            (self.rbf, self.witnesses) = generate_rbf(store.get_paths(),
                store.current_limit)
            dp(1, 1, 'Done computing rbf after %.2f s.' % (time.time() - timer))

        # Now we know that self.dbf is defined at t
        return self.rbf[t]

    def get_dbf(self, t, incremental=None):
        """Return the value dbf(<t>) for this Task. (The dbf must have been
        computed first with prepare_dbf().)

        incremental: If not none, incremental computation of dbf.
            For more details, see is_feasible() method of TaskSet.
        """
        if incremental is None:
            if self.dbf is None:
                 raise RuntimeError('The dbf is not computed!')
        else:
            if self.dbf is None:
                dp(1, 0, 'Initialising incremental dbf computation for task %s...' % self)
                dp(2, 1, 'Path class:  %s' % self.dbf_path_class.__name__)
                dp(2, 1, 'Store class: %s' % self.dbf_store_class.__name__)

                # Explore task graph.
                debug.down(2)
                # This expects a store without D
                store = self.dbf_store_class()
                ee = engine.IncrementalExplorationEngine(self, store, self.dbf_path_class)
                eerunner = ee.run(incremental)
                debug.up(2)
                dp(2, 1, 'Init done.')

                self.dbf = []
                self._store = store
                self._eerunner = eerunner
            else:
                store = self._store
                eerunner = self._eerunner

            if len(self.dbf) <= t:

                timer = time.time()
                while store.current_limit < t:
                    dp(2, 2, 'Incremental dbf computation for task %s from %d...' %
                        (self, store.current_limit))
                    eerunner.next()
                dp(2, 1, 'Done exploring task graph after %.2f s.' %
                    (time.time() - timer))

                # Generate dbf.
                (self.dbf, self.witnesses) = generate_dbf(store.get_paths(),
                    store.current_limit)
                dp(1, 1, 'Done computing rbf after %.2f s.' % (time.time() - timer))

        # Now we know that self.dbf is defined at t
        return self.dbf[t]

    def get_utilization(self):
        """Return the utilization of this Task. (The utilization must have
        been computed first with prepare_utilization(). If this was not
        done before, do it right away.)"""
        if self.U is None:
#            raise RuntimeError('The utilization is not computed!')
            self.prepare_utilization()
        return self.U

    def prepare_dbf(self, D):
        """Compute the dbf for this Task up to the bound <D>."""
        timer = time.time()
        dp(1, 0, 'Computing dbf for task %s...' % self)
        dp(2, 1, 'D:           %d' % D)
        dp(2, 1, 'Path class:  %s' % self.dbf_path_class.__name__)
        dp(2, 1, 'Store class: %s' % self.dbf_store_class.__name__)

        # Explore task graph.
        debug.down(2)
        store = self.dbf_store_class(D)
        ee = engine.ExplorationEngine(self, store, self.dbf_path_class)
        ee.run()
        debug.up(2)
        dp(2, 1, 'Done exploring task graph after %.2f s.' %
            (time.time() - timer))

        # Generate dbf.
        (self.dbf, self.witnesses) = generate_dbf(store.get_paths(), D)

        dp(1, 1, 'Done computing dbf after %.2f s.' % (time.time() - timer))

    def prepare_utilization(self):
        """Compute the utilization of this Task."""
        timer = time.time()
        dp(1, 0, 'Computing utilization of task %s...' % self)
        dp(2, 1, 'Path class:  %s' % self.utilization_path_class.__name__)
        dp(2, 1, 'Store class: %s' % self.utilization_store_class.__name__)

        # Explore task graph.
        debug.down(2)
        store = self.utilization_store_class(len(self.jobs))
        ee = engine.ExplorationEngine(self, store, self.utilization_path_class)
        ee.run()
        debug.up(2)
        dp(2, 1, 'Done exploring task graph after %.2f s.' %
            (time.time() - timer))

        # Check cycles and compute U.
        dp(2, 1, 'Computing utilization from paths...')
        e2_max = 0 # Start with dummy cycle (U = 0).
        p_max = 1
        witness = None

        for path in store.get_paths():
            # Check only cycles.
            if path.get_start() == path.get_end() and len(path) > 0:
                e2 = path.get_e2()
                p = path.get_p()
                dp(4, 2, 'Found cycle %s with <%d, %d>.' % (path, e2, p))

                # Test if a new most dense cycle is found (avoid rounding).
                if e2 * p_max > e2_max * p:
                    e2_max = e2
                    p_max = p
                    witness = path
                    dp(4, 3, 'New candidate (U = %.5f): %s' %
                        (float(e2_max) / p_max, witness))

        dp(1, 1, 'Done computing utilization after %.2f s.' %
            (time.time() - timer))

        if witness is None:
            self.U = float(0)
            dp(1, 1, 'No cycle found! U = 0.')
        else:
            self.U = float(e2_max) / p_max
            dp(1, 1, 'U = %.5f via %s' % (self.U, witness))

    def __str__(self):
        return str(self.name)

    def render(self, filename, distance=10):

        import pygraphviz as pgv

        G = pgv.AGraph(directed=True, strict=False)
        for job in self.jobs:
            G.add_node(job.name, label=("%s <%d, %d>" % (job.name, job.get_e(), job.get_d())))
        for job in self.jobs:
            for succ in job.succs.keys():
                G.add_edge(job.name, succ.name, label=job.succs[succ], len=distance)
        G.layout(prog="neato")
        G.draw(filename)

    def pretty_print(self):
        for j in self.jobs:
            print "%s with e=%d d=%d" % (j.name, j.get_e(), j.get_d())
            for s in j.succs:
                print "  edge to %s with p=%d" % (s.name, j.succs[s])

    def lowest_priority_feasible(self, hp_tasks, critical_jobs=None, dbg=False,
            force_solver=None):
        """Returns True iff task can have priority lower than taskset.
        """

        if len(hp_tasks) == 0:
            dp(0, 0, "Trivially LP feasible.")
            return True

        debug.down(1)
        if critical_jobs is None:
            critical_jobs = set(self.jobs)

        jobs_to_test = set(self.jobs).intersection(critical_jobs)
        jobs_not_to_test = set(self.jobs).difference(critical_jobs)
        dp(0, 0, "Jobs to test: %s" % ", ".join([str(j) for j in jobs_to_test]))
        dp(0, 0, "Jobs skipped: %s" % ", ".join([str(j) for j in jobs_not_to_test]))

        # This is in case jobs_to_test is empty
        res = False

        for j in jobs_to_test:
            dp(0, 0, "Checking job '%s'..." % j.name)
            res = TaskSet(hp_tasks).interference_test(j.E, j.D, dbg,
                force_solver=force_solver)
            if res:
                dp(0, 1, "Job is NOT lowest-priority feasible.")
                break
            else:
                dp(0, 1, "Job is lowest-priority feasible.")
        debug.up(1)

        global xx_stats_jobs_tested
        xx_stats_jobs_tested += 1
        return not res


class TaskSet(object):

    def __init__(self, tasks=[]):
        self.tasks = tasks
        self.max_busy_period = None

    def reset(self):
        for task in self.tasks:
            task.reset()
        self.max_busy_period = None

    def get_utilization(self):
        return sum([task.get_utilization() for task in self.tasks])


    def get_max_busy_period(self):
        """ Returns upper bound on busy window size, based on
            incremental rbf computation."""

        if self.max_busy_period is None:
            start_time = time.time()
            dp(0, 0, 'Computing maximal busy window size (upper bound)...')

            t = 1
            while True:
                rbfts = [task.get_rbf(t-1) for task in self.tasks]
                rbft = sum(rbfts)
                dp(2, 2, "Computed rbf(%d)=%d." % (t, rbft))
                if (rbft <= t):
                    dp(0, 2, 'Done.')
                    dp(1, 2, 'rbf(%d) = %d' % (t, rbft))
                    dp(2, 3, '= sum(%s)' % (rbfts))
                    break
                else:
                    dp(3, 2, 'rbf(%d) = %d' % (t, rbft))
                    dp(4, 3, '= sum(%s)' % (rbfts))
                    t = rbft

            dp(0, 0, "Busy window size computed within %.2f s." % (time.time() -
                start_time))

            self.max_busy_period = t
        else:
            dp(2, 0, 'Using cached maximal busy window size (upper bound)...')

        return self.max_busy_period


    def is_feasible(self, autosave = False, incremental = 1000, force_store=True):
        """ incremental: If not None, an interval length for which
            the dbf will be computed incrementally, i.e.,
            incremental steps at a time.
            Based on the observation that counterexamples are found
            usually for quite small t, i.e., not the full domain [0, D]
            is necessary for that.

            force_store: If True (default), then set dbf_store to
              DiscardingSortedDbfStore if incremental is None,
              DiscardingSortedDbfStoreNoD otherwise."""
        start_time = time.time()
        dp(0, 0, 'Checking feasibility of task set...')

        dp(0, 1, 'Computing utilization of task set...')
        U = 0
        e_sum = 0
        debug.down(2)
        for task in self.tasks:
            task.prepare_utilization()
            U += task.get_utilization()
            e_sum += task.get_e_sum()
        debug.up(2)

        dp(0, 2, 'Done computing utilization of task set after %.2f s.' %
            (time.time() - start_time))
        dp(0, 2, "Task set's utilization:     %.5f" % U)

        if U >= 1:
            feasible = False
        else:
            D = int(e_sum / (1 - U))
            dp(0, 2, "Task set's total execution: %d" % e_sum)
            dp(0, 2, "Bound (D): %d" % D)

            if incremental is None:
                dp(0, 1, 'Computing dbf of task set...')
                debug.down(2)
                for task in self.tasks:
                    if force_store:
                        task.set_dbf_store_abstraction(
                            path.discardingstores.DiscardingSortedDbfStore)
                    task.prepare_dbf(D)
                debug.up(2)
                dp(0, 2, 'Done computing dbf for task set.')
            else:
                if force_store:
                    for task in self.tasks:
                        task.set_dbf_store_abstraction(
                            path.discardingstores.DiscardingSortedDbfStoreNoD)

            feasible = True
            for t in xrange(D + 1):
                dbfts = [task.get_dbf(t, incremental) for task in self.tasks]
                dbft = sum(dbfts)
                if (dbft > t) and feasible:
                    dp(0, 2, '*** COUNTEREXAMPLE! ***')
                    dp(1, 2, 'dbf(%d) = %d' % (t, dbft))
                    dp(2, 3, '= sum(%s)' % (dbfts))
                    feasible = False
                    break
                else:
                    dp(3, 2, 'dbf(%d) = %d' % (t, dbft))
                    dp(4, 3, '= sum(%s)' % (dbfts))

        if feasible:
            dp(0, 1, ':-) Task set is feasible!')
        else:
            dp(0, 1, ':-( Task set is not feasible!')

        dp(0, 0, "Feasibility test completed after %.2f s." % (time.time() -
            start_time))

        if autosave:
            self.save_to_file('autosave.pickle')
            dp(0, 0, 'TaskSet autosaved.')

        return feasible

    ##modify_rlease_delay {{{1
    def modify_rlease_delay(self, level = 0, given_order=False):
        """RF/IF shaping: @level = 0(safe), 1(extreme), 2(fortune)
        :returns: @todo

        """

        ret_flag = True
        slvl = int(level / 3)
        level = level%3

        mod_bounds={}
        ts_cjs={}
        min_dx = 1000000 ## [Robin] infinity
        #for t in reversed(self.tasks):
        ces = [max([j.get_e() for j in tt.get_jobs()]) for tt in self.tasks]
        cds = [min([j.get_d() for j in tt.get_jobs()]) for tt in self.tasks]

        ##[Robin] Beginning of calculating adjusting bound {{{2
        for idx in reversed(range(len(self.tasks))):
            t = self.tasks[idx]
            tbs = {}
            cjs = []
            for j in t.get_jobs():
                tbs[j]=0

            if given_order and t == self.tasks[0]:
                for j in t.get_jobs():
                    tbs[j] = j.get_mindelay() - j.get_e()
                mod_bounds[t]=tbs
                ts_cjs[t]=cjs
                continue

            js = sorted(t.get_jobs(),key=lambda x:x.get_e(),reverse=True)

            if not given_order:
                ce = sum(ces)
                cd = min(cds)
            else:
                ce = sum(ces[:idx+1])
                cd = min(cds[:idx+1])
            #print ce,cd,min_dx
            #ce = 10
            #cd = 0
            if ce > cd or cd > min_dx:
                cd = min_dx
                #print '======'
            else:
                ce = cd
                #print '### unreachable zone for OPA ###'
            ce = ces[idx]
            cd = max(ce,min_dx)

            if ce > min_dx:
                ret_flag = False
                if level < 0:
                    return ret_flag
            #print '==',ce,cd

            for j in js:
                tbs[j] = 0
                if j.get_d() >= cd:
                    tbs[j] = (j.get_d()-j.get_e()) - (cd - ce)
                elif j.get_d() - j.get_e() > cd - ce:
                    tbs[j] = (j.get_d() - j.get_e()) - (cd - ce)
                else:
                    cd = j.get_d()
                    ce = j.get_e()
                    cjs = [j] + cjs
            ## [Robin] //TODO need more


            from math import ceil, floor
            js.sort(key=lambda x: x.get_d()-tbs[x])

            #dummy = True
            #dummy = False
            global gg_dummy
            dummy = gg_dummy
            for (i,j) in enumerate(js):
                if dummy or level < 0:
                    break
                _jd = j.get_d() - tbs[j]
                _je = j.get_e()

                if _jd == 0:
                    print j.get_e(), j.get_d(), ce, cd, tbs[j], j.succs
                    print 'xxxxxxxxxxxxxxxxxxxxxxx'

                #print j.get_d(), j.get_e()
                #for (ii, jj) in enumerate(js):
                for jj in js[i+1:]:
                    _me = int(ceil(jj.get_e()*1.0/_je))
                    _md = int(floor(jj.get_d()/_jd))
                    #print _me, _md
                    if _me <= _md:
                        tbs[jj] = max(tbs[jj], jj.get_d() - _jd * _me + (_je*_me-jj.get_e()))
                        #print '2222222222222222222222222222222222222222'

            for (i,j) in enumerate(cjs):
                if not dummy:
                    break
                for (ii, jj) in enumerate(cjs):
                    if ii>i and int(ceil(jj.get_e()*1.0/j.get_e())) <= int(floor(jj.get_d()/j.get_d())):
                        del cjs[ii]
                        #print '111111111111111111111111111111'
                        tbs[jj] = jj.get_d() - j.get_d() * int(ceil(jj.get_e()*1.0/j.get_e()))

            if given_order:
                min_dx = min ([j.get_d() - tbs[j] -j.get_e() for j in js] + [min_dx])

            cjs = [j for j in cjs if tbs[j]==0]
            for j in cjs:
                del tbs[j]

            mod_bounds[t] = tbs
            ts_cjs[t] = cjs

        ## [Robin] end of calcualting adusting bound ~ }}}2
        for t in self.tasks:
            for j in mod_bounds[t] :
                j.D -= mod_bounds[t][j]
                if j.D < j.get_d():
                    raise '33333333333333333333333333'
        ############################

        mod_bck = {} ## [Robin] could be removed ~
        for t in mod_bounds:
            mod_bck[t]={}
            for j in mod_bounds[t]:
                mod_bck[t][j] = mod_bounds[t][j]

        ## BEGIN: Adjusting release dealy for all tasks {{{2
        for (i,t) in enumerate(self.tasks):
            if given_order:
                try:
                    mlen = max([(max([0]+[j.get_d() for j in ts_cjs[tt]])) for tt in self.tasks[i:] if tt!= t])
                    minlen = min ([(min([0]+[j.get_d() for j in ts_cjs[tt]])) for tt in self.tasks[i:] if tt!= t])

                except:
                    break
            else:
                mlen = max([(max([0]+[j.get_d() for j in ts_cjs[tt]])) for tt in self.tasks if tt != t])
                minlen = min([(min([0]+[j.get_d() for j in ts_cjs[tt]])) for tt in self.tasks if tt != t])

            if slvl > 0:
                mlen = int(minlen + (mlen - minlen)*0.618) ## [Robin] Golden Ratio
                #mlen = int((mlen + minlen)*0.618)


            ## [Robin] Adjust vetex by check succesives {{{3
            loop = True
            while loop:
                skiped = {}
                loop = False
                for j in mod_bounds[t]:
                    if skiped.has_key(j):
                        continue
                    skiped[j] = None
                    if mod_bounds[t][j] <= 0:
                        continue
                    m =  -1

                    for nj in j.succs:
                        #if nj == j : continue ## [Robin] must all of the j-started paths!!!
                        mm = 0
                        for pj in nj.get_prevs():
                            if pj == j:
                                continue
                            if j.succs[nj] >= pj.succs[nj] and j.get_e() <= pj.get_e(): ##//TODO need more, according the description in manuscript
                                skiped[pj]=None
                                delta = (pj.get_e() -j.get_e() + j.succs[nj]-pj.succs[nj])
                                if j != nj:
                                    delta = int (floor(delta/2.0))
                                mm = max (mm, delta)
                                #if pj.succs[nj]+nj.get_mindelay()>=mlen:
                                    #mm = max(mm, (pj.get_e() + min(nj.get_e(), mlen - pj.succs[nj])
                                        #) - (j.get_e() + min(nj.get_e(), mlen - j.succs[nj]))       )
                                #else:
                                    #mm=max(mm,j.succs[nj] - pj.succs[nj]) ## [Robin] //TODO need more
                            elif j.succs[nj] > pj.succs[nj] and j.succs[nj] + j.get_e()>mlen and (level > 0):
                                oo = j.get_e() + nj.get_e() - (j.succs[nj]+nj.get_e()-mlen)
                                cpm = pj.get_e() + min(nj.get_e(), mlen - pj.succs[nj])
                                if ( cpm >= oo) :
                                    skiped[pj]=None
                                    mm = max(mm, cpm-oo)
                            ## [Robin]  //TODO
                        if m == -1:
                            m = mm
                        else:
                            if level < 2:
                                m = min((m,mm))
                            else:
                                m = max(m,mm)
                        if mm<=0 and level < 2:
                            break
                    if level < 3:
                        m = min(m, mod_bounds[t][j])
                    else :
                        m= min(m, max(mod_bounds[t][j],(j.get_d() -j.get_e()*gg_min_swm)))
                    if  m > 0:
                        mod_bounds[t][j] -= m
                        loop = True
                        dp(0,1,'m=%d'%(m),6)
                        for nj in j.succs:
                            if nj != j:
                                j.succs[nj]-=int(m)
                                pass
                        j.get_mindelay(True)
                        for pj in j.get_prevs():
                            if pj != j:
                                pj.succs[j] += int(m)
                                pj.get_mindelay(True)
                    else:
                        #dp(0,1,'xxxxxx',6)
                        pass
            #END of Adjusting succesives }}}3

            ## [Robin] Adjust vetex by check previous vetex {{{3
            #loop = True
            #while loop:
                #loop = False
                skiped = {}
                for j in mod_bounds[t]:
                    if skiped.has_key(j):
                        continue
                    skiped[j] = None
                    if mod_bounds[t][j] <= 0:
                        continue

                    flag = True
                    for nj in j.succs:
                        if j.succs[nj] + nj.get_mindelay() <= mlen:
                            flag = False
                            break
                    if not flag : continue

                    m =  -1

                    for pj in j.get_prevs():
                        if pj == j : continue
                        mm = None
                        for nj in j.succs:
                            if nj == j:
                                #continue
                                pass
                            if pj.get_e() >= j.get_e():
                                if pj.get_e() >= nj.get_e():
                                    sl = j.succs[nj] - pj.succs[j] + (pj.get_e()+j.get_e())
                                    #sr = mlen - (j.succs[nj]+nj.get_mindelay()) + (pj.get_e() - nj.get_e())
                                    sr =  (j.succs[nj]+nj.get_mindelay()) + (pj.get_e() - nj.get_e()) - mlen
                                else:
                                    sl = j.succs[nj] - pj.succs[j] + (pj.get_e()+j.get_e())
                                    sr = (j.succs[nj]+pj.get_e() - mlen)

                                #slack = int(min(sl,sr).618)
                                #slack = int(min(sl,sr)*0.5)
                                #slack = int(min(sl,sr))
                                if j == nj:
                                    pass
                                elif level > 0:
                                    sl = int(sl *0.618)
                                else:
                                    sl = int(sl * 0.5)
                                slack = int(min(sl,sr))
                                if mm is None:
                                    mm = slack
                                else:
                                    if level < 1 or sl < 0:
                                        mm = min (mm, slack)
                                    else:
                                        mm = max (mm, slack)
                            elif (level > 0):
                                ## [Robin]  //TODO need more work
                                pl = pj.get_e()+min(mlen-pj.succs[j],j.get_e())
                                jl = j.get_e() + max(0,mlen-j.get_mindelay())
                                if pl > jl:
                                    delta = min(pl-jl,j.get_mindelay()-pj.succs[j]-(j.get_e()-pj.get_e()))
                                    if mm == -1:
                                        mm = delta
                                    else:
                                        if(level < 2):
                                            mm = min (mm, delta)
                                        else:
                                            mm = max(mm, delta)
                                pass
                            else :
                                mm = None
                                break
                        m = max((m,mm if mm is not None else -1))
                    ## [Robin] end FOR

                    if level < 3:
                        m = min(m, mod_bounds[t][j])
                    else :
                        m= min(m, max(mod_bounds[t][j],j.get_d() - j.get_e()*gg_min_swm))
                    if  m > 0:
                        mod_bounds[t][j] -= m
                        loop = True
                        dp(0,1,'m=%d'%(m),6)
                        for nj in j.succs:
                            if nj != j:
                                j.succs[nj]-=int(m)
                                pass
                        j.get_mindelay(True)
                        for pj in j.get_prevs():
                            if pj != j:
                                pj.succs[j] += int(m)
                                pj.get_mindelay(True)
                    else:
                        #dp(0,1,'xxxxxx',6)
                        pass
            ## end adjust previos
                if gg_loop_once:
                    loop = False

        ## END of Adusting Release Delay }}}2

        for t in self.tasks:
            for j in mod_bounds[t] :
                #j.D -= (mod_bck[t][j] - mod_bounds[t][j])
                j.D +=  mod_bounds[t][j]
            pass


        dp(0,1,'modify_rlease_delay',group=6)
        #print self.tasks
        #print 'modify_release_delay'
        return ret_flag
    ## Modify_rlease_delay }}}1


    def is_fp_feasible(self, cj_optimization=True, dbg=False,
            force_solver=None, autosave=False,
            ## [Robin] Add new switch parameter priode
            given_order=None
            ):
        """ Checks for static priority feasibility of task set via
        Audsley's Algorithm. Returns True or False.

        Note: Limited to constrained deadlines.
        """
        #
        # Performance:
        # * Create a bunch of random tasks:
        #   # for i in range(100): tasks.append(examples.RandomTask(1,5, 1,3, 20,100, 1,3, 20,100, name="T%d"%i))
        # * FP feasibility test takes about a minute for 10-14 tasks.
        #   # task.TaskSet(tasks[:12]).is_fp_feasible()

        if not all([t.constrained for t in self.tasks]):
            dp(0, 0, "Error: Not a constrained deadlines task set.")
            return None

        start_time = time.time()
        dp(0, 0, "Checking FP feasibility of task set ...")

        debug.down(1)
        # Initiall, assume all jobs to be critical
        res = self.get_fp_order(cj_optimization=cj_optimization, dbg=dbg,
            force_solver=force_solver,given_order=given_order)
        debug.up(1)

        if res is not False:
            dp(0, 1, ":-) Task set is fp feasible!")
            dp(0, 0, "Priority order: '%s'" %
                "', '".join([t.name for t in res]))
            feasible = True
        else:
            dp(0, 1, ":-( Task set is not fp feasible!")
            feasible = False

        dp(0, 0, "Feasibility test completed after %.2f s." % (time.time() -
            start_time))

        if autosave:
            self.save_to_file('autosave.pickle')
            dp(0, 0, 'TaskSet autosaved.')

        return feasible


    def fake_run_prepare_rfpaths(self, cj=None, cj_optimization=True, dbg=False,
            force_solver=None):
        """ Checks for static priority feasibility of task set via
        Audsley's Algorithm. Returns either False or the priority order
        as a list which is permutation of self.tasks.

        Note: Limited to constrained deadlines.
        """

        global xx_stats_jobs_ncj

        start_time = time.time()
        dp(0, 0, "Creating rfpaths for task set %s." % [t.name for t in self.tasks])

        if cj is None:

            # Optimization: Test only critical jobs
            #  - intra task: j1 >= j2 if j1.e >= j2.e and j1.d <= j2.d
            #  - inter task: T1.j1 >= T2.j2 if j1 >= j2 and T1 >= T2 (i.e. T1 lower prio)
            if cj_optimization:
                dp(0, 1, "Building initial critical_jobs set.")

                # Critical jobs in all already processed tasks
                cj = set()
                for (i, t) in enumerate(self.tasks):
                    # Critical jobs in current task
                    cj_task = set()

                    for job in t.jobs:
                        # Remove from cj_task all jobs that we dominate
                        cj_task.difference_update([j
                            for j in cj_task if job.dominates(j, strict=True)])
                        # Add ourselves to cj_task if we are not dominated
                        # by anything in cj_task
                        if all([not j.dominates(job, strict=True) for j in cj_task]):
                            cj_task.add(job)
                    cj = cj.union(cj_task)

                all_jobs = [j for t in self.tasks for j in t.jobs]
                dp(0, 2, "%d of %d (%.2f%%) jobs are intra-task critical." %
                    (len(cj), len(all_jobs), float(len(cj)*100)/len(all_jobs)))
                dp(0, 2, "Critical jobs: %s" % [str(j) for j in cj])
                xx_stats_jobs_ncj += len(all_jobs) - len(cj)
            else:
                cj = set([j for T in self.tasks for j in T.jobs])

            D = max([j.get_d() for j in cj])
            dp(1, 1, "Upper bound for scheduling window size: D=%d" % D)
            if force_solver in [None, 'rbf', 'rf', 'rf_iterative']:
                dp(1, 1, "Preparing request functions.")
                debug.down(2)
                for task in self.tasks:
                    # Use get_rfpaths() instead of prepare_rfpaths() since
                    # this may save work if we are running interactively
                    # with the same task set
                    task.get_rfpaths(D)
                debug.up(2)

        dp(0, 0, "Done after %.2f s." % (time.time() - start_time))

        return True


    def get_fp_order(self, cj=None, cj_optimization=True, dbg=False,
            force_solver=None,
            ## [Robin] check given priorities order
            given_order=None):
        """ Checks for static priority feasibility of task set via
        Audsley's Algorithm. Returns either False or the priority order
        as a list which is permutation of self.tasks.

        Note: Limited to constrained deadlines.
        """

        global xx_stats_jobs_ncj

        dp(0, 0, "Determining priority order for task set %s." % [t.name for t in self.tasks])

        if cj is None:

            # Optimization: Test only critical jobs
            #  - intra task: j1 >= j2 if j1.e >= j2.e and j1.d <= j2.d
            #  - inter task: T1.j1 >= T2.j2 if j1 >= j2 and T1 >= T2 (i.e. T1 lower prio)
            if cj_optimization:
                dp(0, 1, "Building initial critical_jobs set.")

                # Critical jobs in all already processed tasks
                cj = set()
                for (i, t) in enumerate(self.tasks):
                    # Critical jobs in current task
                    cj_task = set()

                    for job in t.jobs:
                        # Remove from cj_task all jobs that we dominate
                        cj_task.difference_update([j
                            for j in cj_task if job.dominates(j, strict=True)])
                        # Add ourselves to cj_task if we are not dominated
                        # by anything in cj_task
                        if all([not j.dominates(job, strict=True) for j in cj_task]):
                            cj_task.add(job)
                    cj = cj.union(cj_task)

                all_jobs = [j for t in self.tasks for j in t.jobs]
                dp(0, 2, "%d of %d (%.2f%%) jobs are intra-task critical." %
                    (len(cj), len(all_jobs), float(len(cj)*100)/len(all_jobs)))
                dp(0, 2, "Critical jobs: %s" % [str(j) for j in cj])
                xx_stats_jobs_ncj += len(all_jobs) - len(cj)
            else:
                cj = set([j for T in self.tasks for j in T.jobs])

            D = max([j.get_d() for j in cj])
            dp(1, 1, "Upper bound for scheduling window size: D=%d" % D)
            if force_solver in [None, 'rbf', 'rf', 'rf_iterative']:
                dp(1, 1, "Preparing request functions.")
                debug.down(2)
                for task in self.tasks:
                    # Use get_rfpaths() instead of prepare_rfpaths() since
                    # this may save work if we are running interactively
                    # with the same task set
                    task.get_rfpaths(D)
                debug.up(2)


        debug.down(1)
        lp_task = None
        for i in reversed(range(len(self.tasks))):
            lp_task = self.tasks[i]
            hp_tasks = self.tasks[:i] + self.tasks[i+1:]
            dp(0, 0, "Checking lowest-priority feasibility of task '%s'." % lp_task.name)

            dp(0, 1, "Interfering tasks: '%s'" %
                "', '".join([t.name for t in hp_tasks]))

            res = lp_task.lowest_priority_feasible(hp_tasks=hp_tasks,
                critical_jobs=cj, dbg=dbg, force_solver=force_solver)
            if res:
                dp(0, 1, "Task is lp-feasible.")

                if cj_optimization:
                    # Update cj set, more jobs could be inter-task non-critical.
                    new_ncj = set()
                    for job in lp_task.jobs:
                        new_ncj_job = [j
                            for j in cj.intersection([j for t in hp_tasks for j in t.jobs])
                            if job.dominates(j, strict=True)]
                        dp(0, 2, "New non-critical jobs from '%s': '%s'" % (str(job),
                            "', '".join([str(j) for j in new_ncj_job])))
                        new_ncj.update(new_ncj_job)
                    old_cj = cj.copy()
                    cj.difference_update(new_ncj)
                    xx_stats_jobs_ncj += len(new_ncj)
                    dp(0, 2, "Now, we have %d critical jobs left. (Before: %d)" %
                        (len(cj), len(old_cj)))

                break
            else:
                dp(0, 1, "Task can't have this priority.")
                # [Robin] add
                if given_order:
                    dp(0, 1, "Due to given_order, TS is UNSCHED~~~")
                    break
                ## [Robin]  add-end
        debug.up(1)

        if not res:
            dp(0, 0, "No task can have lowest priority. Infeasible.")
            return False
        else:
            dp(0, 0, "Found LP task '%s'.\n" % lp_task)
            if len(hp_tasks) > 0:
                res = TaskSet(hp_tasks).get_fp_order(cj, cj_optimization, dbg=dbg, given_order=given_order)
            else:
                res = []
                if cj_optimization:
                    dp(0, 0, "Done. %d jobs were critical." % len(cj))
                else:
                    dp(0, 0, "Done.")
            if res is False:
                return False
            else:
                prio_order = res + [lp_task]
                return prio_order


    def is_fp_schedulable(self, dbg=False, cj_optimization=True, desc_prio=True,
            force_solver=None, autosave=False):
        """ Checks for static priority schedulability of task set.
        Assumes that the tasks were given in priority order at object
        creation time. Lower indices in list == higher priority.

        Note: Limited to constrained deadlines.
        """

        global xx_stats_jobs_ncj

        if not all([t.constrained for t in self.tasks]):
            dp(0, 0, "Error: Not a constrained deadlines task set.")
            return None

        start_time = time.time()
        dp(0, 0, "Checking FP schedulability of task set...")

        schedulable = True

        # Optimization: Test only critical jobs
        #  - intra task: j1 >= j2 if j1.e >= j2.e and j1.d <= j2.d
        #  - inter task: T1.j1 >= T2.j2 if j1 >= j2 and T1 >= T2 (i.e. T1 lower prio)
        if cj_optimization:
            dp(0, 1, "Building critical_jobs set.")

            # Critical jobs in all already processed tasks
            cj = set()
            for (i, t) in enumerate(self.tasks):
                # Critical jobs in current task
                cj_task = set()

                for job in t.jobs:
                    # Remove from cj all jobs that we dominate
                    cj.difference_update([j
                        for j in cj if job.dominates(j, strict=True)])
                    # Remove from cj_task all jobs that we dominate
                    cj_task.difference_update([j
                        for j in cj_task if job.dominates(j, strict=True)])
                    # Add ourselves to cj_task if we are not dominated
                    # by anything in cj_task
                    if all([not j.dominates(job, strict=True) for j in cj_task]):
                        cj_task.add(job)
                cj = cj.union(cj_task)

            # Non-critical jobs
            ncj = set()
            ncj_reasons = dict()
            ncj_intra = dict()
            for i in range(len(self.tasks)):
                t = self.tasks[i]
                for j in t.jobs:
                    if j not in cj:
                        ncj.add(j)
                        intra_task_dominators = cj.intersection(t.jobs)
                        inter_task_dominators = cj.intersection([j2
                            for t2 in self.tasks[i+1:] for j2 in t2.jobs])
                        ncj_reasons[j] = list(intra_task_dominators) + \
                            list(inter_task_dominators)
                        ncj_intra[j] = (len(intra_task_dominators) > 0)

            all_jobs = [j for t in self.tasks for j in t.jobs]
            dp(0, 2, "%d of %d (%3.2f%%) jobs are critical." %
                (len(cj), len(all_jobs), float(len(cj)*100)/len(all_jobs)))
            dp(0, 2, "Of %d non-critical jobs, %d are intra-task dominated." %
                (len(ncj), len([j for j in ncj_intra if ncj_intra[j]])))
            dp(0, 2, "Critical jobs: %s" % [str(j) for j in cj])
            dp(0, 2, "Non-critical jobs:")
            for j in ncj:
#                dp(0, 3, "%s, dominated by %s" %
#                    (str(j), ", ".join(ncj_reasons[j])))
                dp(0, 3, "%s, dominated by at least %s." %
                    (str(j), str(ncj_reasons[j][0])))
            xx_stats_jobs_ncj += len(ncj)

        else:
            cj = set([j for T in self.tasks for j in T.jobs])

        D = max([j.get_d() for j in cj])
        if force_solver in [None, 'rbf', 'rf', 'rf_iterative']:
            dp(1, 1, "Upper bound for scheduling window size: D=%d" % D)
            dp(1, 1, "Preparing request functions.")
            debug.down(2)
            for task in self.tasks:
                # Use get_rfpaths() instead of prepare_rfpaths() since
                # this may save work if we are running interactively
                # with the same task set
                task.get_rfpaths(D)
            debug.up(2)

        debug.down(1)
        idx_list = range(len(self.tasks))
        if desc_prio:
            # TODO: Does this really make a difference? Do some testing...
            idx_list = reversed(idx_list)
        for i in idx_list:
            checktask = self.tasks[i]
            dp(0, 0, "Checking lowest-priority feasibility of task '%s'." %
                checktask.name)

            dp(0, 1, "Interfering tasks: '%s'" %
                "', '".join([self.tasks[j].name for j in range(i)]))

            res = checktask.lowest_priority_feasible(hp_tasks=self.tasks[:i],
                critical_jobs=cj, dbg=dbg, force_solver=force_solver)
            if res:
                dp(0, 0, "Task ok.")
            else:
                dp(0, 0, "Task can't have this priority.")
                break
        debug.up(1)
        if res:
            dp(0, 1, ":-) Task set schedulable with this priority order!")
        else:
            dp(0, 1, ":-( Task set unschedulable with this priority order!")

        dp(0, 0, "Schedulability test completed after %.2f s." % (time.time() -
            start_time))

        if autosave:
            self.save_to_file('autosave.pickle')
            dp(0, 0, 'TaskSet autosaved.')

        return res


    def rta_edf(self, force_solver=None, autosave=False, skipx_optimization=True):
        """ Response-Time Analysis for EDF scheduling of task set.

        Returns a dict with {vertex: rt}.
        rt is None if deadline miss.

        force_solver: treeroots or refinement

        Note: Limited to constrained deadlines.
        """

        if not all([t.constrained for t in self.tasks]):
            dp(0, 0, "Error: Not a constrained deadlines task set.")
            return None

        start_time = time.time()
        dp(0, 0, "Response-Time Analysis for EDF...")

        alljobs = set([j for T in self.tasks for j in T.jobs])

        debug.down(2)
        maxL = self.get_max_busy_period()
        debug.up(2)
        dp(1, 1, "Upper bound for busy window size: D=%d" % maxL)

        maxD = max([j.get_d() for j in alljobs])
        dp(1, 1, "Upper bound for scheduling window size: D=%d" % maxD)


        dp(1, 1, "Preparing rfdf functions for gamma=%d." % (maxL+maxD+1))
        debug.down(2)
        for task in self.tasks:
            dp(2, 2, "Task '%s'." % (str(task)))
            # Use get_rfpaths() instead of prepare_rfpaths() since
            # this may save work if we are running interactively
            # with the same task set
            task.get_rfdfpaths(maxL+maxD+1)
        debug.up(2)

        response_times = dict()

        for job in alljobs:

            dp(0, 0, "Computing RTs of job '%s' in task '%s'." %
                (str(job), str(job.get_task())))

            debug.down(2)
            rt = self.get_edfrt(job, force_solver=force_solver,
                skipx_optimization=skipx_optimization)
            debug.up(2)
            dp(2, 2, "Saving RT='%s'." % str(rt))
            response_times[job] = rt

        dp(0, 0, "RTA completed after %.2f s." % (time.time() -
            start_time))

        if autosave:
            self.save_to_file('autosave.pickle')
            dp(0, 0, 'TaskSet autosaved.')

        return response_times


    def get_edfrt(self, v, force_solver = None, skipx_optimization = True):
        """ Returns EDF response time of v in this task set.
        False if response time larger than d(v)
        """

        solver = force_solver or "refinement"

        if solver == "treeroots":
            return self.get_edfrt_treeroots(v, skipx_optimization=skipx_optimization)
        elif solver == "refinement":
            return self.get_edfrt_refinement(v, skipx_optimization=skipx_optimization)
        else:
            raise RuntimeError("Unsupported edfrt solver: %s" %
                str(solver))

    def get_edfrt_treeroots(self, v, skipx_optimization = True):

        def compute_rt(wbftuple, L, D):
            # Return either RT or d+1 in case RT > d

            global xx_stats_skipx_skipped
            global xx_stats_skipx_notskipped

            dbf = [sum([f.get_df()[t] for f in wbftuple]) for t in range(L+D+1)]

            idle_instant = None
            for x in range(L + 1):
                if skipx_optimization:
                    maxdemand = dbf[x + D]
                    if maxdemand - x < idle_instant:
                        dp(5, 2, "Skipping x=%d since dbf(%d+%d)=%d." %
                            (x, x, D, maxdemand))
                        xx_stats_skipx_skipped += 1
                        continue
                    else:
#                        dp(5, 2, "dbf(%d+%d) = %d." %
#                            (x, D, maxdemand))
                        xx_stats_skipx_notskipped += 1
                t = 1
                while (t <= D) and (idle_instant < D + 1):
                    dp(5, 2, "Checking workload at x=%d, t=%d, D=%d..." % (x, t, D))
                    workload = sum([f.eval_wbf(x+t, x+D) for f in wbftuple])
                    dp(5, 3, "%d (%s)" % (workload, str([f.eval_wbf(x+t, x+D) for f in wbftuple])))
                    if workload <= x + t:
                        dp(5, 3, "Idle. t=%d" % t)
                        idle_instant = max(idle_instant, t)
                        break
                    elif workload > x+D:
                        # This is already a deadline violation
                        dp(5, 3, "Deadline miss. workload = %d" % workload)
                        idle_instant = D+1
                        break
                    else:
                        t = workload - x
            return (D+1) if idle_instant is None else idle_instant

        dp(2, 0, "Computing response time for vertex '%s'..." % str(v))
        timer = time.time()

        debug.down(1)
        L = self.get_max_busy_period()
        delta = L + v.get_d()
        dp(2, 0, "Maximal busy period is %d." % L)
        debug.up(1)

        rfdfs = list()
        for task in self.tasks:
            if not v in task.jobs:
                rfdfs.extend(list(task.get_rfdfpaths(delta+1, abstraction_level=0)))
        (own_df,) = v.get_task().get_dfreversepaths(v, delta+1, abstraction_level=0)

        idle_instant = compute_rt(rfdfs + [own_df], L, v.get_d())

        dp(2, 0, "Done with %d (d=%d) after %.2fs." % (idle_instant, v.get_d(),
            (time.time() - timer)))

        return None if idle_instant > v.get_d() else idle_instant


    def get_edfrt_refinement(self, v, skipx_optimization = True):

        def compute_rt(wbftuple, L, D):
            # Return either RT or d+1 in case RT > d

            global xx_stats_skipx_skipped
            global xx_stats_skipx_notskipped

            dbf = [sum([f.get_df()[t] for f in wbftuple]) for t in range(L+D+1)]

            idle_instant = None
            for x in range(L + 1):
                if skipx_optimization:
                    maxdemand = dbf[x + D]
                    if maxdemand - x < idle_instant:
                        dp(5, 2, "Skipping x=%d since dbf(%d+%d)=%d." %
                            (x, x, D, maxdemand))
                        xx_stats_skipx_skipped += 1
                        continue
                    else:
#                        dp(5, 2, "dbf(%d+%d) = %d." %
#                            (x, D, maxdemand))
                        xx_stats_skipx_notskipped += 1
                t = 1
                while (t <= D) and (idle_instant < D + 1):
                    dp(5, 2, "Checking workload at x=%d, t=%d, D=%d..." % (x, t, D))
                    workload = sum([f.eval_wbf(x+t, x+D) for f in wbftuple])
                    dp(5, 3, "%d (%s)" % (workload, str([f.eval_wbf(x+t, x+D) for f in wbftuple])))
                    if workload <= x + t:
                        dp(5, 3, "Idle. t=%d" % t)
                        idle_instant = max(idle_instant, t)
                        break
                    elif workload > x+D:
                        # This is already a deadline violation
                        dp(5, 3, "Deadline miss. workload = %d" % workload)
                        idle_instant = D+1
                        break
                    else:
                        t = workload - x
            return (D+1) if idle_instant is None else idle_instant


        dp(2, 0, "Computing response time for vertex '%s'..." % str(v))
        D = v.get_d()
        timer = time.time()

        debug.down(1)
        L = self.get_max_busy_period()
        delta = L + v.get_d()
        dp(2, 0, "Maximal busy period is %d." % L)
        debug.up(1)

        # Get all leaves
        rfdfs_concrete = list()
        for task in self.tasks:
            if not v in task.jobs:
                rfdfs_concrete.append(task.get_rfdfpaths(delta+1, abstraction_level=None).copy())
        own_df_concrete = v.get_task().get_dfreversepaths(v, delta+1, abstraction_level=None).copy()

        stats_total = reduce(lambda x,y:x*y, [len(paths)
            for paths in (rfdfs_concrete + [own_df_concrete])])

        # Get all roots
        rfdfs = list()
        for task in self.tasks:
            if not v in task.jobs:
                rfdfs.extend(task.get_rfdfpaths(delta+1, abstraction_level=1).copy())
        (own_df,) = v.get_task().get_dfreversepaths(v, delta+1, abstraction_level=1).copy()
        stats_tested = 0

        # Needs to be a list() since we want to start manipulating it
        # when refining.
        start_tuple = rfdfs + [own_df]

#        idle_instant = compute_rt(paths, L, v.get_d())

        # This will be our store for todo tuples. We use heapq which
        # is a priority queue maintaining the SMALLEST element in position 0.
        # Thus, save triles (-rt, i, tuple) in the queue where i is just
        # an ever decreasing counter to make heap comparisons
        # work even if rt is the same (otherwise it starts comparing
        # tuples, i.e., request functions, which will just end badly
        # since we overleaded comparison operators which are not always
        # defined).
        todo = [(-compute_rt(start_tuple, L, D), 0, start_tuple)]
        stats_tested += 1

        initial_rt = -todo[0][0]

        while True:
            (maxrt, _, ptuple) = heapq.heappop(todo)
            maxrt = -maxrt

            dp(4, 1, "Current maximum with RT %d is %s." % (maxrt,
                ', '.join([p.name for p in ptuple])))

            # Check whether rftuple is abstract
            is_abstract = any([len(path.jobs) == 0 for path in ptuple])

            if is_abstract:
                # Need to do more work: Push concretization of some abstract path
                dp(4, 3, "This combination was abstract. Pushing concretization.")
                # Find task to split
                (max_spread, min_pos, min_path) = max([(path.spread, i, path)
                    for (i, path) in enumerate(ptuple) if len(path.jobs) == 0])
                dp(5, 4, "Splitting path %s with spread %.5f." %
                    (min_path.name, max_spread))
                for path in min_path.childs:
                    new_ptuple = ptuple[:]
                    new_ptuple[min_pos] = path
                    rt = compute_rt(new_ptuple, L, D)
                    dp(5, 4, "Pushing combination [%s] with RT=%d" % (
                        ', '.join([p.name for p in new_ptuple]), rt))
                    heapq.heappush(todo, (-rt, -stats_tested, new_ptuple))
                    stats_tested += 1
                    if stats_tested % 10000 == 0:
                        dp(2, 5, "Tested %d/%d combinations." %
                            (stats_tested, stats_total))
                        dp(2, 6, "Configuration details: %s" %
                            str([len(paths) for paths in (rfdfs_concrete + [own_df_concrete])]))
                        dp(2, 6, "Current max/Initial RT: %d/%d" % (maxrt, initial_rt))

            else:
                # Done: Found actual response time.
                dp(4, 3, "This combination was concrete. We are done.")
                break

        dp(2, 0, "Done with %d (d=%d) after %.2fs." % (maxrt, v.get_d(),
            (time.time() - timer)))

        global xx_stats_combinations_tested
        xx_stats_combinations_tested += stats_tested

        global xx_stats_rt_total
        xx_stats_rt_total += 1
        global xx_stats_rt_improved
        if maxrt < initial_rt:
            dp(2, 1, "IMPROVEMENT: RT was improved from %d to %d." %
                (initial_rt, maxrt))
            xx_stats_rt_improved += 1
            xx_stats_rt_improvements.append((initial_rt, maxrt))

        global xx_stats_combi
        if len(xx_stats_combi) < xx_stats_combi_MAXLEN:
            xx_stats_combi.append( ("EDF-RT", maxrt < initial_rt, stats_tested, stats_total) )

        return None if maxrt > D else maxrt



    def rta_fp(self, dbg=False, force_solver=None, dj_optimization=True,
            autosave=False):
        """ Response-Time Analysis for static priority scheduling of task set.
        Assumes that the tasks were given in priority order at object
        creation time. Lower indices in list == higher priority.

        Returns a dict with {vertex: rt}.

        force_solver: rbf or rf_iterative
        dj_optimization: After computing RT for a job, use this as a new upper
            bound for RT of all dominated jobs. This can decrease the domain
            of their request functions and lead to smaller abstraction trees.

        Note: Limited to constrained deadlines.
        """

        global xx_stats_jobs_ncj

        if not all([t.constrained for t in self.tasks]):
            dp(0, 0, "Error: Not a constrained deadlines task set.")
            return None

        start_time = time.time()
        dp(0, 0, "Response-Time Analysis for static priorities...")

        alljobs = set([j for T in self.tasks for j in T.jobs])

        D = max([j.get_d() for j in alljobs])
        dp(1, 1, "Upper bound for scheduling window size: D=%d" % D)
        dp(1, 1, "Preparing request functions.")
        debug.down(2)
        for task in self.tasks:
            # Use get_rfpaths() instead of prepare_rfpaths() since
            # this may save work if we are running interactively
            # with the same task set
            task.get_rfpaths(D)
        debug.up(2)

        debug.down(1)
        idx_list = range(len(self.tasks))
        response_times = dict()
        rt_bounds = dict([(job, job.get_d()) for t in self.tasks
            for job in t.jobs])
        for i in reversed(idx_list):
            checktask = self.tasks[i]
            dp(0, 0, "Computing RTs of task '%s'." % checktask.name)

            dp(0, 1, "Interfering tasks: '%s'" %
                "', '".join([self.tasks[j].name for j in range(i)]))

            for job in checktask.jobs:
                rt = TaskSet(self.tasks[:i]).get_fprt(job.get_e(),
                    rt_bounds[job], debug=dbg, force_solver=force_solver)
                dp(2, 2, "Job '%s' has RT=%s." % (job.name, str(rt)))
                if dj_optimization:
                    # Find all dominated jobs of higher priority
                    for task in self.tasks[:i]:
                        for j in task.jobs:
                            if job.dominates(j, strict=False):
                                if rt is not None and rt < rt_bounds[j]:
                                    dp(2, 3, "Reducing RT bound of job '%s' from %d to %d." % (j.name, rt_bounds[j], rt))
                                    rt_bounds[j] = rt
                response_times[job] = rt

        debug.up(1)

        dp(0, 0, "RTA completed after %.2f s." % (time.time() -
            start_time))

        if autosave:
            self.save_to_file('autosave.pickle')
            dp(0, 0, 'TaskSet autosaved.')

        return response_times


    def get_fprt(self, c, d, debug=False, force_solver=None):
        """Returns response time via RTA.
        False if response time larger than d.
        """

        if c == 0:
            return 0

        solver = force_solver or xx_default_solver

        if len(self.tasks) == 0:
            return c

        if solver == 'rbf':
            return self.get_fprt_rbf(c, d, debug)
        elif solver == 'rf_iterative':
            return self.get_fprt_rf_iterative(c, d, debug)
        else:
            raise RuntimeError("Unsupported fprt solver: %s" %
                str(solver))


    def get_fprt_rbf(self, c, d, dbg=False, subset=None):
        """Request bound funtion based RTA.
        Overapproximate, i.e., returned value is possibly larger than
        actual response time. Very fast though.
        """

        if subset is None:
            subset = self.tasks

        # Dict with key = task and value = set of rfpaths
        rfpaths = dict([(task, task.get_rfpaths(d, abstraction_level=0).copy())
            for task in subset])

        for task in subset:
            dp(3, 0, "Path for task '%s':" % task.name)
            # There is just one path, so replace singleton set with object itself
            rfpaths[task] = rfpaths[task].pop()
            dp(3, 1, "%s: %s" % (rfpaths[task].name, str(rfpaths[task])))

        dp(2, 0, "Testing combination of rbfs.")
        timer = time.time()
        rftuple = rfpaths.values()

        rfs = [p.get_rf() for p in rftuple]
        idle_instant = None
        t = 1
        while t <= d:
            dp(5, 2, "Checking workload at t=%d..." % t)
            # Use rf[t-1] here since that's how rf is stored:
            # rf(t) = rf[t-1]
            workload = sum([rf[t - 1] for rf in rfs]) + c
            if workload <= t:
                idle_instant = t
                break
            else:
                t = workload
        if idle_instant is not None:
            dp(4, 2, "Found idle instant at t=%d." % t)
        else:
            dp(4, 2, "Found no idle instant.")

        dp(2, 0, "Done with %s after %.2fs." %
            ("SCHED" if idle_instant else "UNSCHED", (time.time() - timer)))

        global xx_stats_combinations_tested
        xx_stats_combinations_tested += 1

        return idle_instant


    def get_fprt_rf_iterative(self, c, d, dbg=False, subset=None):
        """RTA using incremental precision, i.e., combinatorial abstraction
        refinement. Starts with rbf test and refines abstractions iteratively
        until definitive (and precise) conclusion.

        Specifically, refines abstraction of currently highest RT bound,
        until a leaf combination has highest RT bound.
        """

        def compute_rt(rftuple, c, d):
            # Do the actual RT computation.
            # Return either RT or d+1 in case RT > d
            dp(4, 1, "Testing combination [%s]" %
                ', '.join([p.name for p in rftuple]))

            rfs = [p.get_rf() for p in rftuple]
            idle_instant = None
            t = 1
            while t <= d:
                dp(5, 2, "Checking workload at t=%d..." % t)
                workload = sum([rf[t-1] for rf in rfs]) + c
                if workload <= t:
                    idle_instant = t
                    break
                else:
                    t = workload
            return (d+1) if idle_instant is None else idle_instant


        if subset is None:
            subset = self.tasks

        # Dict with key = task and value = set of rfpaths
        rfpaths_concrete = dict([(task, task.get_rfpaths(d, abstraction_level=None).copy())
            for task in subset])
        rfpaths = dict([(task, task.get_rfpaths(d, abstraction_level=1).copy())
            for task in subset])

        for task in subset:
            dp(3, 0, "Paths for task '%s':" % task.name)
            for rfpath in rfpaths[task]:
                dp(3, 1, "%s: %s" % (rfpath.name, str(rfpath)))

        stats_total = reduce(lambda x,y:x*y, [len(paths)
            for paths in rfpaths_concrete.values()])
        stats_tested = 0

        start_tuple = [s.pop() for s in rfpaths.values()]

        # This will be our store for todo tuples. We use heapq which
        # is a priority queue maintaining the SMALLEST element in position 0.
        # Thus, save triles (-rt, i, tuple) in the queue where i is just
        # an ever decreasing counter to make heap comparisons
        # work even if rt is the same (otherwise it starts comparing
        # tuples, i.e., request functions, which will just end badly
        # since we overleaded comparison operators which are not always
        # defined).
        todo = [(-compute_rt(start_tuple, c, d), 0, start_tuple)]
        stats_tested += 1

        initial_rt = -todo[0][0]

        timer = time.time()
        while True:
            (maxrt, _, rftuple) = heapq.heappop(todo)
            maxrt = -maxrt

            dp(4, 1, "Current maximum with RT %d is %s." % (maxrt,
                ', '.join([p.name for p in rftuple])))

            # Check whether rftuple is abstract
            is_abstract = any([len(rfpath.jobs) == 0 for rfpath in rftuple])

            if is_abstract:
                # Need to do more work: Push concretization of some abstract path
                dp(4, 3, "This combination was abstract. Pushing concretization.")
                # Find task to split
                (max_spread, min_pos, min_rfpath) = max([(rfpath.spread, i, rfpath)
                    for (i, rfpath) in enumerate(rftuple) if len(rfpath.jobs) == 0])
                dp(5, 4, "Splitting path %s with spread %.5f." %
                    (min_rfpath.name, max_spread))
                for rfpath in min_rfpath.childs:
                    new_rftuple = rftuple[:]
                    new_rftuple[min_pos] = rfpath
                    rt = compute_rt(new_rftuple, c, d)
                    dp(5, 4, "Pushing combination [%s] with RT=%d" % (
                        ', '.join([p.name for p in new_rftuple]), rt))
                    heapq.heappush(todo, (-rt, -stats_tested, new_rftuple))
                    stats_tested += 1
                    if stats_tested % 10000 == 0:
                        dp(2, 5, "Tested %d/%d combinations." %
                            (stats_tested, stats_total))
                        dp(2, 6, "Configuration details: %s" %
                            str([len(paths) for paths in rfpaths_concrete.values()]))
                        dp(2, 6, "Current max/Initial RT: %d/%d" % (maxrt, initial_rt))

                    if stats_tested % 100000 == 0:
                        dp(2, 5, "This is taking very long. Saving.")
                        global xx_save_long_time_fprt
                        xx_save_long_time_fprt = (subset, c, d)
            else:
                # Done: Found actual response time.
                dp(4, 3, "This combination was concrete. We are done.")
                break

        dp(2, 0, "Done with %d after %.2fs. Summary:" %
            (maxrt, (time.time() - timer)))
        dp(2, 1, "Combinations tested / total: %d / %d (%.1f%%)" %
            (stats_tested, stats_total, float(stats_tested*100)/stats_total))

        global xx_stats_combinations_tested
        xx_stats_combinations_tested += stats_tested

        global xx_stats_rt_total
        xx_stats_rt_total += 1
        global xx_stats_rt_improved
        if maxrt < initial_rt:
            dp(2, 1, "IMPROVEMENT: RT was improved from %d to %d." %
                (initial_rt, maxrt))
            xx_stats_rt_improved += 1
            xx_stats_rt_improvements.append((initial_rt, maxrt))

        global xx_stats_combi
        if len(xx_stats_combi) < xx_stats_combi_MAXLEN:
            xx_stats_combi.append( ("FP-RT", maxrt < initial_rt, stats_tested, stats_total) )

        return None if maxrt > d else maxrt


    def interference_test(self, c, d, debug=False, subset=None,
            force_solver=None):

        solver = force_solver or xx_default_solver

        if solver == 'smt':
            return self.interference_test_smt(c, d, debug, subset)
        elif solver == 'sat':
            return self.interference_test_sat(c, d, debug, subset)
        elif solver == 'rf': ## [Robin] no abstractions, just path dominaations
            return self.interference_test_rf(c, d, debug, subset)
        elif solver == 'rbf': ## [Robin] Top level Abstractions, FAST, Approximate
            return self.interference_test_rbf(c, d, debug, subset)
        elif solver == 'rf_iterative': ## [Robin] RTSS13, Refinement
            return self.interference_test_rf_iterative(c, d, debug, subset)
        else:
            raise RuntimeError("Unsupported interference solver: %s" %
                str(solver))


    def interference_test_rf_iterative(self, c, d, dbg=False, subset=None):
        """Implementation with incremental precision, i.e., iterative abstraction
        refinement. Starts with rbf test and refines abstractions iteratively
        until definitive (and precise) conclusion.

        State of the art. (2013-04-29)
        """

        if subset is None:
            subset = self.tasks

        # Dict with key = task and value = set of rfpaths
        rfpaths_concrete = dict([(task, task.get_rfpaths(d, abstraction_level=None).copy())
            for task in subset])
        rfpaths = dict([(task, task.get_rfpaths(d, abstraction_level=1).copy())
            for task in subset])

        for task in subset:
            dp(3, 0, "Paths for task '%s':" % task.name)
            for rfpath in rfpaths[task]:
                dp(3, 1, "%s: %s" % (rfpath.name, str(rfpath)))

        start_tuple = [s.pop() for s in rfpaths.values()]
        todo = [start_tuple]

        stats_total = reduce(lambda x,y:x*y, [len(paths)
            for paths in rfpaths_concrete.values()])
        stats_tested = 0
        stats_pos = 0
        stats_neg = 0
        timer = time.time()

        while len(todo) > 0:
            rftuple = todo.pop()
            dp(4, 1, "Testing combination [%s]" %
                ', '.join([p.name for p in rftuple]))

            rfs = [p.get_rf() for p in rftuple]
            idle_instant = None
            t = 0
            while t < d:
                dp(5, 2, "Checking workload at t=%d..." % t)
                workload = sum([rf[t] for rf in rfs]) + c
                if workload <= t + 1:
                    idle_instant = t
                    break
                else:
                    t = workload - 1
            stats_tested += 1

            if idle_instant is not None:
                dp(4, 2, "Found idle instant at t=%d." % t)
                stats_pos += 1
            else:
                dp(4, 2, "Found no idle instant.")
                stats_neg += 1

                # Check whether rftuple is abstract
                is_abstract = any([len(rfpath.jobs) == 0 for rfpath in rftuple])

                if is_abstract:
                    # Need to do more work: Push concretization of some abstract path
                    dp(4, 3, "This combination was abstract. Pushing concretization.")
                    (max_spread, min_pos, min_rfpath) = max([(rfpath.spread, i, rfpath)
                        for (i, rfpath) in enumerate(rftuple) if len(rfpath.jobs) == 0])
                    dp(5, 4, "Splitting path %s with spread %.5f." %
                        (min_rfpath.name, max_spread))
                    for rfpath in min_rfpath.childs:
                        new_rftuple = rftuple[:]
                        new_rftuple[min_pos] = rfpath
                        dp(5, 4, "Pushing combination [%s]" %
                            ', '.join([p.name for p in new_rftuple]))
                        todo.append(new_rftuple)
                else:
                    # Done: Found deadline miss.
                    dp(4, 3, "This combination was concrete. We are done.")
                    break

        dp(2, 0, "Done with %s after %.2fs. Summary:" %
            ("SCHED" if idle_instant else "UNSCHED", (time.time() - timer)))
        dp(2, 1, "Combinations tested / total: %d / %d (%.1f%%)" %
            (stats_tested, stats_total, float(stats_tested*100)/stats_total))

        global xx_stats_combinations_tested
        global xx_stats_al_nonzero_schedulable
        xx_stats_combinations_tested += stats_tested
        if idle_instant and stats_tested > 1:
            xx_stats_al_nonzero_schedulable += 1

        global xx_stats_combi
        if len(xx_stats_combi) < xx_stats_combi_MAXLEN:
            xx_stats_combi.append( (idle_instant is None,
		stats_tested, stats_total, stats_pos, stats_neg) )

        return idle_instant is None


    def interference_test_rbf(self, c, d, dbg=False, subset=None):

        """Request bound funtion based interference test.
        Sound but incomplete, i.e., return value "False" (SCHED) is accurate
        while return value "True" (UNSCHED) is overapproximate.
        Very fast though.
        """

        if subset is None:
            subset = self.tasks

        # Dict with key = task and value = set of rfpaths
        rfpaths = dict([(task, task.get_rfpaths(d, abstraction_level=0).copy())
            for task in subset])

        for task in subset:
            dp(3, 0, "Path for task '%s':" % task.name)
            # There is just one path, so replace singleton set with object itself
            rfpaths[task] = rfpaths[task].pop()
            dp(3, 1, "%s: %s" % (rfpaths[task].name, str(rfpaths[task])))

        dp(2, 0, "Testing combination of rbfs.")
        timer = time.time()
        rftuple = rfpaths.values()

        rfs = [p.get_rf() for p in rftuple]
        idle_instant = None
        t = 0
        while t < d:
            dp(5, 2, "Checking workload at t=%d..." % t)
            workload = sum([rf[t] for rf in rfs]) + c
            if workload <= t + 1:
                idle_instant = t
                break
            else:
                t = workload - 1
        if idle_instant is not None:
            dp(4, 2, "Found idle instant at t=%d." % t)
        else:
            dp(4, 2, "Found no idle instant.")

        dp(2, 0, "Done with %s after %.2fs." %
            ("SCHED" if idle_instant else "UNSCHED", (time.time() - timer)))

        global xx_stats_combinations_tested
        xx_stats_combinations_tested += 1

        return idle_instant is None


    def interference_test_rf(self, c, d, dbg=False, subset=None):
        """Original (non-iterative) request funtion based interference test.
        Implements use of prefix inclusion constraints.
        Tests first rbf combination for speed up of negative instances.
        Superceded by incremental rf based test which refines this step.
        """

        # Make sure to call prepare_rfpaths with maximum D beforehand.
        # (This is for efficiency reasons. Otherwise, they will be recreated
        # which is potentially costly.)

        global xx_stats_al_testcounts
        global xx_stats_al_nonzero_schedulable

        for abstraction_level in xx_abstraction_levels:
            dp(3, 0, "Testing interference with abstraction level %s." %
                str(abstraction_level))
            xx_stats_al_testcounts[abstraction_level] += 1
            debug.down(1)
            res = self.interference_test_rf_abstraction(c, d, dbg=dbg,
                subset=subset, abstraction_level=abstraction_level)
            debug.up(1)
            if res:
                if abstraction_level is None:
                    dp(3, 0, "Deadline miss found.")
                    break
                else:
                    dp(3, 0, "Inconclusive. Safe assumption: Deadline miss.")
            else:
                dp(3, 0, "No deadline miss found.")
                if abstraction_level != 0:
                    xx_stats_al_nonzero_schedulable += 1

        return res

    def interference_test_rf_abstraction(self, c, d, dbg=False, subset=None,
            abstraction_level=None):

        ec_threshold = xx_ec_threshold
        ec_maxsize = xx_ec_maxsize

        if subset is None:
            subset = self.tasks

        # Dict with key = task and value = set of rfpaths
        rfpaths = dict([(task, task.get_rfpaths(d, abstraction_level).copy())
            for task in subset])

        # Dict with key = (path, position) and value = set of dominated rfpaths
        dom = dict()
        for task in subset:
            dom.update(task.get_dominance_sets(d, abstraction_level))

        for task in subset:
            dp(3, 0, "Paths for task '%s':" % task.name)
            for rfpath in rfpaths[task]:
                dp(3, 1, "%s: %s" % (rfpath.name, str(rfpath)))

        stats_total = reduce(lambda x,y:x*y, [len(paths)
            for paths in rfpaths.values()])
        stats_tested = 0
        stats_skipped = 0
        dp(2, 0, "Starting %d combination tests in abstraction level %s." %
            (stats_total, abstraction_level))
        timer = time.time()
        exclusion_constraints = list()
        for rftuple in itertools.product(*rfpaths.values()):
            # Check if we are included in some exclusion constraint
            skip = False
            for ec in exclusion_constraints:
                if ec.issuperset(rftuple):
                    skip = True
                    break
            if skip:
                # yes we are
                dp(4, 1, "Skipping combination [%s]" %
                    ', '.join([p.name for p in rftuple]))
                stats_skipped += 1
                continue
            # No we are not. Let's get going.

            dp(4, 1, "Testing combination [%s]" %
                ', '.join([p.name for p in rftuple]))
            rfs = [p.get_rf() for p in rftuple]
            idle_instant = None
            t = 0
            while t < d:
                dp(5, 2, "Checking workload at t=%d..." % t)
                workload = sum([rf[t] for rf in rfs]) + c
                if workload <= t + 1:
                    idle_instant = t
                    break
                else:
                    t = workload - 1
            stats_tested += 1
            if idle_instant is not None:
                dp(4, 2, "Found idle instant at t=%d." % t)
                ec = set()
                for p in rftuple:
                    ec.update(dom[(p, idle_instant)])
                ec_minsize = len(subset) + ec_threshold
                if len(ec) < ec_minsize:
                    dp(5, 2, "Exclusion constraint too small (size: %d, minimum: %d)" %
                        (len(ec), ec_minsize))
                else:
                    dp(5, 2, "Adding exclusion constraint: [%s]" %
                        ", ".join([p.name for p in ec]))
                    exclusion_constraints.append(ec)
                    if len(exclusion_constraints) > ec_maxsize:
                        exclusion_constraints.pop(0)
            else:
                dp(4, 2, "Found no idle instant.")
                break
        dp(2, 0, "Done with %s after %.2fs. Summary:" %
            ("SCHED" if idle_instant else "UNSCHED", (time.time() - timer)))
        dp(2, 1, "Combinations tested / skipped / total: %d (%.1f) / %d (%.1f) / %d" %
            (stats_tested, float(stats_tested*100)/stats_total,
            stats_skipped, float(stats_skipped*100)/stats_total,
            stats_total))
        dp(2, 1, "Created %d exclusion constraints." % len(exclusion_constraints))

        global xx_stats_combinations_tested
        global xx_stats_combinations_skipped
        xx_stats_combinations_tested += stats_tested
        xx_stats_combinations_skipped += stats_skipped

        return idle_instant is None



    def interference_test_smt(self, c, d, debug=False, subset=None):

        # TODO: Check for unique vertex names

        def vstr(t, v):
            return "%s_%s" % (t.name, v.name)

        def estr(t, v1, v2):
            return "E_%s_%s_%s" % (t.name, v1.name, v2.name)

        # Boilerplate
        smtfile = """(set-logic DRTFPS)
(set-info :smt-lib-version 2.0)
"""

        if debug:
            smtfile += "(set-option :verbosity 3)\n"
        else:
            smtfile += "(set-option :verbosity 0)\n"

        smtfile += """
(declare-sort Task 0)
(declare-sort Vertex 0)
(declare-sort Edge 0)
(declare-fun interference (Real Real) Bool)
(declare-fun vdata (Vertex Real Task) Bool)
(declare-fun edata (Edge Vertex Vertex Real) Bool)
(declare-fun start (Vertex) Bool)
(declare-fun step (Real Edge) Bool)
"""

        if subset is None:
            subset = self.tasks

        # Symbol declarations
        for T in subset:
            smtfile += "(declare-fun %s () Task)\n" % T.name
            for j in T.jobs:
                smtfile += "(declare-fun %s () Vertex)\n" % vstr(T, j)
                for j2 in j.succs:
                    smtfile += "(declare-fun %s () Edge)\n" % estr(T, j, j2)

        # Interference data
        smtfile += "(assert (interference %d %d))\n" % (c, d)

        # Vertex and Edge data
        for T in subset:
            for j in T.jobs:
                smtfile += "(assert (vdata %s %d %s))\n" % (vstr(T, j), j.E, T.name)
                for j2 in j.succs:
                    smtfile += "(assert (edata %s %s %s %d))\n" % (estr(T, j, j2),
                        vstr(T, j), vstr(T, j2), j.succs[j2])

        # Constraints: Starts unique
        for T in subset:
            startvars = [bf.BF_variable("start %s" % vstr(T, j)) for j in T.jobs]
            f = bf.BF_exactly(1, startvars).simplify()
            smtfile += "(assert%s)\n" % f.to_smt2_str()

        # Constraints: Steps unique
        #TODO: Find maximum step count more exactly
        for T in subset:
            edges = [(estr(T, j, j2), j.succs[j2]) for j in T.jobs for j2 in j.succs]
            maxsteps = (d-1) / min([e[1] for e in edges])

            for step in range(1, maxsteps+1):
                stepvars = [bf.BF_variable("step %d %s" % (step, edge[0])) for edge
                    in edges]
                f = bf.BF_exactly(1, stepvars).simplify()
                smtfile += "(assert%s)\n" % f.to_smt2_str()

        # Constraints: Starts connected
        for T in subset:
            for j in T.jobs:
                A = bf.BF_variable("start %s" % vstr(T, j))
                B = bf.BF_or([bf.BF_variable("step %d %s" % (1, estr(T, j, j2))) for
                    j2 in j.succs])
                f = bf.BF_or([bf.BF_not(A), B])
                smtfile += "(assert%s)\n" % f.to_smt2_str()

        # Constraints: Steps connected
        for T in subset:
            edges = [(estr(T, j, j2), j.succs[j2]) for j in T.jobs for j2 in j.succs]
            maxsteps = (d-1) / min([e[1] for e in edges])
            for step in range(1, maxsteps):
                for j in T.jobs:
                    for j2 in j.succs:
                        A = bf.BF_variable("step %d %s" % (step, estr(T, j, j2)))
                        B = bf.BF_or([bf.BF_variable("step %d %s" % (step+1,
                            estr(T, j2, j3))) for j3 in j2.succs])
                        f = bf.BF_or([bf.BF_not(A), B])
                        smtfile += "(assert%s)\n" % f.to_smt2_str()

        # Ending
        smtfile += "(check-sat)\n(exit)"

        opensmt_infile = "/tmp/opensmt-in.smt2"
        with open(opensmt_infile, "w") as f:
            f.write(smtfile)

        r = subprocess.call(["opensmt/opensmt/build/opensmt", opensmt_infile])
        if r == 0:
            return True
        elif r == 1:
            return False
        else:
            print "Odd return value of OpenSMT: %d" % r
        return False


    def interference_test_sat(self, c, d, debug=False, guess='unsat', subset=None):
        """Returns True iff the task set can cause strictly more than d-c
        accumulated time units of interference in a consecutive window
        of length d.

        Thus, True means: interpreting the task set as higher-priority tasks,
        an additional lower priority job with WCET c and relative deadline d
        would potentially miss its deadline, therefore not being schedulable.
        False means the opposite, i.e., a positive (partial) schedulability
        test for this particular (partial) priority order.

        Parameter debug gives a debug return tuple
           (var_x, var_rel, var_inst, var_exec, C, f, m)
        with all variables, the constraint dict C, the final formula f in CNF
        and the satisfying assignment m in case f was satisfiable.

        Parameter guess indicates whether we assume that this test will succeed
        (guess=='sat') or fail (guess=='unsat'). The latter is the default
        and leads to additional constraints being generated which aids the
        UNSAT proof but would potentially make search for a satisfying
        assignment slower.
        """

        # TODO: Implement Optimizations, e.g.
        #        * Limit irange to d [done]
        #        * Even irange*min(jrange) to d (sound?)
        #        * Instead of checking ALL low-prio jobs, do partial-order optimization
        #        * Reduce symmetries for faster UNSAT proof:
        #          - First job released at 0, first job runs at 0 [done]
        #          - Release jobs in order [done]
        #          - Execute job pieces in order [done]
        #        * TODO: more?

        # Compute maximal values
        trange = range(d)
        # Use d-1 in the following since we are concerned with actually
        # occupied time slots, compared to just releases that get_max_releases
        # computes.
        irange = range(min(sum([t.get_max_releases(d-1) for t in self.tasks]),
                           d))
        jrange = range(max([j.get_e() for t in self.tasks for j in t.get_jobs()]))
        # Let's hope the job types are disjoint. Otherwise: TROUBLE AHEAD.
        jtrange = [j for t in self.tasks for j in t.get_jobs()]

#        print len(trange), len(irange), len(jrange), len(jtrange)

        # Create variables

        var_x = dict([((i, j, t), bf.BF_variable("x(%d,%d,%d)" % (i, j, t)))
            for t in trange for j in jrange for i in irange])
        dp(2, 3, "var_x contains %d elements." % len(var_x))

        var_rel = dict([((i, t), bf.BF_variable("rel(%d,%d)" % (i, t)))
            for t in trange for i in irange])
        dp(2, 3, "var_rel contains %d elements." % len(var_rel))

        var_inst = dict([((i, jt), bf.BF_variable("inst(%d,%s)" % (i, jt)))
            for jt in jtrange for i in irange])
        dp(2, 3, "var_inst contains %d elements." % len(var_inst))

        var_exec = dict([(t, bf.BF_variable("exec(%d)" % t)) for t in trange])
        dp(2, 3, "var_exec contains %d elements." % len(var_exec))

        dp(2, 2, "Created %d boolean variables." % (len(var_x) + len(var_rel) +
            len(var_inst) + len(var_exec)))

        # Create constraints

        def countdagnodes(formula):
            return formula.dagapply(lambda o, r: r+1, startval=0)

        C = dict()

        C["x_wellformed"] = [bf.BF_atmost_CNF(1, [var_x[(i, j, t)] for t in trange])
            for i in irange for j in jrange]

        C["inst_wellformed"] = [bf.BF_exactly_CNF(1, [var_inst[(i, jt)] for jt in
            jtrange]) for i in irange]

        C["rel"] = [bf.BF_or([bf.BF_not(var_rel[(i1, t1)]),
                           bf.BF_not(var_rel[(i2, t2)]),
                           bf.BF_not(var_inst[(i1, jt1)]),
                           bf.BF_not(var_inst[(i2, jt2)])])
                 for i1 in irange
                 for i2 in irange
                 for jt1 in jtrange
                 for jt2 in jtrange
                 for t1 in trange
                 for t2 in trange
                 if i1 != i2
                 if t1 <= t2
                 if jt1.get_task() == jt2.get_task()
                 if not jt1.get_task().reachable(jt1, jt2, t2-t1)]

#        if debug:
#            for i in range(100, 300):
#                dp(2, 4, "Example: %s" % C["rel"][i])

        C["exec"] = [bf.BF_and(bf.BF_pattern3(bf.BF_not(var_exec[t]),
            [bf.BF_not(var_x[(i, j, t)]) for i in irange for j in jrange]))
            for t in trange]

        C["consistency_rel_x"] = [bf.BF_or([bf.BF_not(var_x[(i, j, t)])] +
            [var_rel[(i, t2)] for t2 in trange if t2 <= t])
            for i in irange for j in jrange for t in trange]

        C["consistency_pieces"] = [bf.BF_or([bf.BF_not(var_inst[(i, jt)]),
                                             bf.BF_not(var_x[(i, j, t)])])
                for i in irange
                for j in jrange
                for jt in jtrange
                for t in trange
                if j >= jt.get_e()]

        C["busy"] = [bf.BF_atmost(c-1, [bf.BF_not(var_exec[t]) for t in trange])]

        if guess == 'unsat':

            C["initially_busy"] = [var_exec[0], var_x[(0, 0, 0)],
                var_rel[(0, 0)]]

            C["in_order_rel"] = [bf.BF_or([bf.BF_not(var_rel[(i1, t1)]),
                                           bf.BF_not(var_rel[(i2, t2)])])
                    for i1 in irange
                    for i2 in irange
                    for t1 in trange
                    for t2 in trange
                    if i1 < i2
                    if t1 > t2]

            C["in_order_pieces"] = [bf.BF_or([bf.BF_not(var_x[(i, j1, t1)]),
                                              bf.BF_not(var_x[(i, j2, t2)])])
                    for i in irange
                    for j1 in jrange
                    for j2 in jrange
                    for t1 in trange
                    for t2 in trange
                    if j1 < j2
                    if t1 > t2]

        for n in C.keys():
            dp(2, 3, "%s contains %d dag nodes for %d constraints." %
                (n, countdagnodes(bf.BF_and(C[n])), len(C[n])))

        # Test satisfiability

        f = bf.BF_and([c for cset in C.values() for c in cset]).CNF()

        res = f.is_satisfiable()

        if debug:
            return (var_x, var_rel, var_inst, var_exec, C, f,
                f.get_satmap() if res else None)
        else:
            return res


    def set_abstraction(self, abstraction):
        """Set path and store abstractions for all tasks. The <abstraction>
        must be a module providing DbfPath, DbfStore, UtilizationPath and
        UtilizationStore.
        """
        for task in self.tasks:
            task.set_dbf_path_abstraction(abstraction.DbfPath)
            task.set_dbf_store_abstraction(abstraction.DbfStore)
            task.set_utilization_path_abstraction(abstraction.UtilizationPath)
            task.set_utilization_store_abstraction(abstraction.UtilizationStore)

    def set_abstraction_by_name(self, abstraction):
        if abstraction == 'fullpath':
            self.set_abstraction(path.fullpath)
        elif abstraction == 'fullpathdiscard':
            self.set_abstraction(path.fullpathdiscard)
        elif abstraction == 'triple':
            self.set_abstraction(path.triple)
        elif abstraction == 'quadruple':
            self.set_abstraction(path.quadruple)
        else:
            raise RuntimeError('Invalid abstraction type.')

    def save_to_file(self, filename):
        try:
            fd = open(filename, 'w')
            cPickle.dump(self, fd, cPickle.HIGHEST_PROTOCOL)
        except Exception:
            print('Could not save task set to %s!' % filename)
        finally:
            fd.close()


def add_to_maxpaths_rf(paths, maxpaths, D):
    for path in paths:

        dp(3, 2, "Processing: %s" % path)

        # Check whether too short
        if path.get_horizon() < D:
            dp(4, 3, "Too short.")
            continue

        # Check whether we are dominated by some processed path
        dominated = False
        new_rf = path.get_rf()
        for p in maxpaths:
            rf = p.get_rf()
            dominated = all([rf[i] >= new_rf[i] for i in range(D)])
            if dominated:
                dp(4, 3, "Dominated by %s." % p)
                break
        if dominated:
            continue
        dp(4, 3, "New. Will add.")

        # Remove all paths dominated by us
        remove_paths = set()
        for p in maxpaths:
            rf = p.get_rf()
            dominated = all([rf[i] <= new_rf[i] for i in range(D)])
            if dominated:
                dp(4, 4, "Dominates: %s" % p)
                remove_paths.add(p)
        maxpaths.difference_update(remove_paths)

        # Done. Add finally.
        maxpaths.add(path)


def add_to_maxpaths_df(paths, maxpaths, D):
    for path in paths:

        dp(3, 2, "Processing: %s" % path)

        # Check whether too short
        if path.get_horizon() < D:
            dp(4, 3, "Too short.")
            continue

        # Check whether we are dominated by some processed path
        dominated = False
        new_df = path.get_df()
        for p in maxpaths:
            df = p.get_df()
            dominated = all([df[i] >= new_df[i] for i in range(D)])
            if dominated:
                dp(4, 3, "Dominated by %s." % p)
                break
        if dominated:
            continue
        dp(4, 3, "New. Will add.")

        # Remove all paths dominated by us
        remove_paths = set()
        for p in maxpaths:
            df = p.get_df()
            dominated = all([df[i] <= new_df[i] for i in range(D)])
            if dominated:
                dp(4, 4, "Dominates: %s" % p)
                remove_paths.add(p)
        maxpaths.difference_update(remove_paths)

        # Done. Add finally.
        maxpaths.add(path)


def add_to_maxpaths_rfdf(paths, maxpaths, D):
    for path in paths:

        dp(3, 2, "Processing: %s" % path)

        # Check whether too short
        if path.get_horizon() < D:
            dp(4, 3, "Too short.")
            continue

        # Check whether we are dominated by some processed path
        dominated = False
        new_rf = path.get_rf()
        new_df = path.get_df()
        for p in maxpaths:
            rf = p.get_rf()
            df = p.get_df()
            dominated = (all([rf[i] >= new_rf[i] for i in range(D)]) and
                all([df[i] >= new_df[i] for i in range(D)]))
            if dominated:
                dp(4, 3, "Dominated by %s." % p)
                break
        if dominated:
            continue
        dp(4, 3, "New. Will add.")

        # Remove all paths dominated by us
        remove_paths = set()
        for p in maxpaths:
            rf = p.get_rf()
            df = p.get_df()
            dominated = (all([rf[i] <= new_rf[i] for i in range(D)]) and
                all([df[i] <= new_df[i] for i in range(D)]))
            if dominated:
                dp(4, 4, "Dominates: %s" % p)
                remove_paths.add(p)
        maxpaths.difference_update(remove_paths)

        # Done. Add finally.
        maxpaths.add(path)


def TS_from_TS(TS):
    """Clones a TaskSet, all the way down to cloning jobs etc."""

    tasks = []

    for T in TS.tasks:
        newjobs = []
        jobmapping = {}
        for j in T.jobs:
            newj = Job(j.E, j.D, name=j.name)
            newjobs.append(newj)
            jobmapping[j] = newj
        for j in T.jobs:
            newj = jobmapping[j]
            for (j2, sep) in j.succs.items():
                newj.add_succ(j2, sep)
        newT = Task(newjobs, name=T.name)

        tasks.append(newT)

    return TaskSet(tasks)


def generate_dbf(paths, D):
    dp(2, 1, 'Generating dbf from paths...')
    dbf = [0] * (D + 1)
    witnesses = [None] * (D + 1) # Witness paths.
    for path in paths:
        e = path.get_e()
        d = path.get_d()
        t = d
        while t <= D and dbf[t] < e:
            dbf[t] = e
            witnesses[t] = path
            t += 1
    return (dbf, witnesses)


def generate_rbf(paths, D):
    dp(2, 1, 'Generating rbf from paths...')
    rbf = [0] * (D + 1)
    witnesses = [None] * (D + 1) # Witness paths.
    for path in paths:
        e = path.get_e()
        p = path.get_p()
        t = p
        while t <= D and rbf[t] < e:
            rbf[t] = e
            witnesses[t] = path
            t += 1
    return (rbf, witnesses)



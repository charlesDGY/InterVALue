"""Basic Path and PathStore templates to be used by specific abstractions."""

from debug import debug_print as dp

class Path(object):
    
    """Basic template for *all* path abstraction classes. Both dbf and
    utilization path abstractions need to implement these methods.
    """

    def __init__(self, jobs):
        """Create a Path from the non-empty sequence of jobs."""
        self.jobs = jobs

    def get_start(self):
        """Return the first job in the path."""
        raise NotImplementedError

    def get_end(self):
        """Return the last job in the path."""
        raise NotImplementedError

    def get_extended(self, job):
        """Return a list of new paths that are the possible extensions
        of this path with the node <job>.
        """
        raise NotImplementedError

    def __ge__(self, o):
        """Domination relation"""
        raise NotImplementedError

    def __gt__(self, o):
        """Strict domination relation"""
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class RfPath(Path):
    
    """Template for path abstraction classes used to do fp analysis."""

    def get_rf(self):
        """Return request function of that path."""
        raise NotImplementedError

    def get_horizon(self):
        """Return rf horizon, i.e., how far the function is defined."""
        raise NotImplementedError

    def distance_to(self, o):
        """Return distance to path o. Distance is pointwise distance of
        request functions with exponentially decreasing weight."""
        rf1 = self.get_rf()
        rf2 = o.get_rf()
        base = 0.01**(1.0/self.get_horizon())
        return sum([abs(rf1[i] - rf2[i])*(0.8**i)
            for i in xrange(self.get_horizon())])


class DfPath(Path):
    
    """Template for path abstraction classes used to do edf-rta."""

    def get_df(self):
        """Return demand function of that path."""
        raise NotImplementedError

    def get_rf(self):
        """Return request function of that path."""
        raise NotImplementedError

    def get_horizon(self):
        """Return rf horizon, i.e., how far the function is defined."""
        raise NotImplementedError

    def distance_to(self, o):
        """Return distance to path o. Distance is pointwise distance of
        request and demand functions with exponentially decreasing weight."""
        base = 0.01**(1.0/self.get_horizon())
        df1 = self.get_df()
        df2 = o.get_df()
        dfdist = sum([abs(df1[i] - df2[i])*(0.8**i)
            for i in xrange(self.get_horizon())])
        return dfdist

class RfDfPath(Path):
    
    """Template for path abstraction classes used to do edf-rta."""

    def get_df(self):
        """Return demand function of that path."""
        raise NotImplementedError

    def get_rf(self):
        """Return request function of that path."""
        raise NotImplementedError

    def get_horizon(self):
        """Return rf horizon, i.e., how far the function is defined."""

    def distance_to(self, o):
        """Return distance to path o. Distance is pointwise distance of
        request and demand functions with exponentially decreasing weight."""
        base = 0.01**(1.0/self.get_horizon())
        rf1 = self.get_rf()
        rf2 = o.get_rf()
        rfdist = sum([abs(rf1[i] - rf2[i])*(0.8**i)
            for i in xrange(self.get_horizon())])
        df1 = self.get_df()
        df2 = o.get_df()
        dfdist = sum([abs(df1[i] - df2[i])*(0.8**i)
            for i in xrange(self.get_horizon())])
        return rfdist + dfdist


class DbfPath(Path):
    
    """Template for path abstraction classes used to compute the dbf."""

    def get_e(self):
        """Return the total execution requirement for the path."""
        raise NotImplementedError

    def get_d(self):
        """Return the deadline of the path (i.e., the latest deadline
        relative to the spawning of the first job).
        """
        raise NotImplementedError


class UtilizationPath(Path):
    
    """Template for path abstraction classes used to compute utilization."""

    def get_p(self):
        """Return the total duration of the path (i.e., the minimal time
        required to spawn all jobs in it).
        """
        raise NotImplementedError

    def get_e2(self):
        """Return total execution requirement of a cycle (i.e., don't include
        the end node twice).
        """ 
        raise NotImplementedError

    def get_start(self):
        """Return the first job in the path."""
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class PathStore(object):

    """Basic template for all path stores."""

    def __init__(self):
        """Create a basic PathStore, which imposes no restrictions on
        the paths that can be stored.
        """
        self.stored = set()      # Paths that have already been extended.
        self.fresh = set()      # Paths that have not yet been extended.

    def pop_fresh(self):
        """Return one path on the 'frontier' of the explored paths, i.e.,
        one that has not previously been extended. Afterwards the path is
        marked non-fresh.
        """
        if len(self.fresh) > 0:
            path = self.fresh.pop()
            self.stored.add(path)
            return path
        return None

    def add_paths(self, paths):
        """Add the paths in the list <paths> to the set of frontier paths
        (given that they are valid and relevant)."""
        for path in paths:
            if self.should_be_stored(path):
                self.fresh.add(path)
                dp(4, 0, "Stored %s." % path)
            else:
                dp(4, 0, "Discarded %s." % path)


    def get_stored_num(self):
        """Return the number of stored (already extended) paths."""
        return len(self.stored)

    def get_fresh_num(self):
        """Return the number of fresh (not yet extended) paths."""
        return len(self.fresh)

    def get_paths(self):
        """Return the set of generated paths."""
        return self.stored

    def should_be_stored(self, path):
        """Return True if this task should be added to the store (e.g.,
        if the path falls within specified bounds or is relevant for what
        is being computed).
        """
#        raise NotImplementedError
        # Default: Store everything
        return True

 
class RfPathStore(PathStore):
    
    """A basic PathStore for Paths in rf computations. Only discards paths
    that have a horizon of at least D.
    """

    def __init__(self, D):
        self.D = D
        super(RfPathStore, self).__init__()

    def add_paths(self, paths):
        """Add the paths in the list <paths> to the store.
        If path does not exceed horizon yet, store it in fresh set.
        """
        for path in paths:
            if self.is_todo(path):
                self.fresh.add(path)
                dp(4, 0, "Stored todo %s." % path)
            else:
                self.stored.add(path)
                dp(4, 0, "Stored non-todo %s." % path)


    def is_todo(self, path):
        return path.get_horizon() < self.D


class RfDfPathStore(PathStore):
    
    """A basic PathStore for Paths in rfdf computations. Only discards paths
    that have a horizon of at least D.
    """

    def __init__(self, D):
        self.D = D
        super(RfDfPathStore, self).__init__()

    def add_paths(self, paths):
        """Add the paths in the list <paths> to the store.
        If path does not exceed horizon yet, store it in fresh set.
        """
        for path in paths:
            if self.is_todo(path):
                self.fresh.add(path)
                dp(4, 0, "Stored todo %s." % path)
            else:
                self.stored.add(path)
                dp(4, 0, "Stored non-todo %s." % path)


    def is_todo(self, path):
        return path.get_horizon() < self.D


class DbfPathStore(PathStore):
    
    """A basic PathStore for Paths in dbf computations. Only discards paths
    that have a deadline exceeding the bound <D>.
    """

    def __init__(self, D):
        self.D = D
        super(DbfPathStore, self).__init__()

    def should_be_stored(self, path):
        return path.get_d() <= self.D


class UtilizationPathStore(PathStore):
    
    """A basic PathStore for Paths in utilization computations. Only
    discards paths that have are longer than the <maxlen>.
    """
    def __init__(self, maxlen):
        self.maxlen = maxlen
        super(UtilizationPathStore, self).__init__()

    def should_be_stored(self, path):
        return len(path) <= self.maxlen


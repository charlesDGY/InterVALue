from debug import debug_print as dp
import debug


class ExplorationEngine(object):

    """The ExplorationEngine generates all paths in a Task (using the
    abstracton of a given Path class) and stores them in a given
    path store.
    """

    def __init__(self, task, store, path_creator, 
            start_jobs = None, backwards = False):
        """path_creator is a function taking a list of jobs and returning
        a path object. This can be a class (so the function is implicitly the 
        constructor) or a wrapper function.

        start_jobs: Which jobs to start at. (Default: All.)
        backwards: If True, extend paths in the front. (Default: False)
        """
        self.task = task
        self.store = store

        # TODO: path_creator is only used for creating initial paths from
        # start_jobs. Better would be to just supply the initial set of
        # paths with default to all 0-paths created from all jobs via
        # some default (or supplied?) path class
        self.path_creator = path_creator
        self.start_jobs = start_jobs or task.jobs
        self.backwards = backwards

    def run(self):
        """Run the ExplorationEngine until completion."""
        dp(3, 0, 'ExplorationEngine starting...')

        # Add all vertices as paths of length 0.
        dp(3, 1, 'Adding 0-paths to path store...')
        paths = [self.path_creator([job]) for job in self.start_jobs]
        debug.down(2)
        self.store.add_paths(paths)
        debug.up(2)
        dp(3, 2, 'Added %d 0-paths to store.' % self.store.get_fresh_num())

        # Build the rest of the paths for the path store one by one.
        dp(3, 1, 'Generating k-paths...')
        while True:
            dp(3, 2, 'Currently %d stored, %d fresh.' %
                (self.store.get_stored_num(), self.store.get_fresh_num()))
            path = self.store.pop_fresh()
            if path is None:
                break
            dp(4, 2, 'Extending %s...' % path)
            if self.backwards:
                u = path.get_start()
                extension_vertices = u.get_prevs()
            else:
                u = path.get_end()
                extension_vertices = u.succs
            for v in extension_vertices:
                dp(4, 3, '... with %s. Candidates:' % v)
                debug.down(4)
                ext_paths = path.get_extended(v)
                self.store.add_paths(ext_paths)
                debug.up(4)
                # * What if we haven't stored any extension, shouldn't
                # the original path be stored then? We might lose a critical
                # path otherwise. (?)
                #   - Well, if all extensions are non-critical, how can the
                #   path itself be critical?
                #     - Depends on what type of path abstraction we are 
                #       deadling with. This is regulated via the store. 
                #       -> For demand triples, the pop_fresh() method always 
                #       saves the popped path directly in the store, 
                #       so it's preserved.
                #       -> For rfpaths, it doesn't since there is no reason to
                #       do so.

        dp(3, 1, 'Done generating paths, %d paths stored in total' %
            self.store.get_stored_num())


class IncrementalExplorationEngine(object):

    """The IncrementalExplorationEngine generates all paths in a Task (using the
    abstracton of a given Path class) and stores them in a given
    path store. The run(increments) method yields after every increments steps
    with the guarantee that all paths up to this time-length are
    already created in the store.
    """

    def __init__(self, task, store, path_creator):
        """path_creator is a function taking a list of jobs and returning
        a path object. This can be a class (so the function is implicitly the 
        constructor) or a wrapper function.

        Note: store needs to support store.current_limit and is expected to
        pop paths in suitable increasing order.
        """
        self.task = task
        self.store = store
        self.path_creator = path_creator

    def run(self, increments):
        """Run the ExplorationEngine for increments steps at a time."""
        dp(3, 0, 'ExplorationEngine starting...')

        # Add all vertices as paths of length 0.
        dp(3, 1, 'Adding 0-paths to path store...')
        paths = [self.path_creator([job]) for job in self.task.jobs]
        debug.down(2)
        self.store.add_paths(paths)
        debug.up(2)
        dp(3, 2, 'Added %d 0-paths to store.' % self.store.get_fresh_num())

        # Build the rest of the paths for the path store one by one.
        dp(3, 1, 'Generating k-paths...')
        current_limit = increments
        while True:
            dp(3, 2, 'Currently %d stored, %d fresh.' %
                (self.store.get_stored_num(), self.store.get_fresh_num()))
            if self.store.current_limit > current_limit:
                dp(2, 2, "Store is complete up to %d (>%d). Yielding." %
                    (self.store.current_limit, current_limit))
                yield
                current_limit += increments
            path = self.store.pop_fresh()
            if path is None:
                break
            dp(4, 2, 'Extending %s...' % path)
            u = path.get_end()
            for v in u.succs:
                dp(4, 3, '... with %s. Candidates:' % v)
                debug.down(4)
                ext_paths = path.get_extended(v)
                self.store.add_paths(ext_paths)
                debug.up(4)

        dp(3, 1, 'Done generating paths, %d paths stored in total' %
            self.store.get_stored_num())


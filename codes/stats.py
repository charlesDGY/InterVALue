import task
import time
import examples
import debug

import signal
import itertools
import random

from matplotlib import pyplot
from matplotlib import rc
gg_total_lvls = 3
gg_happy_lvls = [0]*6
gg_skip_bad = True
# From http://pguides.net/python-tutorial/python-timeout-a-function/
# with a bugfix that calls f actually with *args.
class TimeoutException(Exception):
    pass
def timeout_unix(timeout_time, default):
    def timeout_function(f):
        def f2(*args,**argh):
            def timeout_handler(signum, frame):
                raise TimeoutException()
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_time) # triger alarm in timeout_time seconds
            try:
                retval = f(*args,**argh)
                signal.alarm(0) # [Robin] AVOID the timeout alarm that raised in FINALLY
            except TimeoutException:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler)
                signal.alarm(0) # [Robin] AVOID recursive alarm ???
            return retval
        return f2
    return timeout_function

def timeout_win(timeout_time, default):
    def timeout_function(f):
        def f2(*args,**argh):
            try:
                retval = f(*args,**argh)
            except TimeoutException:
                return default
            finally:
                pass
            return retval
        return f2
    return timeout_function

timeout=timeout_unix
try:
    signal.SIGALRM
except AttributeError:
    timeout = timeout_win
    print 'Unsupported signal.SIGALRM'

@timeout(100, None)
def run_experiment(taskset, exp_type, given_order=False):

    taskset.reset()
    xx = 'rf_iterative'
    if exp_type == 'dbf':
        return taskset.is_feasible()
    elif exp_type == 'rf-go': ## [Robin] Just check the given priorities order
        if given_order:
            return taskset.is_fp_schedulable(force_solver='rf_iterative')
        else:
            return taskset.is_fp_feasible(force_solver='rf_iterative',given_order=False) ## [Robin]
    elif exp_type == 'rf-go-m': ## [Robin] Just check the given priorities order
        res = False
        for lvl in range(0,gg_total_lvls):
            import copy
            ts = copy.deepcopy(taskset)
            ts.modify_rlease_delay(level=lvl, given_order=given_order)
            if given_order:
                res = ts.is_fp_schedulable(force_solver='rf_iterative')
            else:
                res = ts.is_fp_feasible(force_solver='rf_iterative',given_order=given_order)
            if res is None or res:
                gg_happy_lvls[lvl] += 1 * (not not res)
                break
        return res
    elif exp_type == 'rbf-go': ## [Robin] Just check the given priorities order
        return taskset.is_fp_schedulable(force_solver='rf_iterative') ## [Robin]
        #return taskset.is_fp_feasible(force_solver='rf_iterative',given_order=True) ## [Robin]
    elif exp_type == 'rbf-go-m': ## [Robin] Just check the given priorities order
        res = False
        for lvl in range(0,3):
            import copy
            ts = copy.deepcopy(taskset)
            ts.modify_rlease_delay(level=lvl, given_order=True)
            res = ts.is_fp_schedulable (force_solver='rf_iterative')
            #res = ts.is_fp_feasible(force_solver='rf_iterative',given_order=True)
            if res is not None and res:
                break
        return res
    elif exp_type == 'rbf':
        return taskset.is_fp_feasible(force_solver='rbf')
    elif exp_type == 'rf_iterative':
        return taskset.is_fp_feasible(force_solver='rf_iterative')
    elif exp_type == 'rfpaths':
        return taskset.fake_run_prepare_rfpaths()
    elif exp_type == 'rta-fp':
        res = taskset.get_fp_order()
        if not res:
            return "INFEASIBLE"
        else:
            taskset2 = task.TaskSet(res)
            return taskset2.rta_fp()
    elif exp_type == 'rta-edf':
        res = taskset.is_feasible()
        if not res:
            return "INFEASIBLE"
        else:
            return taskset.rta_edf()

def T_gen_Robin(t = None, tid = 0):
    """@todo: Docstring for T_gen_Robin.

    :t: @todo
    :tid: @todo
    :returns: @todo

    """
    if t is None:
        HML = ['H', 'M', 'L']
        t = HML[random.randint(0, 2)]
        t = '2'
    if t == 'H':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=50, p_max=100,
                        e_min=1, e_max=2,
                        d_min=100, d_max=100,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(H)"%tid)
    elif t == 'M':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=100, p_max=200,
                        e_min=1, e_max=4,
                        d_min=200, d_max=200,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(M)"%tid)
    elif t == 'L':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=200, p_max=300,
                        e_min=1, e_max=6,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(L)"%tid)
    elif t == '1':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=4,
                        p_min=50, p_max=300,
                        e_min=1, e_max=6,
                        d_min=300, d_max=600,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(M)"%tid)
    elif t == '2':
        return examples.RandomTask(size_min=6, size_max=13,
                        fanout_min=1, fanout_max=5,
                        p_min=50, p_max=300,
                        e_min=1, e_max=7,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(L)"%tid)
    pass

def T_gen_X3(t = None, tid = 0):
    if t is None:
        HML = ['H', 'M', 'L']
        t = HML[random.randint(0, 2)]
    if t == 'H':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=50, p_max=100,
                        e_min=1, e_max=2,
                        d_min=100, d_max=100,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(H)"%tid)
    elif t == 'M':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=100, p_max=200,
                        e_min=1, e_max=4,
                        d_min=200, d_max=200,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(M)"%tid)
    elif t == 'L':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=200, p_max=300,
                        e_min=1, e_max=6,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(L)"%tid)

#def scaletask(factor):



def T_gen_X4(t = None, tid = 0):
    """Slow, but implicit deadlines, so EDF is close to 100% and
    the whole comparison is more meaningful.
    """
    if t is None:
        HML = ['H', 'M', 'L']
        t = HML[random.randint(0, 2)]
    if t == 'H':
        return examples.RandomTask(size_min=3, size_max=5,
                        fanout_min=1, fanout_max=3,
                        p_min=25, p_max=50,
                        e_min=1, e_max=2,
                        d_min=50, d_max=50,
#                        d_min=25, d_max=100,
                        d_implicit=True,
                        name="T%d(H)"%tid)
    elif t == 'M':
        return examples.RandomTask(size_min=5, size_max=9,
                        fanout_min=1, fanout_max=4,
                        p_min=50, p_max=100,
                        e_min=2, e_max=4,
                        d_min=100, d_max=100,
#                        d_min=50, d_max=200,
                        d_implicit=True,
                        name="T%d(M)"%tid)
    elif t == 'L':
        return examples.RandomTask(size_min=7, size_max=13,
                        fanout_min=1, fanout_max=5,
                        p_min=100, p_max=200,
                        e_min=3, e_max=6,
                        d_min=200, d_max=200,
#                        d_min=100, d_max=200,
                        d_implicit=True,
                        name="T%d(L)"%tid)

def T_gen_X5(t = None, tid = 0):
    """This is all much faster, but the deadlines are not implicit.
    Thus, the statistics don't say so much...
    """
    if t is None:
        HML = ['H', 'M', 'L']
        t = HML[random.randint(0, 2)]
    if t == 'H':
        return examples.RandomTask(size_min=3, size_max=5,
                        fanout_min=1, fanout_max=3,
                        p_min=50, p_max=100,
                        e_min=1, e_max=2,
#                        d_min=100, d_max=100,
                        d_min=25, d_max=100,
#                        d_implicit=True,
                        name="T%d(H)"%tid)
    elif t == 'M':
        return examples.RandomTask(size_min=5, size_max=9,
                        fanout_min=1, fanout_max=4,
                        p_min=100, p_max=200,
                        e_min=1, e_max=4,
#                        d_min=200, d_max=200,
                        d_min=50, d_max=200,
#                        d_implicit=True,
                        name="T%d(M)"%tid)
    elif t == 'L':
        return examples.RandomTask(size_min=7, size_max=13,
                        fanout_min=1, fanout_max=5,
                        p_min=200, p_max=400,
                        e_min=1, e_max=8,
#                        d_min=300, d_max=300,
                        d_min=100, d_max=400,
#                        d_implicit=True,
                        name="T%d(L)"%tid)

def T_gen_X6(tid = 0):
    return examples.RandomTaskNew(size_min=5, size_max=10,
        fanout_min=1, fanout_max=3,
        p_min=10, p_max=300,
        ratioed_min=0.001, ratioed_max=0.07,
        name="T%d"%tid)

def T_gen_X7(tid = 0):
    return examples.RandomTaskNew(size_min=5, size_max=10,
        fanout_min=1, fanout_max=3,
        p_min=100, p_max=300,
        ratioed_min=0.001, ratioed_max=0.07,
#        d_implicit = True,
        name="T%d"%tid)

def TS_iter(T_gen, len_range=None, U_range=None):
    if len_range is not None:
        for goal_len in itertools.cycle(len_range):
            TS = task.TaskSet([T_gen(tid = i) for i in xrange(goal_len)])
            yield TS

    elif U_range is not None:
        for goal_U in itertools.cycle(U_range):
            U = 0.0
            i = 0
            tasks = [T_gen(tid = i)]
            while U < goal_U:
                i += 1
                T = T_gen(tid = i)
                U += T.get_utilization()
                tasks.append(T)
            TS = task.TaskSet(tasks)
            yield TS


def acceptance_experiment(U_range = None, len_range = None, exp_types = ['dbf', 'rf_iterative', 'rfpaths'],
        T_gen=T_gen_X5, repeats=3):

    if U_range is None and len_range is None:
        raise RuntimeError('Specify U_range or len_range.')

    debug.set_level(-1)
    #debug.set_level(1)

    experiments = list()

    try:

        tried = 0
        failed = 0
        happy = 0
        sad = 0
        for TS in TS_iter(T_gen, len_range=len_range, U_range=U_range):

            exp = dict()

            #exp['taskset'] = TS
            exp['U'] = TS.get_utilization()
            exp['size'] = len(TS.tasks)

            print "Current experiment:"
            print "  Tasks: %d" % len(TS.tasks)
            print "  Utilization: %.2f" % exp['U']

            for exp_type in exp_types:

                times = []
                for i in range(repeats):
                    timer = time.time()
                    res = run_experiment(TS, exp_type)
                    times.append(time.time() - timer)
                    if res is None:
                        break
                #print "  Tasks: %d" % len(TS.tasks)
                #print "  Utilization: %.2f" % exp['U']

                exp[exp_type + '-time'] = min(times)
                exp[exp_type + '-res'] = res

                print "  %s-time: %.2f (%s)" % (exp_type, min(times),
                    ", ".join(["%.2f" % t for t in times]))
                print "  %s-res: %s" % (exp_type, str(res))

            #print "  Tasks: %d" % len(TS.tasks)
            #print "  Utilization: %.2f" % exp['U']
            experiments.append(exp)
            ress = [exp[t+'-res'] for t in exp_types]
            tried += 1
            if not ress[0]:
                failed += 1
            #print 'tried = %d times, faild = %d' % (tried, failed)
            if not all([ress[0]==r for r in ress]):
                if not ress[0]:
                    happy += 1
                else:
                    sad += 1
            ff = failed
            if ff == 0 : ff = 1
            print "=========== happy=%d, sad=%d, faild=%d, ratio =%0.2f, total=%d, ok = %0.2f"%(happy, sad, failed, happy*1.0/ff, tried, (tried-failed)*1.0/tried)
                #break

    except KeyboardInterrupt:
        pass

    return experiments

def acceptance_experiment_robin(U_range = None, len_range = None, exp_types = ['dbf', 'rf_iterative', 'rfpaths'],
        T_gen=T_gen_X5, repeats=3, sort_ts=True, given_order=False):

    if U_range is None and len_range is None:
        raise RuntimeError('Specify U_range or len_range.')

    debug.set_level(-1)
    #debug.set_level(1)

    experiments = list()

    try:

        tried = 0
        failed = 0
        happy = 0
        sad = 0
        bad = 0
        for TS in TS_iter(T_gen, len_range=len_range, U_range=U_range):

            if sort_ts:
                TS.tasks.sort(key=lambda x:min([y.get_d() for y in x.get_jobs()]))

            import copy
            if gg_skip_bad and not copy.deepcopy(TS).modify_rlease_delay(level=-1,given_order=given_order):
                bad += 1
                print '======================================, bad =' , bad
                continue
            exp = dict()

            #exp['taskset'] = TS
            exp['U'] = TS.get_utilization()
            exp['size'] = len(TS.tasks)
            exp['jobs'] = sum([len(tt.get_jobs()) for tt in TS.tasks])

            print "Current experiment:"
            print "  Tasks: %d, Jobs: %d" % (len(TS.tasks), exp['jobs'])
            print "  Utilization: %.2f" % exp['U']

            ok = False
            times = []
            for exp_type in exp_types:
                if ok and False:
                    exp[exp_type + '-time'] = min(times)
                    exp[exp_type + '-res'] = True
                    break
                times = []
                for i in range(repeats):
                    timer = time.time()
                    res = run_experiment(TS, exp_type,given_order=given_order)
                    times.append(time.time() - timer)
                    if res is None:
                        break
                #print "  Tasks: %d" % len(TS.tasks)
                #print "  Utilization: %.2f" % exp['U']

                exp[exp_type + '-time'] = min(times)
                exp[exp_type + '-res'] = res
                ok = res

                print "  %s-time: %.2f (%s)" % (exp_type, min(times),
                    ", ".join(["%.2f" % t for t in times]))
                print "  %s-res: %s" % (exp_type, str(res))

            #print "  Tasks: %d" % len(TS.tasks)
            #print "  Utilization: %.2f" % exp['U']
            experiments.append(exp)
            ress = [exp[t+'-res'] for t in exp_types]
            tried += 1
            if not ress[0]:
                failed += 1
            #print 'tried = %d times, faild = %d' % (tried, failed)
            if ress[0] is not None and not all([ress[0]==r for r in ress]):
                if not ress[0]:
                    happy += 1
                else:
                    sad += 1
            ff = failed
            if ff == 0 : ff = 1
            hh = max(1,happy) * 1.0
            print "======== happy=%d, sad=%d, failed=%d, bad=%d, ratio =%0.2f, total=%d, ok = %0.2f"%(happy, sad, failed, bad, happy*1.0/ff, tried, (tried-failed)*1.0/tried)
            fmt = "******** "
            vals = []
            for i in range(gg_total_lvls):
                fmt += "lvl_%d= %%d(%%0.2f); "%(i)
                vals += [gg_happy_lvls[i],gg_happy_lvls[i]/hh]
            fmt += 'total= %d'
            vals += [happy]

            #print fmt, vals
            print fmt % tuple(vals)
            #print "******** lvl_0= %d(%0.2f); lvl_1= %d(%0.2f), lvl_2= %d(%0.2f), total=%d" %(gg_happy_lvls[0], gg_happy_lvls[0]/hh,gg_happy_lvls[1], gg_happy_lvls[1]/hh,gg_happy_lvls[2], gg_happy_lvls[2]/hh,happy)
                #break




    except KeyboardInterrupt:
        pass

    return experiments

def acceptance_experiment_robin_mixed(U_range = None, len_range = None, exp_types = ['rf-go:k:fix','rf-go-m:fix', 'rf-go:opa', 'rf-go-m:opa'],
        T_gen=T_gen_X5, repeats=3, sort_ts=True, given_order=False):

    if U_range is None and len_range is None:
        raise RuntimeError('Specify U_range or len_range.')

    debug.set_level(-1)
    #debug.set_level(1)

    experiments = list()

    try:

        tried = 0
        failed = 0
        happy = 0
        sad = 0
        bad = 0
        for TS in TS_iter(T_gen, len_range=len_range, U_range=U_range):

            if sort_ts:
                TS.tasks.sort(key=lambda x:min([y.get_d() for y in x.get_jobs()]))

            import copy
            if gg_skip_bad and not copy.deepcopy(TS).modify_rlease_delay(level=-1,given_order=given_order):
                bad += 1
                print '======================================, bad =' , bad
                continue
            exp = dict()

            #exp['taskset'] = TS
            exp['U'] = TS.get_utilization()
            exp['size'] = len(TS.tasks)
            exp['jobs'] = sum([tt.get_jobs() for tt in TS.tasks])

            print "Current experiment:"
            print "  Tasks: %d, Vertices: %d" % len(TS.tasks), exp['jobs']
            print "  Utilization: %.2f" % exp['U']

            ok = False
            times = []
            for exp_type in exp_types:
                slices = exp_type.split(':')
                #exp_type = slices[0]
                keys=dict.fromkeys(slices,True)
                if ok and not False:
                    exp[exp_type + '-time'] = min(times)
                    exp[exp_type + '-res'] = True
                    continue
                times = []
                for i in range(repeats):
                    timer = time.time()
                    if keys.has_key('fix'):
                        go = True
                    elif keys.has_key('opa'):
                        go = False
                    else:
                        go = given_order
                    res = run_experiment(TS, slices[0],given_order=go)
                    times.append(time.time() - timer)
                    if res is None:
                        break
                #print "  Tasks: %d" % len(TS.tasks)
                #print "  Utilization: %.2f" % exp['U']

                exp[exp_type + '-time'] = min(times)
                exp[exp_type + '-res'] = res
                if keys.has_key('k'):
                    ok = res


                print "  %s-time: %.2f (%s)" % (exp_type, min(times),
                    ", ".join(["%.2f" % t for t in times]))
                print "  %s-res: %s" % (exp_type, str(res))

            #print "  Tasks: %d" % len(TS.tasks)
            #print "  Utilization: %.2f" % exp['U']
            experiments.append(exp)
            ress = [exp[t+'-res'] for t in exp_types]
            tried += 1
            if not ress[0]:
                failed += 1
            #print 'tried = %d times, faild = %d' % (tried, failed)
            if not all([ress[0]==r for r in ress]):
                if not ress[0]:
                    happy += 1
                else:
                    sad += 1
            ff = failed
            if ff == 0 : ff = 1
            hh = max(1,happy) * 1.0
            print "======== happy=%d, sad=%d, failed=%d, bad=%d, ratio =%0.2f, total=%d, ok = %0.2f"%(happy, sad, failed, bad, happy*1.0/ff, tried, (tried-failed)*1.0/tried)
            fmt = "******** "
            vals = []
            for i in range(gg_total_lvls):
                fmt += "lvl_%d= %%d(%%0.2f); "%(i)
                vals += [gg_happy_lvls[i],gg_happy_lvls[i]/hh]
            fmt += 'total= %d'
            vals += [happy]

            #print fmt, vals
            print fmt % tuple(vals)
            #print "******** lvl_0= %d(%0.2f); lvl_1= %d(%0.2f), lvl_2= %d(%0.2f), total=%d" %(gg_happy_lvls[0], gg_happy_lvls[0]/hh,gg_happy_lvls[1], gg_happy_lvls[1]/hh,gg_happy_lvls[2], gg_happy_lvls[2]/hh,happy)
                #break




    except KeyboardInterrupt:
        pass

    return experiments


def rta_experiment(U_range = None, len_range = None, exp_types = ['rta-fp', 'rta-edf'],
        T_gen=T_gen_X7, repeats=1):

    if U_range is None and len_range is None:
        raise RuntimeError('Specify U_range or len_range.')

    debug.set_level(-1)

    experiments = list()

    try:

        for TS in TS_iter(T_gen, len_range=len_range, U_range=U_range):

            exp = dict()

            #exp['taskset'] = TS
            exp['U'] = TS.get_utilization()
            exp['size'] = len(TS.tasks)

            print "Current experiment:"
            print "  Tasks: %d" % len(TS.tasks)
            print "  Utilization: %.2f" % exp['U']

            for exp_type in exp_types:

                times = []
                for i in range(repeats):
                    timer = time.time()
                    res = run_experiment(TS, exp_type)
                    times.append(time.time() - timer)
                    if res is None:
                        break

                if res is None:
                    print "  %s-timeout." % exp_type
                    exp[exp_type + '-time'] = min(times)
                elif res == "INFEASIBLE":
                    print "  %s-infeasible." % exp_type
                    exp[exp_type + '-time'] = "INFEASIBLE"
                else:
                    exp[exp_type + '-time'] = min(times)

                    print "  %s-time: %.2f (%s)" % (exp_type, min(times),
                        ", ".join(["%.2f" % t for t in times]))

            experiments.append(exp)


    except KeyboardInterrupt:
        pass

    return experiments


def ii(val, low, step=1):
    return val >= low and val < low + step
def ff(val, low, step=1):
    return val >= low*1.0/100 and val < (low+step)*1.0/100
def pp_ratio(r, ts, X):
    """r: range to be displayed, e.g., range(100)
    ts: types to be display, e.g., ['dbf', 'rbf']
    X: list of dictionaries, i.e., experiment results
    """
    for i in r:
        print "%d%%:" % (i*100),
        for t in ts:
            positives = len([x for x in X if x[t+"-res"] and ii(x['U'], i, 0.01)])
            total = len([x for x in X if ii(x['U'], i, 0.01)])
    #            total = len([x for x in X if ii(x['U'], i) and x[t+"-res"] is not None])
            print "[%s: %d/%d (%.2f%%)]" % (t,
                positives, total, positives*100.0/total if total > 0 else -1),
        print


def pp_time(r, ts, X):
    """r: range to be displayed, e.g., range(100)
    ts: types to be display, e.g., ['dbf', 'rbf']
    X: list of dictionaries, i.e., experiment results
    """
    for i in r:
        print "%d%%:" % (i*100),
        for t in ts:
            total = len([x for x in X if ii(x['U'], i, 0.01) and x[t+"-res"] is not None])
            avg_time = sum([x[t+"-time"] for x in X if ii(x['U'], i, 0.01) and x[t+"-res"] is not None]) / total if total > 0 else -1
            print "[%s: %.2f in %d]" % (t,
                avg_time, total),
        print


def plotit(X, r=range(100), ts=['dbf', 'rf_iterative'], xgroup='U', fmt=None,
        xlim=None, ylim=(0, 50), minslotsize=10, labels=None, xlabel=None, ylabel=None):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    ts: types to be display, defaults to ['dbf', 'rf_iterative']
    xgroup: property of X elements to group by, defaults to 'U'
    """

    rc('text', usetex=True)
    rc('font', family='serif')

    plotdata = dict([(t, list()) for t in ts])
    fmt = fmt or dict([(t, 'ko-') for t in ts])
    labels = labels or dict([(t, t) for t in ts])
    xlabel = xlabel or 'Task Set Utilization'
    ylabel = ylabel or 'Analysis Run-Time'

    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            times = [x[t+"-time"] for x in X
                if ii(x[xgroup], j, step) and x[t+"-res"] is not None]
            total = len(times)
            avg_time = sum(times) / total if total >= minslotsize else None
            times.sort()
            med_time = times[total/2] if total >= minslotsize else None
            print "[%s: avg %.2f med %.2f in %d]" % (t, avg_time or -1, med_time or -1, total),
            plotdata[t].append(avg_time)
        print

    for t in ts:
        pyplot.plot(r[:-1], plotdata[t], fmt[t], label=labels[t], linewidth=2)
    pyplot.grid(True)
    pyplot.legend(loc = "upper left")
    if xlim is not None:
        pyplot.xlim(xlim[0], xlim[1])
    if ylim is not None:
        pyplot.ylim(ylim[0], ylim[1])
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.show()


def plot_runtime_over_U(X, r=range(100), t="rta-edf"):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """

    ts = [t]

    rc('text', usetex=True)
    rc('font', family='serif')

    plotdata = dict([(t, list()) for t in ts])
    minslotsize = 10

    for i, j in enumerate(r[:-1]):
        #print "%s:" % j,
        step = r[i+1] - r[i]
        times = [x[t+"-time"] for x in X
            if ii(x['U'], j, step) and x[t+"-time"]!="INFEASIBLE"]
        total = len(times)
        avg_time = sum(times) / total if total >= minslotsize else None
        times.sort()
        med_time = times[total/2] if total >= minslotsize else None
        #print "[%s: avg %.2f med %.2f in %d]" % (t, avg_time or -1, med_time or -1, total),
        plotdata[t].append(med_time)
        #print


    if t == "rta-fp":
        pyplot.figure(figsize=(3.0, 3.5))
    else:
        pyplot.figure(figsize=(3.4, 3.5))

    if t == "rta-fp":
        pyplot.plot(r[:-1], plotdata[t], 'ks-', label='SP',
            color="#000088", linewidth=2)
        xticks = [0.0, 0.1, 0.2, 0.3, 0.4]
        ylim = 0.8
        pyplot.subplots_adjust(bottom=0.13, left=0.22)
    else:
        pyplot.plot(r[:-1], plotdata[t], 'ko--', label='EDF',
            color="#880000", linewidth=2)
        xticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        ylim = 105
        pyplot.subplots_adjust(bottom=0.13, left=0.15)


    pyplot.grid(True)
    pyplot.xticks(xticks)
    pyplot.legend(loc = "upper left")
    pyplot.xlim(0, max(xticks) + 0.05)
    pyplot.ylim(0, ylim)
    pyplot.xlabel('Task Set Utilization')
    pyplot.ylabel('Analysis Run-Time (seconds)')
    pyplot.show()


def plot_runtime_over_size(X, r=range(100)):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """

    ts=['dbf', 'rf_iterative']

    rc('text', usetex=True)
    rc('font', family='serif')

    plotdata = dict([(t, list()) for t in ts])
    minslotsize = 10

    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            times = [x[t+"-time"] for x in X
                if ii(x['size'], j, step) and x[t+"-res"] is not None]
            total = len(times)
            avg_time = sum(times) / total if total >= minslotsize else None
            times.sort()
            med_time = times[total/2] if total >= minslotsize else None
            print "[%s: avg %.2f med %.2f in %d]" % (t, avg_time or -1, med_time or -1, total),
            plotdata[t].append(med_time)
        print


    pyplot.figure(figsize=(6, 4.2))
    pyplot.plot(r[:-1], plotdata['dbf'], 'ko--', label='EDF',
        color="#880088", linewidth=2)
    pyplot.plot(r[:-1], plotdata['rf_iterative'], 'ks-', label='SP',
        color="#000088", linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "upper left")
    #pyplot.xlim(0, 1)
    pyplot.ylim(0, 20)
    pyplot.xlabel('Task Set Size')
    pyplot.ylabel('Analysis Run-Time (seconds)')
    pyplot.show()


def plot_ratio_over_U_Robin(X, r=range(100),ys=[ ['rf-go:k:fix','refinement-MDM'],['rf-go-m:fix','shaping-MDM'], ['rf-go:opa','refinement-OPA'], ['rf-go-m:opa','shaping-OPA']]):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """

    ts=['rf-go', 'rf-go-m']
    if ys is not None:
        ts = [x[0] for x in ys]

    try:
        ts.index('rf-go-m:fix')
        ts.index('rf-go-m:opa')
        ts += ['shaping-full']
        for x in X:
            x['shaping-full-res'] = x['rf-go-m:fix-res'] or x['rf-go-m:opa-res']
    except:
        pass
    #rc('text', usetex=True)
    #rc('font', family='serif')
    #matplotlib.rcParams['xtick.direction'] = 'out'
    #matplotlib.rcParams['ytick.direction'] = 'out'
    #rc('xtick',direction='out')
    rc('xtick.major',width=1,size=5)
    rc('ytick.major',width=1,size=5)
    rc('grid',color='gray',linestyle=':',linewidth=0.7,alpha=0.9)
    #rc('ytick',direction='out')
    rc('text', usetex=True)
    rc('font', family='serif')

    def tc(r,g,b):
        return '#%02X%02X%02X' % (r,g,b)

    plotdata = dict([(t, list()) for t in ts])
    minslotsize = 10
    minslotsize = 1

    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            res = [x[t+"-res"] for x in X
                if ff(x['U'], j, step) and x[t+"-res"] is not None]
            total = len(res)
            #ratio = 1.0 * sum(res) / total if total >= minslotsize else None
            ratio = 100.0 * sum(res) / total if total >= minslotsize else None
            print "[%s: ratio %.2f in %d]" % (t, ratio or 0, total),
            plotdata[t].append(ratio)
        print

    r = [x/100.0 for x in r]
    pyplot.figure(figsize=(5, 4))
    #pyplot.subplots_adjust(bottom=0.13)
    pyplot.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.99)
    if ys is not None:
        pyplot.plot(r[:-1], plotdata['shaping-full'], '*-', label='shaping-Full',
            color="#CE191E", linewidth=1.5)
        pyplot.plot(r[:-1], plotdata['rf-go-m:fix'], 'ko-', label='shaping-MDM',
            color="#FED521", linewidth=1.5)
        pyplot.plot(r[:-1], plotdata['rf-go:k:fix'], 'ko--', label='refinement-MDM',
            color="#0D8461", linewidth=1.5)
        pyplot.plot(r[:-1], plotdata['rf-go-m:opa'], 'ks-', label='shaping-OPA',
            color="#315BA7", linewidth=1.5)
        pyplot.plot(r[:-1], plotdata['rf-go:opa'], 'ks--', label='refinement-OPA',
            color="#80007B", linewidth=1.5)
        #for (n,t) in ys:
            #print n,t
            #print plotdata[n]
            #pyplot(r[:-1], plotdata[n], 'ko--', label=t, color='"#880088', linewidth=2)
    else:
        pyplot.plot(r[:-1], plotdata['rf-go'], 'ko--', label='refinement',
            color="#880088", linewidth=2)
        pyplot.plot(r[:-1], plotdata['rf-go-m'], 'ks-', label='shaping',
            color="#000088", linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "lower left",title='', fontsize=12,shadow=False,handlelength=3.5,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    pyplot.yticks(range(0, 101, 20), ['%d' % d for d in range(0, 101, 20)])
    #pyplot.xlim(0, 100)
    #pyplot.ylim(-0.02, 1.02)
    pyplot.ylim(-2, 102)
    pyplot.xlabel('Task set utilization', fontsize=12)
    pyplot.ylabel('Acceptance ratio (\%)', fontsize=12)
    pyplot.show()

def plot_ratio_over_U(X, r=range(100)):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """

    ts=['dbf', 'rf_iterative']

    rc('text', usetex=True)
    rc('font', family='serif')

    plotdata = dict([(t, list()) for t in ts])
    minslotsize = 10

    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            res = [x[t+"-res"] for x in X
                if ii(x['U'], j, step) and x[t+"-res"] is not None]
            total = len(res)
            ratio = 1.0 * sum(res) / total if total >= minslotsize else None
            print "[%s: ratio %.2f in %d]" % (t, ratio or -1, total),
            plotdata[t].append(ratio)
        print

    pyplot.figure(figsize=(6, 3.5))
    pyplot.subplots_adjust(bottom=0.13)
    pyplot.plot(r[:-1], plotdata['dbf'], 'ko--', label='EDF',
        color="#880088", linewidth=2)
    pyplot.plot(r[:-1], plotdata['rf_iterative'], 'ks-', label='SP',
        color="#000088", linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "lower left")
    #pyplot.xlim(0, 1)
    pyplot.ylim(0, 1)
    pyplot.xlabel('Task Set Utilization')
    pyplot.ylabel('Acceptance Ratio')
    pyplot.show()



def plot_splittimes_over_U(X, r=None):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """

    ts=['rf_iterative', 'rfpaths']

    r = r or [i/100.0 for i in range(5, 110, 10)]

    rc('text', usetex=True)
    rc('font', family='serif')

    plotdata = dict([(t, list()) for t in ts])
    minslotsize = 10

    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            times = [x[t+"-time"] for x in X
                if ii(x['U'], j, step) and x[t+"-res"] is not None]
            total = len(times)
            avg_time = sum(times) / total if total >= minslotsize else None
            times.sort()
            med_time = times[total/2] if total >= minslotsize else None
            print "[%s: avg %.2f med %.2f in %d]" % (t, avg_time or -1, med_time or -1, total),
            plotdata[t].append(med_time)
        print


    width = 0.08

    pyplot.figure(figsize=(6, 4.2))
    pyplot.bar(r[:-1], plotdata['rf_iterative'], width=width, label='Combination Testing',
        color="#000088")

    pyplot.bar(r[:-1], plotdata['rfpaths'], width=0.08, label='Computing Request Functions',
        color="#44AA44")

    pyplot.grid(True)
    pyplot.legend(loc = "upper left")
#    pyplot.xticks([i+width/2. for i in r[:-1]], ["%d%%" % ((r[i]+r[i+1])*50) for i in range(len(r[:-1]))])
    pyplot.xticks([i+width/2. for i in r[:-1]], ["%d\\%%" % i for i in range(10, 100, 10)])
    pyplot.xlim(width-0.05, 1-0.05)
    pyplot.ylim(0, 1.3)
    pyplot.xlabel('Task Set Utilization')
    pyplot.ylabel('Run-Time (seconds)')
    pyplot.show()



def plot_stats_combi(X):
    """
    X: list of triples (outcome, tested, total)

    outcome == True means EDF
    outcome == False means SP
    """

    rc('text', usetex=True)
    rc('font', family='serif')

    width = 0.08

    pyplot.figure(figsize=(6, 3.0))
    pyplot.subplots_adjust(bottom=0.16)
    pyplot.scatter([x[2] for x in X if x[0]], [x[1] for x in X if x[0]], s=10,
        label='EDF', color="#880000")

    pyplot.scatter([x[2] for x in X if not x[0]], [x[1] for x in X if not x[0]], s=20,
        label='SP', color="#000088", marker='x')

    pyplot.grid(True)
    pyplot.legend(loc = "upper left")
#    pyplot.xticks([i+width/2. for i in r[:-1]], ["%d%%" % ((r[i]+r[i+1])*50) for i in range(len(r[:-1]))])
#    pyplot.xticks([i+width/2. for i in r[:-1]], ["%d\\%%" % i for i in range(10, 100, 10)])
    pyplot.xlim(0.5, 10**12)
    pyplot.ylim(0.5, 3*10**3)
    pyplot.xscale('log')
    pyplot.yscale('log')
#    pyplot.xlim(width-0.05, 1-0.05)
#    pyplot.ylim(0, 3)
    pyplot.xlabel('Total Combinations')
    pyplot.ylabel('Tested Combinations')
    pyplot.show()


def plot_precision(A, B):
    """
    A and B: Triple of (x, y, l) with
      x: number of improvements
      y: total number
      l: list of improvements with pairs (first estimation, precise rt)

    A is for "minimal improvement"
    B is for "a lot of improvement"
    """

    X = []
    Y = []
    for (newlist, oldlist) in [(X, A), (Y, B)]:
        newlist.extend([(1.0 * i/j,
            sum((1.0 * (x - y) / x) for (x, y) in l)/len(l) if len(l) > 0 else 0)
            for (i, j, l) in oldlist])

    rc('text', usetex=True)
    rc('font', family='serif')

    width = 0.08

    pyplot.figure(figsize=(5, 3))
    pyplot.subplots_adjust(bottom=0.16, left=0.14)
    pyplot.scatter([x[0] for x in X], [x[1] for x in X], s=20,
        label='Type A', color="#008800", marker='x')

    pyplot.scatter([x[0] for x in Y], [x[1] for x in Y], s=10,
        label='Type B', color="#880088")

    pyplot.grid(True)
    pyplot.legend(loc = "upper left")
    pyplot.xticks([i/100.0 for i in range(0, 101, 20)],
        ["%d\\%%" % i for i in range(0, 101, 20)])
    pyplot.yticks([i/100.0 for i in range(5, 21, 5)],
        ["%d\\%%" % i for i in range(5, 21, 5)])
    pyplot.xlim(0.0, 1.0)
    pyplot.ylim(0.0, 0.2)
    pyplot.xlabel('Fraction of improved RT estimates')
    pyplot.ylabel('Average improvement')
    pyplot.show()





# This is how the experiment figures were made.
#
# Make sure to import task, examples, stats, debug, cPickle.
#
# ########################################################################
#
# First, data creation:
#
# X.pickle
# ********
# Result of running the following:
#
# stats.acceptance_experiment(U_range=[i/100.0 for i in range(102)], T_gen = stats.T_gen_X5, repeats=3)
#
# Comments:
# * T_gen_X5 creates task sets with the parameters mentioned in the paper.
# * The function runs the task sets through the test and measures time.
# * 3 times, fastest wins.
# * Types:
#   - dbf: Just EDF schedulability from RTAS11 paper
#   - rf_iterative: Full abstraction refinement procedure
#   - rfpaths: Compute only rf paths and return true. This is a hack in order
#       to measure the rf path computation time.
# * In order to speed up, run 3 of these in parallel over night. (On the same
#   machine in order to get comparable times.)
#
# X_stats_combi.pickle:
# *********************
# Run the following:
#
# stats.acceptance_experiment(U_range=[i/100.0 for i in range(10, 110, 10)], exp_types=['rf_iterative'], T_gen = stats.T_gen_X5, repeats=1)

#stats.acceptance_experiment(U_range=[i/100.0 for i in range(10, 110, 10)], exp_types=['rbf-go','rbf-go-m'], T_gen = stats.T_gen_X5, repeats=1)
#
# After that, task.xx_stats_combi contains tons of tuples as described below
# for Y. They are captured during rf_iterative runs.
# Save the first 10**5 of those.
#
#
# ########################################################################
#
# Second, figure creation:
#
# Make sure to have pyplot installed. The functions create a plot
# which then needs to be manually saved by clicking on the save
# button and choosing a filename.
#
# fig-runtime-over-U.pdf
# **********************{
# with open("X.pickle") as f:
#     X = cPickle.load(f)
# stats.plot_runtime_over_U([x for x in X if x['U'] < 1.0], r=[i/100.0 for i in range(1, 101, 3)])
##}
# Comments:
# * Plots runtimes over task set utilization.
# * Cut off at 1.0 because EDF runtimes are theoretically infinite there
#
#
# fig-splittimes-over-U.pdf
# *************************
# with open("X.pickle") as f:
#     X = cPickle.load(f)
# stats.plot_splittimes_over_U([x for x in X if 'rfpaths-time' in x and x['U'] < 1.0])
#
# Comments:
# * Plots times split into rf computation and combination testing over U.
# * Cut off at 100% because only those were shown in previous figure.
# * (It's not necessarily faster to first compute U, so the times still make sense.)
#
#
# fig-ratio-over-U.pdf
# ********************
# with open("X.pickle") as f:
#     X = cPickle.load(f)
# stats.plot_ratio_over_U([x for x in X if x['U'] < 1.0], r=[i/100.0 for i in range(1, 110, 3)])
#
# Comments:
# * ...
#
#
# fig-stats-combi.pdf
# *******************
# with open("X_stats_combi.pickle") as f:
#     X = cPickle.load(f)
# Y0a = [(True, 1, 1, 0, 1)] * 100
# Y0b = [(False, 1, 1, 1, 0)] * 100
# Y1 = [y for y in Y if y[2] < 10**12 and y[3]*y[4] > 0 and not y[1]*y[2] == 1]
# Y2 = [y for y in Y if y[2] < 10**12 and y[3]*y[4] == 0 and not y[1]*y[2] == 1]
# stats.plot_stats_combi(Y0a + Y0b + Y1 + Y2[:5000])
#
# Comments:
# * Y contains tuples (schedulable, comb_tested, comb_total, pos, neg)
# * Coordinates in the plot are (comb_total, comb_tested)
# * Y0 are a few dots at (1, 1) representing about 50% of all tests which were
#   trivial, i.e., only had exactly one rf per task. PDF just gets too big if
#   we print thousands of symbols on top of each other.
# * Y1 are all non-trivial tests which had both positive and negative
#   subtest outcomes. These are the interesting ones, about 1%
# * Y2 are all non-trivial tests which were one-sided, i.e., were only negative
#   (log-"cloud" of red dots) or positive (early termination with just one
#   tested combination of mrf).
# * Limit Y2 in plot since this just leads to overly dense clouds otherwise.



#######################################
#
### RTAS14 Precision figure:
#
## Experiment
#
# for j in range(1000):
#    TS = task.TaskSet([stats.T_gen_X7(tid=i) for i in range(10)])
#    TS.rta_edf()
#    A.append((task.xx_stats_rt_improved, task.xx_stats_rt_total, task.xx_stats_rt_improvements))
#    (task.xx_stats_rt_improved, task.xx_stats_rt_total, task.xx_stats_rt_improvements) = (0, 0, [])
#
# for j in range(1000):
#    TS = task.TaskSet([stats.T_gen_X7(tid=i) for i in range(10)])
#    TS.rta_edf()
#    B.append((task.xx_stats_rt_improved, task.xx_stats_rt_total, task.xx_stats_rt_improvements))
#    (task.xx_stats_rt_improved, task.xx_stats_rt_total, task.xx_stats_rt_improvements) = (0, 0, [])
#
## Or, load from file:
#
# with open("X_precision_monk_A.pickle") as fd:
#    A.extend(cPickle.load(fd))
#
# with open("X_precision_monk_B.pickle") as fd:
#    B.extend(cPickle.load(fd))
#
## Plot:
#
# stats.plot_precision(A[:350], B)
#
####################################
#
### RTAS14 Runtime figure(s)
#
## Experiment
#
# X2_worx += stats.rta_experiment(len_range=range(1,21), repeats=2)
#
## Alternatively, load from file:
#
# with open("X2_worx.pickle", "r") as fd:
#    X2.extend(cPickle.load(fd))
#
## Plot:
#
# stats.plot_runtime_over_U(X2, r=[i/100.0 for i in range(1, 101, 5)], t="rta-fp")
#
# stats.plot_runtime_over_U([x for x in X2 if x["rta-edf-time"] < 100] , r=[i/100.0 for i in range(1, 101, 5)], t="rta-edf")
#
####################################
#
### RTAS14 Combinations figure
#
## Created by saving stats.xx_stats_combi into a file after above experiment.
#
## Alternatively, load from file:
#
# with open("X2_combi_worx.pickle", "r") as fd:
#    X2_combi.extend(cPickle.load(fd))
#
## Plot:
#
# Y0 = [(True, 1, 1) for i in range(100)] + [(False, 1, 1) for i in range(100)]
# Y1 = [(True, x[2], x[3]) for x in X2_combi if x[0]=="EDF-RT" and x[2] > 1]
# Y2 = [(False, x[2], x[3]) for x in X2_combi if x[0]=="FP-RT" and x[2] > 1]
#
# stats.plot_stats_combi(Y1[:5000]+Y2[:5000]+Y0)
#

if __name__ == '__main__':
    print 'hello drt'

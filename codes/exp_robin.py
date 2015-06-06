import stats
import debug
import random
import examples


# X_stats_combi.pickle:
# *********************
# Run the following:
#
# stats.acceptance_experiment(U_range=[i/100.0 for i in range(10, 110, 10)], exp_types=['rf_iterative'], T_gen = stats.T_gen_X5, repeats=1)
#debug.set_group_level(6,2)
#stats.acceptance_experiment_robin(U_range=[i/100.0 for i in range(35, 45, 10)], exp_types=['rbf-go','rbf-go-m'], T_gen = stats.T_gen_Robin, repeats=1)
#stats.acceptance_experiment_robin(U_range=[i/100.0 for i in range(35, 45, 10)], exp_types=['rf-go','rf-go-m'], T_gen = stats.T_gen_Robin, repeats=1)
#stats.acceptance_experiment(U_range=[i/100.0 for i in range(10, 110, 10)], exp_types=['rbf-go','rbf-go-m'], T_gen = stats.T_gen_X5, repeats=1)
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

gg_tg_type='1'

def TG_Robin(t = None, tid = 0):
    """@todo: Docstring for T_gen_Robin.

    :t: @todo
    :tid: @todo
    :returns: @todo

    """
    if t is None:
        HML = ['H', 'M', 'L']
        t = HML[random.randint(0, 2)]
        global gg_tg_type
        t = gg_tg_type if gg_tg_type is not None else t
    if t == 'H':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=50, p_max=300,
                        e_min=1, e_max=8,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(H)"%tid)
    elif t == 'M':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=4,
                        p_min=50, p_max=300,
                        e_min=1, e_max=6,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(M)"%tid)
    elif t == 'L':
        return examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=3,
                        p_min=50, p_max=300,
                        e_min=1, e_max=4,
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
        return examples.RandomTask(size_min=6, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=50, p_max=300,
                        e_min=1, e_max=7,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                        name="T%d(L)"%tid)
    pass

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        switch = sys.argv[1]
    else:
        switch = 'mixed'

    print 'switch=' + switch

    ss = switch.split(':')
    switch = ss[0]

    global gg_tg_type
    gg_tg_type = '1' if len(ss)<1 else ss[1]

    import task
    try:
        lvls = int(sys.argv[2])
    except:
        lvls =3
    print 'OPT levels = ', lvls, ' ; random task type = ', gg_tg_type
    stats.gg_total_lvls = lvls ## [Robin] Default Value, little benifits of lvl4
    if switch == 'mixed':
        res = stats.acceptance_experiment_robin_mixed(
                U_range=[i/100.0 for i in range(28, 68, 3)], T_gen = TG_Robin, repeats=1, sort_ts=True)
    elif switch == 'opa':
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(28, 68, 3)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=False)
    elif switch == 'fix':
        stats.gg_skip_bad = False
        stats.gg_loop_once = True
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(20, 68, 3)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=False, given_order=True)
    elif switch == 'mdm':
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(28, 68, 3)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=True, given_order=True)

    elif switch == '1':
        ## [Robin] 894, 2395, 37%, 7154, 67%
        ## happy=7422, failed=24052, ratio =0.31, total=50098, ok = 0.52
#======== happy=5071, sad=0, failed=13620, bad=0, ratio =0.37, total=28211, ok = 0.52
#******** lvl_0= 942(0.19); lvl_1= 2876(0.57), lvl_2= 1253(0.25), total=5071
#======== happy=4423, sad=0, failed=11737, bad=0, ratio =0.38, total=24432, ok = 0.52
#******** lvl_0= 749(0.17); lvl_1= 2540(0.57); lvl_2= 1134(0.26); lvl_3= 0(0.00); total= 4423
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(35, 45, 5)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=False)
    elif switch == '2':
        ## [Robin] 1458, 2815, 52%, 15815, 82%
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(35, 45, 10)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=False)
        ## [Robin]
    elif switch == '21':
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(35, 49, 5)], exp_types=['rf-go','rf-go-m'],
                #T_gen = stats.T_gen_X3, repeats=1, sort_ts=False)
                T_gen = TG_Robin, repeats=1, sort_ts=False)
    elif switch == '3':
        ## [Robin] 2684, 4715, 57%, 21503, 78%
        ##happy=1780, sad=0, failed=3298, bad=9, ratio =0.54, total=10158, ok = 0.68
        ##happy=1780, sad=0, failed=3298, bad=9, ratio =0.54, total=10158, ok = 0.68
#======== happy=7470, sad=0, failed=13692, bad=32, ratio =0.55, total=41980, ok = 0.67
#******** lvl_0=1537, (0.21); lvl_1=5337, (0.71), lvl_2=596, (0.08), total=7470
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(35, 45, 10)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=True, given_order=True)
    elif switch == '31':
        task.gg_dummy = False
        ## [Robin] 1278, 2999, 43%, 7958, 62%
        ## 2505,6535,38%,12799,49%
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(35, 45, 5)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=True,given_order=True)
    elif switch == '32':
        task.gg_dummy = True
        ## [Robin] 1278, 2999, 43%, 7958, 62%
        ## 2343,6647,35%,12931,49%
        res = stats.acceptance_experiment_robin(
                U_range=[i/100.0 for i in range(35, 45, 5)], exp_types=['rf-go','rf-go-m'],
                T_gen = TG_Robin, repeats=1, sort_ts=True,given_order=True)
    else:
        print 'unknown switch !!!'

    print 'Parameters: ', sys.argv

    if (sys.argv>4):
        with open(sys.argv[3],'w') as f:
            import cPickle
            #cPickle.dump('Parameters: '+ sys.argv)
            cPickle.dump(res,f)

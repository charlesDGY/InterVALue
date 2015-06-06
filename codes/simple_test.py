import examples
from etask import ETask

for i in range (10):
    T = examples.RandomTask(size_min=7, size_max=15,
                        fanout_min=1, fanout_max=5,
                        p_min=50, p_max=300,
                        e_min=1, e_max=8,
                        d_min=300, d_max=300,
                        #d_min=100, d_max=400,
                        d_implicit=True,
                            name="T%d(H)"%i)
    print T
    ## do some experiments based on the Task T
# T.render('et.pdf') # need PyGraphViz ~

from matplotlib import pyplot
from matplotlib import rc

def plot_time_overhead_results(X, r=range(100),only_cmp=True,of=None,ys=[ ['rf-go:k:fix','rf-go-m:fix'], ['rf-go:opa','rf-go-m:opa'],['rf-go','rf-go-m']]):
    global gg_range

    r=gg_range

    rc('xtick.major',width=1,size=5)
    rc('ytick.major',width=1,size=5)
    rc('grid',color='gray',linestyle=':',linewidth=0.7,alpha=0.9)
    #rc('ytick',direction='out')
    rc('text', usetex=True)
    rc('font', family='serif')

    def tc(r,g,b):
        return '#%02X%02X%02X' % (r,g,b)

    plotdata = X
    r = [x/100.0 for x in r]
    pyplot.figure(figsize=(5, 4))
    #pyplot.subplots_adjust(bottom=0.13)
    pyplot.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.99)

    mm = [m*0.8 if m is not None else None for m in plotdata['rf-go-m']]
    pyplot.plot(r[:-1], mm, 'ks-', label='With transforming',
            color="#FF420E", linewidth=2)
    pyplot.plot(r[:-1], plotdata['rf-go'], 'ko--', label='Without transforming',
        color="#80007B", linewidth=2)
    #pyplot.plot(r[:-1], plotdata['rf-go'], 'ko--', label='Without transforming',
        #color="#80007B", linewidth=2)
    #pyplot.plot(r[:-1], plotdata['rf-go-m'], 'ks-', label='With trasforming',
            #color="#000088", linewidth=2)
    #~ pyplot.plot(r[:-1],plotdata['rf-go-m'], 'k^:', label='shaping-overhead',
                #~ color='#FF420E',linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,
            shadow=False,handlelength=3,fancybox=False,frameon=True,ncol=1,numpoints=1,borderaxespad=1)
    #pyplot.legend(loc = "best" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.yticks(range(0, 101, 20), ['%d' % d for d in range(0, 101, 20)])
    pyplot.xlim(0.2, 0.8)
    #pyplot.ylim(-0.02, 1.02)
    #pyplot.ylim(-2, 102)
    #pyplot.ylim(-2,72)
    pyplot.xlabel('Task set utilization', fontsize=12)
    pyplot.ylabel('Average measured time overhead (second)', fontsize=12)
    #pyplot.show()
    if of is None:
        pyplot.show()
    else:
        #print( "hhhh" , file)

        #with open (of+'.pickleRes', 'w') as ff:
            #cPickle.dump(plotdata,ff)
        pyplot.savefig(of,format='pdf')
        #pyplot.show()
        #exit(0)

    pass

def plot_improvement_results(X, r=range(100),only_cmp=True,of=None,ys=[ ['rf-go:k:fix','rf-go-m:fix'], ['rf-go:opa','rf-go-m:opa'],['rf-go','rf-go-m']]):
    global gg_range

    r=gg_range

    rc('xtick.major',width=1,size=5)
    rc('ytick.major',width=1,size=5)
    rc('grid',color='gray',linestyle=':',linewidth=0.7,alpha=0.9)
    #rc('ytick',direction='out')
    rc('text', usetex=True)
    rc('font', family='serif')

    def tc(r,g,b):
        return '#%02X%02X%02X' % (r,g,b)

    plotdata = X

    r = [x/100.0 for x in r]
    pyplot.figure(figsize=(5, 4))
    #pyplot.subplots_adjust(bottom=0.13)
    pyplot.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.99)


    if plotdata.has_key('rf-go-cmp'):
        pyplot.plot(r[:-1], plotdata['rf-go-cmp'], 'ks-', label='Improvement',
                color="#FF420E", linewidth=1.5)
    if plotdata.has_key('imp_Lrf-go-cmp'):
        pyplot.plot(r[:-1], plotdata['imp_Lrf-go-cmp'], 'ks-', label='Light task',
                color="#FF420E", linewidth=1.5)
    if plotdata.has_key('imp_Mrf-go-cmp'):
        pyplot.plot(r[:-1], plotdata['imp_Mrf-go-cmp'], 'ko--', label='Medium task',
                color="#80007B", linewidth=1.5)
    if plotdata.has_key('imp_Hrf-go-cmp'):
        pyplot.plot(r[:-1], plotdata['imp_Hrf-go-cmp'], 'k^:', label='Heavy task',
                color="#0D8461", linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,
            shadow=False,handlelength=3,fancybox=False,frameon=True,ncol=1,numpoints=1,borderaxespad=1)
    #pyplot.legend(loc = "best" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.yticks(range(0, 101, 20), ['%d' % d for d in range(0, 101, 20)])
    #~ pyplot.xlim(0.28, 0.62)
    pyplot.xlim(0.2, 0.8)
    #pyplot.ylim(-0.02, 1.02)
    pyplot.ylim(-2, 102)
    #pyplot.ylim(-2,72)
    pyplot.xlabel('Task set utilization', fontsize=12)
    pyplot.ylabel('Improvement ratio $\\alpha$ (\%)', fontsize=12)
    #pyplot.show()
    if of is None:
        pyplot.show()
    else:
        #print( "hhhh" , file)

        #with open (of+'.pickleRes', 'w') as ff:
            #cPickle.dump(plotdata,ff)
        pyplot.savefig(of,format='pdf')
        #pyplot.show()
        #exit(0)

    pass

def plot_time_overhead(X, r=range(100),only_cmp=True,of=None,ys=[ ['rf-go:k:fix','rf-go-m:fix'], ['rf-go:opa','rf-go-m:opa'],['rf-go','rf-go-m']]):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """
    def ff(val, low, step=1):
        return val >= (low-step*0.5)/100 and val < (low+step*0.5)/100
        #return val >= low*1.0/100 and val < (low+step)*1.0/100

    ts=['rf-go', 'rf-go-m']
    yss = [ts]
    if ys is not None:
        ts = []
        yss = ys
        for xx in ys:
            ts += xx
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
    #~ X = [x for x in X if not x['rf-go-m-res']]
    for x in X:
        if x.has_key('rf-go-res') and x.has_key('rf-go-m-res'): x['rf-go-m-res'] = x['rf-go-res'] or x['rf-go-m-res']
    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            res = [x[t+"-time"] for x in X
                if ff(x['U'], j, step) and x.has_key(t+"-time") and x[t+"-time"] is not None]
            total = len(res)
            #ratio = 1.0 * sum(res) / total if total >= minslotsize else None
            ratio =  sum(res)*1.0 / total if total >= minslotsize else None
            print "[%s: ratio %.2f in %d]" % (t, ratio or 0, total),
            plotdata[t].append(ratio)
        print

    for (x,y) in yss:
        z=x+'-cmp'
        zz=x+'-efficiency'
        #zm=x+'-eff'
        plotdata[z]=[]
        plotdata[zz]=[]
        #plotdata[zm]=[]
        for i, j in enumerate(r[:-1]):
            try:
                plotdata[zz].append(plotdata[y][i]-plotdata[x][i])
            except:
                plotdata[zz].append(None)
                #raise

    print plotdata[z]
    r = [x/100.0 for x in r]
    pyplot.figure(figsize=(5, 4))
    #pyplot.subplots_adjust(bottom=0.13)
    pyplot.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.99)

    pyplot.plot(r[:-1], plotdata['rf-go'], 'ko--', label='Without transforming',
        color="#80007B", linewidth=2)
    pyplot.plot(r[:-1], plotdata['rf-go-m'], 'ks-', label='With transforming',
            color="#80007B", linewidth=2)
    #pyplot.plot(r[:-1],plotdata['rf-go-efficiency'], 'k^:', label='shaping-overhead',
                #color='#FF420E',linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,
            shadow=False,handlelength=3,fancybox=False,frameon=True,ncol=1,numpoints=1,borderaxespad=1)
    #pyplot.legend(loc = "best" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.yticks(range(0, 101, 20), ['%d' % d for d in range(0, 101, 20)])
    pyplot.xlim(0.2, 0.8)
    #pyplot.ylim(-0.02, 1.02)
    #pyplot.ylim(-2, 102)
    #pyplot.ylim(-2,72)
    pyplot.xlabel('Task set utilization', fontsize=12)
    pyplot.ylabel('Average measured time overhead (second)', fontsize=12)
    #pyplot.show()
    if of is None:
        pyplot.show()
    else:
        #print( "hhhh" , file)

        with open (of+'.pickleRes', 'w') as ff:
            cPickle.dump(plotdata,ff)
        pyplot.savefig(of,format='pdf')
        #pyplot.show()
        #exit(0)

def plot_improved_ratio_over(X, r=range(100),only_cmp=True,of=None,ys=[ ['rf-go:k:fix','rf-go-m:fix'], ['rf-go:opa','rf-go-m:opa'],['rf-go','rf-go-m']]):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """
    def ff(val, low, step=1):
        return val >= (low-step*0.5)/100 and val < (low+step*0.5)/100
        #return val >= low*1.0/100 and val < (low+step)*1.0/100

    ts=['rf-go', 'rf-go-m']
    yss = [ts]
    if ys is not None:
        ts = []
        yss = ys
        for xx in ys:
            ts += xx
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
    for x in X:
        if x.has_key('rf-go-res') and x.has_key('rf-go-m-res'): x['rf-go-m-res'] = x['rf-go-res'] or x['rf-go-m-res']

    for i, j in enumerate(r[:-1]):
        print "%s:" % j,
        for t in ts:
            step = r[i+1] - r[i]
            res = [x[t+"-res"] for x in X
                if ff(x['U'], j, step) and x.has_key(t+"-res") and x[t+"-res"] is not None]
            total = len(res)
            #ratio = 1.0 * sum(res) / total if total >= minslotsize else None
            ratio = 100.0 * sum(res) / total if total >= minslotsize else 0 ##None
            print "[%s: ratio %.2f in %d]" % (t, ratio or 0, total),
            plotdata[t].append(ratio)
        print

    for (x,y) in yss:
        z=x+'-cmp'
        zz=x+'-efficiency'
        zm=x+'-eff'
        plotdata[z]=[]
        plotdata[zz]=[]
        plotdata[zm]=[]
        for i, j in enumerate(r[:-1]):
            try:
                step = r[i+1] - r[i]
                resx = [(xx[y+"-time"] - xx[x+"-time"])/xx[y+"-time"] for xx in X
                    if ff(xx['U'], j, step) and xx.has_key(x+"-time") and xx[x+"-time"] is not None]

                plotdata[zz].append(100.0 * sum(resx)/len(resx))
                plotdata[zm].append(100.0 * max(resx))
            except:
                plotdata[zz].append(None)
                plotdata[zm].append(None)
            try:

                #ratio = 1.0 * sum(res) / total if total >= minslotsize else None
                ratio = 100.0 * sum(res) / total if total >= minslotsize else None
                faild = 100 - plotdata[x][i]
                happy = plotdata[y][i]-plotdata[x][i]
                #ratio = 100.0*happy / plotdata[x][i] if plotdata[x][i]>0 else None
                ratio = 100.0*happy / plotdata[y][i] if plotdata[y][i]>0 else None
                #ratio = 100.0*happy/faild if faild>0 else None

                plotdata[z].append(ratio)
            except:
                plotdata[z].append(None)
                #raise

    print plotdata[z]
    r = [x/100.0 for x in r]
    pyplot.figure(figsize=(5, 4))
    #pyplot.subplots_adjust(bottom=0.13)
    pyplot.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.99)
    if ys is not None:
        if not only_cmp and plotdata.has_key('shaping-full'):
            pyplot.plot(r[:-1], plotdata['shaping-full'], '*-', label='shaping-Full',
                color="#CE191E", linewidth=1.5)
        if not only_cmp and plotdata.has_key('rf-go-m:fix'):
            pyplot.plot(r[:-1], plotdata['rf-go-m:fix'], 'ko-', label='shaping-MDM',
                color="#0D8461", linewidth=1.5)
                #color="#FED521", linewidth=1.5)
        if not only_cmp and plotdata.has_key('rf-go:k:fix'):
            pyplot.plot(r[:-1], plotdata['rf-go:k:fix'], 'ko--', label='refinement-MDM',
                color="#0D8461", linewidth=1.5)
        if plotdata.has_key('rf-go:k:fix-cmp'):
            pyplot.plot(r[:-1], plotdata['rf-go:k:fix-cmp'], 'ko:', label='improved-MDM',
                color="#0D8461", linewidth=1.5)
        if not only_cmp and plotdata.has_key('rf-go-m:opa'):
            pyplot.plot(r[:-1], plotdata['rf-go-m:opa'], 'ks-', label='shaping-OPA',
            color="#80007B", linewidth=1.5)
            #color="#315BA7", linewidth=1.5)
        if not only_cmp and plotdata.has_key('rf-go:opa'):
            pyplot.plot(r[:-1], plotdata['rf-go:opa'], 'ks--', label='refinement-OPA',
            color="#80007B", linewidth=1.5)
        if plotdata.has_key('rf-go:opa-cmp'):
            pyplot.plot(r[:-1], plotdata['rf-go:opa-cmp'], 'ks:', label='improved-OPA',
            color="#80007B", linewidth=1.5)
        if not only_cmp and plotdata.has_key('rf-go'):
            pyplot.plot(r[:-1], plotdata['rf-go'], 'k^--', label='refinement-Fixed',
                color="#FF420E", linewidth=1.5)
        if not only_cmp and plotdata.has_key('rf-go-m'):
            pyplot.plot(r[:-1], plotdata['rf-go-m'], 'kv-', label='shaping-Fixed',
                color="#FF420E", linewidth=1.5)
        if plotdata.has_key('rf-go-cmp'):
            pyplot.plot(r[:-1], plotdata['rf-go-cmp'], 'kv:', label='improved-Fixed',
                color="#FF420E", linewidth=1.5)
        if False and plotdata.has_key('rf-go-efficiency'):
            pyplot.plot(r[:-1], plotdata['rf-go-efficiency'], 'ks-', label='efficiency-Fixed',
                color="#FF420E", linewidth=1.5)
        if False and plotdata.has_key('rf-go-eff'):
            pyplot.plot(r[:-1], plotdata['rf-go-eff'], 'ks--', label='eff-Fixed',
                color="#80007B", linewidth=1.5)
            #print n,t
            #print plotdata[n]
            #pyplot(r[:-1], plotdata[n], 'ko--', label=t, color='"#880088', linewidth=2)
    else:
        pyplot.plot(r[:-1], plotdata['rf-go'], 'ko--', label='refinement',
            color="#880088", linewidth=2)
        pyplot.plot(r[:-1], plotdata['rf-go-m'], 'ks-', label='shaping',
            color="#000088", linewidth=2)
        pyplot.plot(r[:-1],plotdata['rf-go-cmp'], 'k^:', label='improved',
                color='#FF420E',linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,
            shadow=False,handlelength=3,fancybox=False,frameon=True,ncol=1,numpoints=1,borderaxespad=1)
    #pyplot.legend(loc = "best" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.legend(loc = "upper left" if only_cmp else  "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    #pyplot.yticks(range(0, 101, 20), ['%d' % d for d in range(0, 101, 20)])
    #~ pyplot.xlim(0.28, 0.62)
    pyplot.xlim(0.2, 0.8)
    #pyplot.ylim(-0.02, 1.02)
    pyplot.ylim(-2, 102)
    #pyplot.ylim(-2,72)
    pyplot.xlabel('Task set utilization', fontsize=12)
    pyplot.ylabel('Improvement ratio (N-o)/N(\%)', fontsize=12)
    #pyplot.show()
    if of is None:
        pyplot.show()
    else:
        #print( "hhhh" , file)

        with open (of+'.pickleRes', 'w') as ff:
            cPickle.dump(plotdata,ff)
        pyplot.savefig(of,format='pdf')
        #pyplot.show()
        #exit(0)


global gg_range

def plot_ratio_over_U_Robin_Mixed(X, r=range(100),of=None,ys=[ ['rf-go:k:fix','refinement-MDM'],['rf-go-m:fix','shaping-MDM'], ['rf-go:opa','refinement-OPA'], ['rf-go-m:opa','shaping-OPA']]):
    """
    X: list of dictionaries, i.e., experiment results

    Optional:
    r: range to be displayed, defaults to range(100)
    """
    def ff(val, low, step=1):
        return val >= (low-step*0.5)/100 and val < (low+step*0.5)/100
        #return val >= low*1.0/100 and val < (low+step)*1.0/100

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
                if ff(x['U'], j, step) and x.has_key(t+"-res") and x[t+"-res"] is not None]
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
        if plotdata.has_key('shaping-full'):
            pyplot.plot(r[:-1], plotdata['shaping-full'], '*-', label='shaping-Full',
                color="#CE191E", linewidth=1.5)
        if plotdata.has_key('rf-go-m:fix'):
            pyplot.plot(r[:-1], plotdata['rf-go-m:fix'], 'ko-', label='shaping-MDM',
                color="#0D8461", linewidth=1.5)
                #color="#FED521", linewidth=1.5)
        if plotdata.has_key('rf-go:k:fix'):
            pyplot.plot(r[:-1], plotdata['rf-go:k:fix'], 'ko--', label='refinement-MDM',
                color="#0D8461", linewidth=1.5)
        if plotdata.has_key('rf-go:k:fix-cmp'):
            pyplot.plot(r[:-1], plotdata['rf-go:k:fix-cmp'], 'ko:', label='refinement-MDM',
                color="#0D8461", linewidth=1.5)
        if plotdata.has_key('rf-go-m:opa'):
            pyplot.plot(r[:-1], plotdata['rf-go-m:opa'], 'ks-', label='shaping-OPA',
            color="#80007B", linewidth=1.5)
            #color="#315BA7", linewidth=1.5)
        if plotdata.has_key('rf-go:opa'):
            pyplot.plot(r[:-1], plotdata['rf-go:opa'], 'ks--', label='refinement-OPA',
            color="#80007B", linewidth=1.5)
        if plotdata.has_key('rf-go:opa-cmp'):
            pyplot.plot(r[:-1], plotdata['rf-go:opa-cmp'], 'ks:', label='refinement-OPA',
            color="#80007B", linewidth=1.5)
        if plotdata.has_key('rf-go'):
            pyplot.plot(r[:-1], plotdata['rf-go'], 'k^--', label='refinement-Fixed',
                color="#FF420E", linewidth=1.5)
        if plotdata.has_key('rf-go-m'):
            pyplot.plot(r[:-1], plotdata['rf-go-m'], 'kv-', label='shaping-Fixed',
                color="#FF420E", linewidth=1.5)
        if plotdata.has_key('rf-go-cmp'):
            pyplot.plot(r[:-1], plotdata['rf-go-cmp'], 'kv:', label='shaping-Fixed',
                color="#FF420E", linewidth=1.5)
            #print n,t
            #print plotdata[n]
            #pyplot(r[:-1], plotdata[n], 'ko--', label=t, color='"#880088', linewidth=2)
    else:
        pyplot.plot(r[:-1], plotdata['rf-go'], 'ko--', label='refinement',
            color="#880088", linewidth=2)
        pyplot.plot(r[:-1], plotdata['rf-go-m'], 'ks-', label='shaping',
            color="#000088", linewidth=2)

    pyplot.grid(True)
    pyplot.legend(loc = "lower left",title='', fontsize=12,shadow=False,handlelength=3,fancybox=False,frameon=False,ncol=1,numpoints=1,borderaxespad=0.4)
    pyplot.yticks(range(0, 101, 20), ['%d' % d for d in range(0, 101, 20)])
    pyplot.xlim(0.28, 0.62)
    #pyplot.ylim(-0.02, 1.02)
    pyplot.ylim(-2, 102)
    pyplot.xlabel('Task set utilization', fontsize=12)
    pyplot.ylabel('Acceptance ratio (\%)', fontsize=12)
    #pyplot.show()
    if of is None:
        pyplot.show()
    else:
        #print( "hhhh" , file)

        pyplot.savefig(of,format='pdf')
        #pyplot.show()
        #exit(0)


def f_plot_mixed(r,ur=[],of=None):
    if len(ur) > 0:
        plot_ratio_over_U_Robin_Mixed(r+ur,r=gg_range,of=of,ys=[ ['rf-go:k:fix','refinement-MDM'],['rf-go-m:fix','shaping-MDM'], ['rf-go:opa','refinement-OPA'], ['rf-go-m:opa','shaping-OPA'], ['rf-go','refinement-fixed'],['rf-go-m','shaping-fixed']])
    else:
        plot_ratio_over_U_Robin_Mixed(r+ur,r=gg_range,of=of)
#fig-runtime-over-U.pdf
#**********************{
def go5(bp="./output", R=True, FN=None,ob='../inc/',rm=False,plot=f_plot_mixed,ur=[]):
    print (bp)
    import os
    import cPickle
    fs = os.listdir(bp)
    num = 0
    r = []
    for f in fs:
        path = os.path.join(bp, f)
        if os.path.isdir(path) and R and (FN is None or len(FN)>0):
            go5(path, R,FN,ob,rm,plot,ur)
        elif f.endswith(".pickle"):
            num += 1
            print 'loading... ' , path
            with open(path, 'r') as f:
                #[bins, trials, eMin, eMax, hiFact, hiProb, pMin, pMax] = cPickle.load(fs)
                #r.append(cPickle.load(fs))
                r += cPickle.load(f)
    if rm and len(r)>0:
        with open (bp+'/merge.pickleAll','w') as f:
            cPickle.dump(r,f)

    if plot and len(r)>0:
        if type(plot)!=list: plot=[plot]
        for pl in plot:
            ff = None
            if FN is not None and len(FN)>0:
                ff = ob + FN.pop(0)
            elif FN is not None:
                return
            print (ob,ff)
            pl(r,ur,ff)
def go(f='mixed1.pickle'):
    with open(f,'r') as f:
    #with open("xdd---.pickle",'r') as f:
        import cPickle
        import stats
        #s = cPickle.load(f)
        #print s
        X = cPickle.load(f)
        #print X
        stats.plot_ratio_over_U_Robin(X,r=range(20,70,2),ys=None)
        #plot_ratio_over_U_Robin_Mixed(X,r=range(20,66,2),ys=[ ['rf-go:k:fix','refinement-MDM'],['rf-go-m:fix','shaping-MDM'], ['rf-go:opa','refinement-OPA'], ['rf-go-m:opa','shaping-OPA']])
        #,ts=['rf-go','rf-go-m']
        #stats.plot_runtime_over_U([x for x in X if x['U'] < 1.0], r=[i/100.0 for i in range(35, 45, 10)])
        #stats.plot_runtime_over_U([x for x in X if x['U'] < 1.0], r=[i/100.0 for i in range(1, 101, 3)])


def f_plot_improved(r,ur=[],of=None):
    #plot_improved_ratio_over(r,r=range(20,70,2),ys=None,of=of)
    #plot_improved_ratio_over(r+ur,r=[x * 1.3333333333 for x in range (16,88)],of=of,only_cmp=True)
    plot_improved_ratio_over(r+ur,r=gg_range,of=of,only_cmp=True)
    #plot_improved_ratio_over(r,r=range(20,70,2),ys=None,of=of)

def f_plot_improved_fix(r,ur=[],of=None):
    #plot_improved_ratio_over(r,r=range(20,70,2),ys=None,of=of)
    #plot_improved_ratio_over(r+ur,r=[x * 1.3333333333 for x in range (16,88)],of=of,only_cmp=True)
    plot_improved_ratio_over(r+ur,r=gg_range,of=of,only_cmp=True,ys=[['rf-go','rf-go-m']])
    #plot_improved_ratio_over(r,r=range(20,70,2),ys=None,of=of)
def f_plot_time_overhead(r,ur=[],of=None):
    #plot_improved_ratio_over(r,r=range(20,70,2),ys=None,of=of)
    #plot_improved_ratio_over(r+ur,r=[x * 1.3333333333 for x in range (16,88)],of=of,only_cmp=True)
    plot_time_overhead(r+ur,r=gg_range,of=of,only_cmp=True,ys=[['rf-go','rf-go-m']])
    #plot_improved_ratio_over(r,r=range(20,70,2),ys=None,of=of)

def fusion(plot=[f_plot_mixed,f_plot_improved]):
    import cPickle
    #goFuck(FN=['mpvd-02.pdf','mpvd-04.pdf','mpvd-08.pdf','mpvd-16.pdf'])
    #go5()
    #go5(FN=['mixed3.pdf','mixed6.pdf'],ob='../inc/')
    rr = []
    go5(R=False,rm=True,plot=False,bp="./output/01f")
    with open('./output/01f/merge.pickleAll','r') as f:
        rr = cPickle.load(f)

    go5(bp='./output/01',FN=['ul6.pdf','cmp6.pdf'],ur=rr,plot=plot)
    #go5(FN=['ul3.pdf','ul6.pdf'],ur=rr,plot=plot)

def fusion2(plot=[f_plot_mixed,f_plot_improved]):
    import cPickle
    #goFuck(FN=['mpvd-02.pdf','mpvd-04.pdf','mpvd-08.pdf','mpvd-16.pdf'])
    #go5()
    #go5(FN=['mixed3.pdf','mixed6.pdf'],ob='../inc/')
    rr = []
    go5(R=False,rm=True,plot=False,bp="./output/fixed")
    with open('./output/fixed/merge.pickleAll','r') as f:
        rr = cPickle.load(f)

    go5(bp='./output/6',FN=['ul6.pdf','cmp6.pdf'],ur=rr,plot=plot)
    #go5(FN=['ul3.pdf','ul6.pdf'],ur=rr,plot=plot)

def improved_ratio():
    go5(bp='./output/01f',FN=['improved.pdf',],plot=f_plot_improved_fix)
    #go5(bp='./output/fixed3',FN=['improved.pdf',],plot=f_plot_improved_fix)

def plotlctes():

    #go5(bp='./output/fix-H',FN=['oh_H.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-H',FN=['imp_H.pdf',],plot=f_plot_improved_fix)

    #go5(bp='./output/fix-M',FN=['oh_M.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-M',FN=['imp_M.pdf',],plot=f_plot_improved_fix)

    #go5(bp='./output/fix-L',FN=['oh_L.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-L',FN=['imp_L.pdf',],plot=f_plot_improved_fix)

    #~ for (f) in ['oh_L','oh_M','oh_H']:
        #~ with open ('../inc/' + f + '.pdf.pickleRes', 'r') as ff:
            #~ x = cPickle.load(ff)
            #~ #for xx in x:
                #~ #x[xx] = [0 if yy is None else yy for yy in x[xx]]
            #~ plot_time_overhead_results(x,of='../inc/' + f + '.pdf')

    for f in ['imp_L','imp_M','imp_H']:
        with open ('../inc/' + f + '.pdf.pickleRes', 'r') as ff:
            x = cPickle.load(ff)
            for xx in x:
                x[xx] = [0 if yy is None else yy for yy in x[xx]]
            plot_improvement_results(x,of='../inc/' + f + '.pdf')

    pass
    
def plotlctes3():

    #go5(bp='./output/fix-H',FN=['oh_H.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-H',FN=['imp_H.pdf',],plot=f_plot_improved_fix)

    #go5(bp='./output/fix-M',FN=['oh_M.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-M',FN=['imp_M.pdf',],plot=f_plot_improved_fix)

    #go5(bp='./output/fix-L',FN=['oh_L.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-L',FN=['imp_L.pdf',],plot=f_plot_improved_fix)

    for f in ['oh_L','oh_M','oh_H']:
        with open ('../inc/' + f + '.pdf.pickleRes', 'r') as ff:
            x = cPickle.load(ff)
            #for xx in x:
                #x[xx] = [0 if yy is None else yy for yy in x[xx]]
            plot_time_overhead_results(x,of='../inc/' + f + '.pdf')

    pass
    
def plotlctes2():
    X={}
    for (f) in ['imp_L','imp_M','imp_H']:
        with open ('../inc/' + f + '.pdf.pickleRes', 'r') as ff:
            x = cPickle.load(ff)
            for xx in x:
                X[f+xx] = [0 if yy is None else yy for yy in x[xx]]
            
    plot_improvement_results(X,of='../inc/' + 'imp' + '.pdf')

    pass

if __name__ == '__main__':
    import time
    import cPickle
    t = time.time()

    global gg_range
    gg_range = [x * 2.75 for x in range (1,50)]
    #gg_range = [x * 2 for x in range (16,88)]
    #gg_range = range(20,100,4)

    #goFuck(FN=['mpvd-02.pdf','mpvd-04.pdf','mpvd-08.pdf','mpvd-16.pdf'])
    #go5()
    #go5(FN=['mixed3.pdf','mixed6.pdf'],ob='../inc/')
    #rr = []
    #with open('./output/fixed/merge.pickleAll','r') as f:
       #rr = cPickle.load(f)
    #plot_improved_ratio_over(rr,r=range(20,70,2),ys=None)
    #go5(FN=['ul3.pdf','ul6.pdf'],ur=rr)
    #go('fix31.pickle')
    #fusion2()
    #improved_ratio()
    #go5(bp='./output/fix00',FN=['improved.pdf','timeoverhead.pdf',],plot=[f_plot_improved_fix,f_plot_time_overhead])
    #go5(bp='./output/01f',FN=['improved.pdf','timeoverhead.pdf',],plot=[f_plot_improved_fix,f_plot_time_overhead])
    plotlctes3()
    #go5(bp='./output/fix-H',FN=['oh_H.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-H',FN=['imp_H.pdf',],plot=f_plot_improved_fix)

    #go5(bp='./output/fix-M',FN=['oh_M.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-M',FN=['imp_M.pdf',],plot=f_plot_improved_fix)

    #go5(bp='./output/fix-L',FN=['oh_L.pdf',],plot=f_plot_time_overhead)
    #go5(bp='./output/fix-L',FN=['imp_L.pdf',],plot=f_plot_improved_fix)
    #fusion(plot=f_plot_improved)
    #go5(FN=['mixed3.pdf','mixed6.pdf'],ob='../inc/')
    #~ improved_ratio()
    pyplot.show()
    print("time:", time.time() - t)

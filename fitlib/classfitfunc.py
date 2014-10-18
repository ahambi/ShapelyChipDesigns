from helpers import *

from matplotlib import pylab, mlab, pyplot
from matplotlib.pyplot import *
#from matplotlib.pyplot import axis, scatter
import numpy as np
from numpy import linspace, array, asarray, arange, sqrt
plt = pyplot

from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs

from pylab import gcf, gca

def get_peaks_position_height(xvals, noisyy, xlin=None, sval=1.0, peak_reject=0.5, 
                              minsearch=False, debug=False):
    ''' 
    xlin: the peaks sit on a baseline. To fit the baseline, give one or multiple ranges
        in which there is no peak, but a baseline, e.g.
        xlin = [-6.0,-2.0,
                8, 10]
        for a curve which is on the baseline between -6 and -2, and 8 and 10. 
    sval: can be used to additionally smoothen the curve. This is useful for very noisy data.
    peak_reject: percent below which a peak is rejected. 1: maximum deviation of the curve 
                    from the linear fit
    minsearch: set True if you search for minima instead for maxima
    '''
    resultx = []
    resulty = []
    
    LFit     = fitfunc(lin, r'$m \times x+b$')
    if debug:
        if len(xlin) == 2:
            i0, i1 = get_range_ind(xvals,xlin[0], xlin[1])
            gca().plot(xvals[i0:i1], noisyy[i0:i1], 'o', c='y', label='baseline fit')
    pf, ierr = LFit.fit([0,1],xvals,noisyy,xselect=xlin)
    #if debug: LFit.plot_result()
    
    minind, maxind = get_minmax_indices(xvals,noisyy,sval=sval,debug=debug)
    
    #if debug: plot(xvals[maxind], noisyy[maxind], 'o', label='max')
    #if debug: plot(xvals[minind], noisyy[minind], 'o', label='min')

    peaklimit = peak_reject*max(noisyy - lin(pf,xvals))
    if debug: print 'peaklimit:',peaklimit

    if minsearch: 
        for i in minind:
            if abs(noisyy[i]-lin(pf,xvals[i])) > peaklimit and noisyy[i]<lin(pf,xvals[i]):
                resultx += [xvals[i]]
                resulty += [noisyy[i]] 
        if debug: gca().plot(resultx, resulty, 'o', label='min')
            
    else:
        for i in maxind:
            if noisyy[i]-lin(pf,xvals[i]) > peaklimit:
                resultx += [xvals[i]]
                resulty += [noisyy[i]]
        if debug: gca().plot(resultx, resulty, 'o', label='max')
            
    return resultx, resulty


class fitfunc:
    ''' 
    initialize with 
    func = the fitfunction or a list of fitfunctions
    tex = Latex expression for the function or a list of them
    '''
    def __init__(self, func, tex='fit function'):
        
        # self.func
        
        if isinstance(func, list): self.func = func
        else: self.func = [func]
        
        # self.tex
        
        if not isinstance(tex, list): tex = [tex]
        
        if len(tex) == len(self.func): 
            self.tex = tex
        else: 
            print 'auto-tex! tex does not have the same length as func.'
            self.tex = [i for i in arange(len(self.func))]

    def errorfunc(self, pfit, x, y):
        ''' p: parameters of func
        x: x-values
        ydata: y-values to fit to '''
        
        pfit = list(pfit)
        
        if self.hold != None: 
            for i in self.hold:
                pfit.insert(i, self.p0[i])
        
        err = [0]*len(self.func)
        ERR = []
        for i, f in enumerate(self.func):
            err[i] = f(pfit, self.xfit[i]) - self.yfit[i]
            ERR += list(err[i])
            
        return array(ERR)
    
    def fit(self, p0, x, y, hold=None, xselect=None):
        '''
        p0: initial fit parameter guess
        xselect: select a range for the xparameter to fit, give [startvalue, endvalue]
        
        returns solp, ier 
        solp: found solution for the parameters 'p'
        ier: sqrt(abs(covariance matrix)) >> diagonal elements are the standard deviations of p
        self.hold: [hold this parameters onto the initial guesses]
        use func(solp, x) to plot the result
        '''
        
        self.p0      = p0
        self.xselect = xselect
        self.hold    = hold
        
        # x, y
        
        if not isinstance(x, list): x = [x]
        if not isinstance(y, list): y = [y]
            
        if len(x) == len(self.func): self.x = x
        else: print 'ERROR: len(x) != len(self.func)'
            
        if len(y) == len(self.func): self.y = y
        else: print 'ERROR: len(y) != len(self.func)'
        
        # hold, self.pfit
        
        if self.hold != None: 
            
            self.p0 = array(self.p0)
            if not isinstance(self.hold, list):
                self.hold = list(self.hold)
            
            self.pfit = list(self.p0)
            
            for index in sorted(self.hold, reverse=True):
                del self.pfit[index]
                
        else: 
            self.pfit = self.p0
            
        # xselect, self.xfit, self.yfit
        
        self.xfit = self.x
        self.yfit = self.y
        
        if xselect: 
            for i, xdata in enumerate(self.xfit):
                self.xfit[i], self.yfit[i] = get_new_xy(self.xfit[i], 
                                                        self.yfit[i],
                                                        xselect) 
                
        self.xfit = array(self.xfit)
        self.yfit = array(self.yfit)

        self.xdummy = []#self.xfit.flatten()
        self.ydummy = []#self.yfit.flatten()
        
        for i, xf in enumerate(self.xfit):
            self.xdummy += list(self.xfit[i])
            self.ydummy += list(self.yfit[i])
        
        solp = leastsq(self.errorfunc, 
                self.pfit, 
                args=(self.xdummy, self.ydummy),
                Dfun=None,
                full_output=True,
                ftol=1e-9,
                xtol=1e-9,
                maxfev=100000,
                epsfcn=1e-10,
                factor=0.1)
        
        solpf = list(solp[0])
        
        if solp[1] == None:
            ier = list([0 for i in arange(len(solpf))]) 
            print 'Jacobian is 0.0'
        else:
            ''' This is new! '''
            s_sq = (asarray(self.errorfunc(self.pfit, self.xdummy, self.ydummy))**2).sum() / (len(self.ydummy) - len(self.pfit))
            pcov = solp[1]
            pcov = pcov * s_sq
            ''' ...'''
            ier = list([sqrt(abs(pcov[i,i])) for i in arange(len(solpf))])
        

        
        if self.hold != None:
        
            for i in self.hold:
                solpf.insert(i, self.p0[i])
                ier.insert(i, 0.0)
        
        self.solp = solpf
        self.ier  = ier 
        
        #residual = self.errorfunc(self.pfit, xdummy, ydummy)
        #reduced_chi_square = (residual**2).sum()# / (len(ydata) - len(self.pfit))
        #print reduced_chi_square
        
        return self.solp, self.ier
    
    def chisquare(self):
        ''' returns chi, p '''
        
        self.chis = [chisquare(self.yfit[i], self.func[i](self.solp, self.xfit[i]),
                               ddof=len(self.yfit[i])-len(self.pfit)-1)[0] 
                                 for i in arange(len(self.xfit))]
        
        self.ps   = [chisquare(self.yfit[i], self.func[i](self.solp, self.xfit[i]),
                               ddof=len(self.yfit[i])-len(self.pfit)-1)[1] 
                                 for i in arange(len(self.xfit))]
        
        '''
        observed = []
        expected = []
        for i, xf in enumerate(self.xfit):
            expected += list(self.func[i](self.solp, self.xfit[i]))
            observed += list(self.yfit[i])

        else: 
            self.observed = observed
            self.expected = expected
            
            # remove expected = 0 occurences
            mincount = 0.5#abs(0.03 * max(self.expected))
            indices = [i for i, x in enumerate(self.expected) if abs(x) <= mincount]
            if len(indices): 
                print 'removed from observed, expected: ',indices
                print 'values below ',mincount,' were removed.'
                
            self.observed = array([item for i,item in enumerate(self.observed) if i not in indices])
            self.expected = array([item for i,item in enumerate(self.expected) if i not in indices])
            
            chi, p = chisquare(self.observed, self.expected,
                               ddof=len(observed)-len(self.func)*len(self.pfit)-1) 
        #print sum((self.errorfunc(self.pfit, self.xdummy, self.ydummy))**2/self.xdummy)'''
        return self.chis, self.ps
    
    def plot_result(self, TITLE='Fit', XLABEL='x-data', YLABEL='y-data', NPOINTS=100, header='auto', pnames='auto', digits=2, data_alpha=0.5, texttag=False, xlims=None, ylims=None):
        
        chi, p = self.chisquare()
        chitext = r'$\mathcal X^2=$'+", ".join([str(round(chi,1)) for chi in self.chis])+\
                    r', $pval=$'+", ".join([str(round(p,2)) for p in self.ps])
        
        if header == 'auto':
            header = ['parameter', r'$p0$', r'$p_{\rm fit} \pm \Delta $']
            
        if pnames == 'auto':
            pnames = ['p'+str(i) for i in arange(len(self.solp))]
            
        rows = []
        for i, pval in enumerate(self.solp):
            rows += [[pnames[i], round(self.p0[i], digits), str(round(self.solp[i],digits))+r'$\pm$'+str(round(self.ier[i],digits))]]

        ### the plot ###
        
        fig = gcf()
        
        F1 = fig.add_axes((.1,.22,.8,.75))
        
        
        if texttag: TextTag()
        
        # plot the data points
            
        colorcycle(len(self.x))
        
        for i, xvals in enumerate(self.x):
            c = gca()._get_lines.color_cycle.next()
            
            if i == 0: 
                scatter(self.x[i], self.y[i], s=30, alpha=data_alpha, label='data', color=c)
            else:
                scatter(self.x[i], self.y[i], s=30, alpha=data_alpha, color=c)
                
        # plot xselect
        
        if self.xselect:
            
            for i, xvals in enumerate(self.x):
                if i == 0:
                    scatter(self.xfit[i], self.yfit[i], s=30, c='yellow', label='fit points')
                else:
                    scatter(self.xfit[i], self.yfit[i], s=30, c='yellow')
               
        # plot a smooth curve of NPOINTS
        colorcycle(len(self.x))
        
        for i, xvals in enumerate(self.x):
            c = gca()._get_lines.color_cycle.next()
            xsmooth = linspace(self.x[i][0], self.x[i][-1], NPOINTS)
            F1.plot(xsmooth, self.func[i](self.solp, xsmooth),
                     color = c,
                     lw = 2,
                     label=self.tex[i])
        
        ## legend, table and titles 
        
        title(TITLE)
        ylabel(YLABEL)
        grid()
        
        lgd=legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=18)
        table = get_table(header, rows)
        t = text(1.05,0.5,table+'\n'+chitext,size=18,
             horizontalalignment='left',
             verticalalignment='top',
             transform=gca().transAxes)
        
        # FRAME 2
        
        from matplotlib.ticker import MaxNLocator
        gca().yaxis.set_major_locator(MaxNLocator(prune='lower')) #Removes lowest ytick label

        line = gca().get_lines()[0] 
        x0 = line.get_xdata().min()
        x1 = line.get_xdata().max() 
        
        if xlims == None: xlim(x0, x1)
        else: xlim(xlims[0], xlims[1])
        
        if ylims == None: pass
        else: ylim(ylims[0], ylims[1])

        F2 =fig.add_axes((.1,.0,.8,.15))
        
        if xlims == None: xlim(x0, x1)
        else: xlim(xlims[0], xlims[1])

        colorcycle(len(self.xfit))
        
        for i, xvals in enumerate(self.xfit):
            c = gca()._get_lines.color_cycle.next()
            err = abs(self.func[i](self.solp, self.xfit[i]) - self.yfit[i])
            plot(self.xfit[i], err, color=c)
            fill_between(self.xfit[i], err, color=c, alpha=.3)
        
        ylabel('Residuals')
        myy = yticks()[0]
        yticks([max(myy), min(myy),0], size=18)
        F2.set_xticklabels([])
        
        grid()
        xlabel(XLABEL)
        #http://stackoverflow.com/questions/10101700/moving-matplotlib-legend-outside-of-the-axis-makes-it-cutoff-by-the-figure-box
        savefig('pdf/'+TITLE+'.pdf',bbox_extra_artists=(lgd, t), bbox_inches='tight')
        savefig('png/'+TITLE+'.png',bbox_extra_artists=(lgd, t), bbox_inches='tight')
from matplotlib import pylab, mlab, pyplot
from matplotlib.pyplot import *
import numpy as np
from numpy import diff, sign
plt = pyplot

from pylab import gcf, gca

from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs

import mpld3
from mpld3 import plugins

from scipy.optimize import leastsq
from scipy.stats import chisquare
import scipy.interpolate as inter
import random
import inspect

from IPython.html.widgets import interact,interactive

from IPython.core.display import HTML

def css_styling():
    styles = open('./styles/custom.css', 'r').read()
    return HTML(styles)

    
def get_range_ind(xarray, startvalue, endvalue):
    
    a      = xarray
    
    target = startvalue
    i0 = min(range(len(a)), key=lambda i: abs(a[i]-target))
    
    target = endvalue
    i1 = min(range(len(a)), key=lambda i: abs(a[i]-target))
    
    return i0, i1

def get_new_xy(x, y, xselect):
    ''' xselect = [x0start, x0end,
                    x1start, x1end, 
                    ...]
        returns: x, y with elements in these sections '''
    xl = len(xselect)
    i = 0
    xfit = []
    yfit = []
    while i < xl:
        i0, i1 = get_range_ind(x, xselect[i], xselect[i+1])
        xfit += list(x[i0:i1])
        yfit += list(y[i0:i1])
        i += 2
    return xfit, yfit

def lin(p,x):
    return p[0]*x+p[1]
    
    
import json
import os

import urllib2
import IPython

from IPython.lib import kernel
connection_file_path = kernel.get_connection_file()
connection_file = os.path.basename(connection_file_path)
kernel_id = connection_file.split('-', 1)[1].split('.')[0]

def NotebookName():
    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    # Updated answer with semi-solutions for both IPython 2.x and IPython < 2.x
    if IPython.version_info[0] < 2:
        ## Not sure if it's even possible to get the port for the
        ## notebook app; so just using the default...
        notebooks = json.load(urllib2.urlopen('http://127.0.0.1:8888/notebooks'))
        for nb in notebooks:
            if nb['kernel_id'] == kernel_id:
                return str(nb['name'])
                break
    else:
        sessions = json.load(urllib2.urlopen('http://127.0.0.1:8888/api/sessions'))
        for sess in sessions:
            if sess['kernel']['id'] == kernel_id:
                return str(sess['notebook']['name'])
                break

                
def TextTag():
    ax = gca()
    thetag = os.getcwd()[0:3]+'...'+os.getcwd()[-20:]+'\\'+NotebookName()
    thetag = thetag.replace(' ','_')
    ax.text(0.01, 0.99, r'\verb{'+thetag, horizontalalignment='left',
            verticalalignment='top',transform=ax.transAxes,
            bbox=dict(facecolor='black', alpha=0.5),fontsize=10, color='white')

def get_table(header, rows):
    
    t = r'\begin{tabular}{|| l | '+(len(header)-1)*'l '
    t += '}' 
    
    for h in header: 
        if h == header[0]:
            t += h
        else:
            t += '&'+h
            
    t += '\\\\\hline ' 
    
    for row in rows: 
        for r in row:
            if r == row[0]:
                t += str(r)
            else:
                t += '&'+str(r)
        t += '\\\ '
    
    t += '\end{tabular}'
    
    return t
    

def get_minmax_indices(x, data, sval=1.0, debug=False):
    '''
    returns: array of minima, array of maxima
    s: noise reject 
    '''
    #if debug: plot(x,data, c='b')
    d2 = inter.UnivariateSpline(x,data,s=sval)
    data = d2(x)
    if debug: plot(x,data, c='r', lw=2, label='smooth')
        
    # that's the line, you need:
    a = diff(sign(diff(data))).nonzero()[0] + 1 # local min+max
    b = (diff(sign(diff(data))) > 0).nonzero()[0] + 1 # local min
    c = (diff(sign(diff(data))) < 0).nonzero()[0] + 1 # local max
    
    #if debug: 
    #    plot(x[b], data[b], "o", label="min")
    #    plot(x[c], data[c], "o", label="max")
    
    return b,c
    
def colorcycle(num_plots):
    colormap = plt.cm.summer
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0.35, 1.0, num_plots)])
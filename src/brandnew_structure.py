
from helpers import *
from descartes import *
#from gdsCAD import *
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import unary_union, cascaded_union
from in_out_show import showPolygons
from matplotlib import pylab, mlab, pyplot, cm
from matplotlib.pyplot import axis, plot, legend
plt = pyplot
from pylab import gcf, gca

from numpy import array, mean
import numpy as np

from descartes import PolygonPatch

class EMPTY:
    """ no doc."""
    def __init__(self):
        self.STRUCTURE = empty()
        self.BOUNDARY = empty()
        self.ANKERS = [anker(self.BOUNDARY)]
        
class LAYER:
    """ no doc."""
    def __init__(self, polylist, name):
        if isinstance(polylist,list):
            self.POLIS = polylist
        else: 
            self.POLIS = [polylist]
        self.NAME   = name
        self.ANKERS = {}
        
    def add_polis(self, additional_polis):
        newpolis = unary_union(self.POLIS+additional_polis)
        newpolis = list(flattenMultipoly(newpolis))
        self.POLIS = newpolis#list(np.hstack(newpolis))
        
    def get_polis(self):
        return self.POLIS
        
    def add_anker(self, ankerpoint, name=None):
        if name != None:
            self.ANKERS[name] = ankerpoint
            #self.ANKERS.update({name:ankerpoint})
        else: 
            name = len(self.ANKERS)
            self.ANKERS[name] = ankerpoint
            
    def get_ankerpoint(self,APkey):
        if isinstance(self.POLIS, list):
            POLY = unary_union(self.POLIS)
            POLY2 = POLY.convex_hull
            APX,APY = anker(POLY2,APkey)
            #xs = [anker(s,APkey)[0] for s in self.POLIS]
            #ys = [anker(s,APkey)[1] for s in self.POLIS]
            #APX,APY = mean(xs),mean(ys)
        else:
            APX,APY = anker(self.POLIS, APkey)
        return APX,APY
            
    def translate_layer(self,NP,OP):
        """ OP: "old point" [x,y] NP: "new point" [x,y] """
        diff = array(NP) - array(OP)
        translated_polis = [translate(s, xoff=diff[0], yoff=diff[1]) 
                            for s in self.POLIS]
        self.POLIS = translated_polis
        
        for k in self.ANKERS.keys():
            oldvalue = self.ANKERS[k]
            self.add_anker(list(array(oldvalue) + diff), k)
        
    def rotate_layer(self, angle, origin):
        """ origin: [x,y] """
        rotated_polis = [rotate(s, angle, origin)
                        for s in self.POLIS]
        self.POLIS = rotated_polis
        
        for k in self.ANKERS.keys():
            Pnew = rotate(Point(self.ANKERS[k]), angle, origin)
            xnew, ynew = Pnew.xy
            self.ANKERS[k] = [xnew[0], ynew[0]]
        
    def scale_layer(self, xf, yf, origin):
        """ xf,yf,zf: factors in x, y and z direction
        origin: [x,y] """
        zf = 1
        origin = origin + [0]
        scaled_polis = [scale(s, xf, yf, zf, origin)
                        for s in self.POLIS]
        self.POLIS = scaled_polis
        
        for k in self.ANKERS.keys():
            Pnew = scale(Point(self.ANKERS[k]), xf, yf, zf, origin)
            xnew, ynew = Pnew.xy
            self.ANKERS[k] = [xnew[0], ynew[0]]

class BRAND_NEW_STRUCTURE:
    """ I DON'T HAVE A DOCSTRING """
    def __init__(self, BOUNDARY, STRUCTURE):
        self.BOUNDARY  = LAYER(BOUNDARY,'BOUNDARY')
        self.STRUCTURE = LAYER(STRUCTURE,'STRUCTURE')
        
        self.ANKERS = {}
        
        self.STRUC1 = LAYER([],'STRUC1')
        self.STRUC2 = LAYER([],'STRUC2')
        self.EBL = LAYER([],'EBL')
        
        self.layers = {'BOUNDARY':self.BOUNDARY,
                        'STRUCTURE':self.STRUCTURE,
                        'STRUC1':self.STRUC1,
                        'STRUC2':self.STRUC2,
                        'EBL':self.EBL
                        }
        
    def get_polygons(self,layername=None):
        if layername:
            L = getattr(self,layername)
            polys = L.get_polis()
        else: 
            polys = make_flat_list(self.BOUNDARY.get_polis(), self.STRUCTURE.get_polis())
        return polys
        
    def get_ankers(self):
        for name in self.layers.keys():
            L = getattr(self,name)
            ankers = L.ANKERS
            for a in ankers.keys():
                self.ANKERS[a] = L.ANKERS[a]
        return self.ANKERS
        
    def add_anker(self,ankerpoint, name=None):
        if name:
            self.STRUCTURE.add_anker(ankerpoint, name)
            self.ANKERS.update({name:ankerpoint})
        else: 
            name = len(self.ANKERS)
            self.ANKERS[name] = ankerpoint
            self.STRUCTURE.add_anker(ankerpoint, name)
    
    def add_layer(self,polylist,name):
        setattr(self, name, LAYER(polylist,name))
        #self.name = LAYER(polylist,name)
        self.layers[name]=LAYER(polylist,name)
        
    def translate(self,NP,OP):
        for k in self.layers.keys():
            L = getattr(self,k)
            L.translate_layer(NP,OP)
            dummy = self.get_ankers()
            
    def rotate(self, angle, origin):
        for k in self.layers.keys():
            L = getattr(self,k)
            L.rotate_layer(angle,origin)
            
    def scale(self, xf, yf, origin):
        for k in self.layers.keys():
            L = getattr(self,k)
            L.scale_layer(xf, yf, origin)
            
    def get_polis_from_layer(self,layername):
        return self.layers[layername].get_polis()
    
    def make_copy(self):
        S = BRAND_NEW_STRUCTURE(self.BOUNDARY, self.STRUCTURE)
        for ka in self.ANKERS.keys():
            S.add_anker(self.ANKERS[ka],ka)
        for k in self.layers.keys():
            L = getattr(self,k)
            S.add_layer(L.get_polis(),k)
            Slayer = getattr(S,k)
            ankers = L.ANKERS
            for a in ankers.keys():
                Slayer.add_anker(ankers[a],a)
        return S
        
    def show_info(self):
        colormap = plt.cm.rainbow
        colors = [colormap(i) for i in np.linspace(0.0, 1.0, 1+len(self.layers.keys()))]
        for j,k in enumerate(self.layers.keys()):
            L = getattr(self,k)
            polys = L.get_polis()
            if len(polys):
                gca().add_patch(PolygonPatch(empty(),fc=colors[j],alpha=0.85,label=k))
            showPolygons(polys,[colors[j]]*len(polys))
        ankers = self.get_ankers()
        ankers = self.ANKERS
        print ankers
        for a in ankers.keys():
            plot(ankers[a][0],ankers[a][1],'o',label=a)
        legend()

from shapely.geometry import Polygon, LineString, MultiPolygon
from numpy import array
import numpy as np

def invert_polarity(BoundingBox, Polygons):
    """ 
    G: GROUNDPLANE
    
    code:: 
    
        BoundingBox = SD.mybox((0,0),chipwidth,chipheight)
        Polygons = G.get_polygons() or G.get_groundpolys() + G.get_strucpolys()
        
    """
    if isinstance(BoundingBox, list):
        print 'BoundingBox should be a single polygon.'
    
    GRold = [BoundingBox] 
    
    for s in Polygons:
        if not s.is_valid:
            pass
        else: 
            GRnew = SD.flattenMultipolyG([GS.difference(s) for GS in GRold])
            GRold = GRnew
        
    return list(GRnew)

def anker(poly, keyword = 'lower_left'):
    """
    keywords = 'lower_left','upper_left','lower_right','upper_right','center'
    returns: array([x,y])
    """
    if keyword not in ['lower_left','upper_left','lower_right','upper_right','center']:
        print 'KEYWORD NOT RECOGNIZED.'
    if type(poly) != LineString:
        X, Y = poly.boundary.xy
    else: X,Y = poly.xy
    X = array(X)
    Y = array(Y)
    if keyword == 'upper_left':
        anker_xy = (min(X), max(Y))
    elif keyword == 'lower_left':
        anker_xy = (min(X), min(Y))
    elif keyword == 'lower_right':
        anker_xy = (max(X), min(Y))
    elif keyword == 'upper_right':
        anker_xy = (max(X), max(Y))
    elif keyword == 'center':
        anker_xy = (min(X)+(max(X)-min(X))/2, min(Y)+(max(Y)-min(Y))/2)
    else: anker_xy = (0,0)
    return array([anker_xy[0],anker_xy[1]])

def find_vertex(keyword,x,y, average=False):
    """ 
    keywords: 'left','right','top','bottom'
    x, y: coordinates of the polygon
    returns: the arguments (average=False) or the average argument (average=True) of 
    the polygon indices
    """
    
    keywords = ['left','right','top','bottom']
    x = array(x)
    y = array(y)
    
    if keyword not in keywords:
        raise Exception('Keyword not valid. Keyword must be in: ',keywords)
        
    elif keyword == 'left':
        # ... minimum x
        arg_x = np.where(x==min(x))
        if average: arg_x = int(mean(arg_x))
        return arg_x
    elif keyword == 'right':
        # ... maximum x
        arg_x = np.where(x==max(x))
        if average: arg_x = int(mean(arg_x))
        return arg_x
    elif keyword == 'bottom':
        # ... minimum y
        arg_y = np.where(y==min(y))
        if average: arg_y = int(mean(arg_y))
        return arg_y
    elif keyword == 'top':
        # ... maximum y
        arg_y = np.where(y==max(y))
        if average: arg_y = int(mean(arg_y))
        return arg_y

def make_flat_list(*kwargs):
    F = []
    for e in kwargs:
        if isinstance(e,list):
            F += e
        else:
            F.append(e)
    return F
	
def flattenMultipolyG(arr):
    """
    Shapely multipolygon >> list of polygons
    """
    res = []
    for a in arr:
        if a.type == 'Polygon':
            res.append(a)
        else: 
            for el in a:
                res.append(el)
    res = array(res)
    return res.flatten()

def flattenMultipoly(arr):
    """
    Shapely multipolygon >> list of polygons
    """
    res = []
    if isinstance(arr,MultiPolygon):
        for a in arr:
            if a.type == 'Polygon':
                res.append(a)
            else: 
                for el in a:
                    res.append(el)
    elif isinstance(arr,Polygon):
        res.append(arr)
    res = array(res)
    return res.flatten()

def empty():
    return Polygon([(0,0),(0,0),(0,0)])
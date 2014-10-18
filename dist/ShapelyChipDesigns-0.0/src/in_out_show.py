
from helpers import *

import mpld3 # version 0.2
from mpld3 import plugins
from pylab import gcf, gca
from matplotlib import pylab, mlab, pyplot
from matplotlib.pyplot import axis
import numpy as np
plt = pyplot

from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs

from shapely.geometry import Polygon
from shapely.ops import unary_union

from descartes import PolygonPatch
from shapely.geometry import mapping
import json
import os
import pkg_resources

import urllib2
import IPython
from IPython.lib import kernel
#connection_file_path = kernel.get_connection_file()
#connection_file = os.path.basename(connection_file_path)
#kernel_id = connection_file.split('-', 1)[1].split('.')[0]

def loaddxf_todict(filename):
    """  """
    try:
        os.remove('buffer.geojson')
    except:
        pass
        
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'

    os.system('ogr2ogr -f GEOJSON buffer.geojson '+filename)

    s =  open("buffer.geojson", "r").read()

    L = json.loads(s)

    return L

def loaddxf_polylist3(filename):
    """ (3 versions!)  """
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'
        
    Dict = loaddxf_todict(filename)

    PS = []

    for f in Dict['features']:
        #print f['geometry']
        c = f['geometry']['coordinates']
        #print len(c)
        """
        p = Polygon(c)
        PS += [p]
        """
        if len(c)>1:
            p = Polygon(c[0], c[1:])
        elif not len(c):
            p = empty()
        else: p = Polygon(c[0])
        
        PS += [p]
    return PS

def loaddxf_polylist4(filename):
    """ (4 versions!)  """
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'
        
    Dict = loaddxf_todict(filename)

    PS = []

    if Dict.has_key('features'):
        for f in Dict['features']:
            c = f['geometry']['coordinates']

            p = Polygon(c)

            PS += [p]

    else:
        if Dict.has_key('coordinates'):
            for d in Dict['coordinates']:
                if len(d)== 1:
                    p = Polygon(d[0])
                if len(d)>1:
                    p = Polygon(d[0],d[1:])
                PS += [p]

    return PS

def loaddxf_polylist2(filename):
    """ (3 versions!) """
    if filename.endswith('.dxf'):
        pass
    else: filename = filename+'.dxf'

    try:
        os.remove('buffer.geojson')
    except:
        pass   

    os.system('ogr2ogr -f GEOJSON buffer.geojson '+filename+'.dxf')

    s =  open("buffer.geojson", "r").read()

    L = json.loads(s)

    CO = []
    PS = []

    for l in L['features']:
        c = l['geometry']['coordinates']

        if len(c)>1:
            p = Polygon(c[0], c[1:-1])
        else: p = Polygon(c[0])
        
        PS += [p]

    return PS


def load_dxf(filename,debug=False):
    f=filename
    G = []

    try:
        G = loaddxf_polylist3(f)
    except: 
        if debug: print 'no load with ver3'

    try:
        G = loaddxf_polylist2(f)
    except: 
        if debug: print 'no load with ver2'

    try:
        G = loaddxf_polylist4(f)
    except:
        if debug: print 'no load with ver4'

    return G

def NotebookName():
    """
    .. doctest::
    
        >>> import _ShapelyChipDesigns as SD
        >>> print SD.NotebookName()
    
    """
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

def savedxf_polylist(list_of_polygons, filename=None, 
    debug=False, save_as='POLYGON'):
    """Saves a list_of_polygons to a dxf file. 
    The polygons have a HATCH-property, which is not supported by AutoCAD and LinkCAD. 
    It can be viewed in e.g. Klayout. 
    To convert the polygons into one which do not have the HATCH property, use the built-in convert function.
    Relies on ogr2ogr. 
    
    .. plot::
    
        import ShapelyChipDesigns as SD
        C = SD.Point(0,0).buffer(5)
        SD.savedxf_polylist([C], 'acircle')
        C
    """
    try:
        os.remove('buffer.geojson')
    except:
        pass

    GNEW = []

    for p in list_of_polygons:
        
        if p.is_valid:
            GNEW += [p]
        if not p.is_valid:
            pnew = p.buffer(0)
            if pnew.is_valid:
                GNEW += [pnew]
                if debug: print 'new polygon made from self intersecting polygon, is valid: ',pnew.is_valid
            else:
                if debug: print 'self intersecting polygon thrown out.'
                else: pass

    if not GNEW:
        GNEW = [empty()]
            
    buffer_obj = unary_union(GNEW)

    if debug: print 'started writing file ...'
    f = open("buffer.geojson", "wb")
    f.write(json.dumps(mapping(buffer_obj)))
    f.close()
    if debug: print 'finished.'

    if debug: print 'started conversion of geojson to dxf ...'
    if filename == None:
        filename = 'buffer'
    if debug: print 'save as MULTILINESTRING or POLYGON...'
    # --config("DXF_WRITE_HATCH", "NO")
    os.system('ogr2ogr -f DXF '+filename+'.dxf buffer.geojson')
    if debug: print 'finished.'
    print 'saved '+filename+'.dxf'
    
def convert(input_filename, output_filename):
    """This function can also be used to repair the savedxf_polylist-output, by choosing
    the unrepaired file as input and another ``*.dxf`` file as output. The output will no longer have the hatch property.
    Relies on the command line access to klayout.
    (test by typing klayout into the command line, 
    if the command is not found, klayout needs to be added to the PATH variable.)"""
    c_file = pkg_resources.resource_filename('ShapelyChipDesigns', 'convert.rb')
    os.system('klayout -rd input='+input_filename+' -rd output='+output_filename+' -r '+c_file)   

def mouseshow():
    fig = gcf()
    plugins.connect(fig, plugins.MousePosition(fontsize=14))
    return mpld3.display(fig)
    
def showPolygons(list_of_polygons, list_of_colors = False):
    """ 
    Adds patches for a list of shapely polygons. A Multipolygon is a list of Polygons.
    """
    if list_of_colors:
        colors = list_of_colors
    else: 
        colormap = plt.cm.summer
        colors = [colormap(i) for i in np.linspace(0.35, 1.0, len(list_of_polygons))]

    fig = gcf()
    ax  = gca()

    if len(list_of_polygons):
        for i,s in enumerate(list_of_polygons):
            ax.add_patch(PolygonPatch(s,fc=colors[i],alpha=0.85))
            
    axis('equal')
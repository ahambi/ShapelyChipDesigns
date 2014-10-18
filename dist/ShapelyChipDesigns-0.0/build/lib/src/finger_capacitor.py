
from helpers import *
from brandnew_structure import *

from numpy import arange

from descartes import *
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import unary_union, cascaded_union

def MakeFingercapacitor(n1, n2, \
                        wfinger, lfinger, wgap, ltaper, \
                        wc, wGgap, \
                        wGfinger=None, lfingeradd=0, *kwargs):
    """ 
    :param int n1: number of fingers (left side)
    :param int n2:  "---------------" (right side)
    :param int wfinger: finger width
    :param int lfinger: finger length  
    :param int wgap: finger-to-finger gap
    :param int ltaper: taper length
    :param int wc: transmission line - conductor width
    :param int wGgap: transmission line: gap width
    :param int wGfinger: _optional_ gap between the outer fingers and the groundplane
    :param int lfingeradd: _optional_ an additional length can be added to the fingers which points into the gap
    :return: A finger capacitor
    :rtype: BRAND_NEW_STRUCTURE
    
    .. note:: Without the optional argument ``wGfinger`` the gap between the outer fingers and the ground-plane 
                holds the ratio of ``wc/wGgap``
    
    .. plot:: tests/test_finger_capacitor.py
       :include-source:
        
    .. raw:: html
    
        <div style="margin-top:10px;">
        <iframe width="700" height="500" scrolling="no" frameborder="0" src="../../../docs/tests/_img/test_finger_capacitor.html"></iframe>
        </div>
    """
    if not ((n1==n2+1) or (n2==n1+1) or (n1==n2)):
        raise Exception("Capacitor: The finger numbers must be equal or differ by one! But here n1="+str(n1)+" and n2="+str(n2))

    if n1 and n2:
        wtaper = (n1+n2)*wfinger + (n1+n2-1)*wgap
    else:
        try: wtaper = kwargs[0]
        except: raise Exception('Either set n1 and n2 unequal to zero or provide the taper width as first kwarg.')
        lfinger = 0

    if wGfinger == None:
        wGfinger = 4.5/10.0*wtaper

    taperL = Polygon([(0,-wc/2.),
                     (ltaper, -wtaper/2.),
                     (ltaper, wtaper/2.),
                     (0,wc/2.)])

    taperR = taperL

    finger = Polygon([(0,0),
                      (lfinger+lfingeradd, 0),
                      (lfinger+lfingeradd, wfinger),
                      (0,wfinger)])

    boundary = Polygon([(0, -wc/2. - wGgap), 
                        (ltaper, -wtaper/2. - wGfinger),
                        (ltaper + lfinger + wgap,  -wtaper/2. - wGfinger), 
                        (2*ltaper + lfinger + wgap,-wc/2.  - wGgap),
                        (2*ltaper + lfinger + wgap, wc/2. + wGgap),
                        (ltaper + lfinger + wgap,  wtaper/2. + wGfinger),
                        (ltaper, wtaper/2. + wGfinger),
                        (0, wc/2. + wGgap)
                        ])

    ######## place fingers 

    if (n1%2==0 and n2%2==0) or (n1%2==1 and n2%2==1):
        # if BOTH sides have even or odd finger numbers 
        f0L = translate(finger, ltaper, -wtaper/2.)
        f0R = translate(finger, ltaper, -wtaper/2. + wfinger + wgap)

    elif n1==n2+1:
        # n1 has more fingers >> start with left side
        f0L = translate(finger, ltaper, -wtaper/2.)
        f0R = translate(finger, ltaper, -wtaper/2. + wfinger + wgap)

    elif n2==n1+1:
        # n2 has more fingers >> start with right side
        f0L = translate(finger, ltaper, -wtaper/2. + wfinger + wgap)
        f0R = translate(finger, ltaper, -wtaper/2.)

    capL = empty()
    capL = capL.union(taperL)

    capR = empty()
    capR = capR.union(taperR)

    if n1 and n2:

        #print "n1"
        for i in arange(n1):
            capL = capL.union(f0L)
            f0L = translate(f0L, 0, 2*wfinger + 2*wgap)
            #print 2*wfinger + 2*wgap

        #print "n2"
        for i in arange(n2):
            capR = capR.union(f0R)
            f0R = translate(f0R, 0, 2*wfinger + 2*wgap)
            #print 2*wfinger + 2*wgap

    ############ finish by aligning the left and the right part

    capR = scale(capR,-1)
    capR = translate(capR, ltaper+wgap-lfingeradd)
    cap = capL.union(capR)

    C = BRAND_NEW_STRUCTURE(boundary,[capL,capR])
    C.add_anker([0,0],'L')
    C.add_anker([2*ltaper+lfinger+wgap,0],'R')
    return C

from pylab import show, figure
import ShapelyChipDesigns as SD
import mpld3

n1      = 3    
n2      = 2    
wfinger = 3    
lfinger = 90    
wgap    = 3   
ltaper  = 100 
wc      = 10    
wGgap   = 4.5 

CAP = SD.MakeFingercapacitor(n1, n2,
                             wfinger, lfinger, wgap, ltaper, 
                             wc, wGgap)

fig = figure()
CAP.show_info()
SD.mouseshow() 

mpld3.save_html(fig, "_img/test_finger_capacitor.html")

from pylab import show, figure, subplot, \
                    plot, tight_layout, grid, \
                    axis
import ShapelyChipDesigns as SD
import mpld3

##########################
# larger EBL markers:
mwidth1  = 10
mlength1 = 30

markerlength, markerwidth = mlength1, mwidth1

P0 = SD.LineString([(-0.5,0),(0.5,0)])
M0 = SD.scale(P0, markerlength)
M1 = SD.rotate(M0,90)

M00 = M0.buffer(markerwidth/2., cap_style=3)
M11 = M1.buffer(markerwidth/2., cap_style=3)

MEBL1 = M00.union(M11)

##########################
# smaller EBL markers:
mwidth2  = 2
mlength2 = 12

markerlength, markerwidth = mlength2, mwidth2

P0 = SD.LineString([(-0.5,0),(0.5,0)])
M0 = SD.scale(P0, markerlength)
M1 = SD.rotate(M0,90)

M00 = M0.buffer(markerwidth/2., cap_style=3)
M11 = M1.buffer(markerwidth/2., cap_style=3)

MEBL2 = M00.union(M11)

# marker positions
wfsize = 500 

ps1 = SD.get_RegPoly_xy((0,0), 
                        wfsize-2*mlength1, 
                        3)
ps2 = SD.get_RegPoly_xy((0,0), 
                        wfsize-2*mlength1-5*mlength2, 
                        3)

# add outer markers
MARKERS = []

marker = MEBL1
POINTS = zip(ps1[0],ps1[1])

for p in POINTS:
    M = SD.translate(marker, p[0],p[1])
    MARKERS += [M]
    
# add inner markers

marker = MEBL2
POINTS = zip(ps2[0], ps2[1])

for p in POINTS:
    M = SD.translate(marker, 
                     p[0], p[1])
    MARKERS += [M]
    
EBLMARKERS = SD.BRAND_NEW_STRUCTURE(MARKERS,
                                    [SD.empty()])

EBLMARKERS.add_anker([0,0], 'center')
EBLMARKERS.rotate(-90, EBLMARKERS.ANKERS['center'])

SD.showPolygons(EBLMARKERS.get_polygons())

S = EBLMARKERS
for k in S.ANKERS.keys():
    x,y = S.ANKERS[k]
    plot(x,y,'o', markersize=5, label=str(k))

    
grid()
show()
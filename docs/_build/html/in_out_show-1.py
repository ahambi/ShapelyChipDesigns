import ShapelyChipDesigns as SD
C = SD.Point(0,0).buffer(5)
SD.savedxf_polylist([C], 'acircle')
C
import numpy

slidable_depth = 0.448450 # 0.01 0.8

def ABCDEGJ(depth):
    B = numpy.array([ 0.5, -depth, 0.0])
    
    x = 0.5 / (1.0 + 1.0/(depth ** 2))
    y = x / depth
    D = numpy.array([   x,      y, 0.0])

    return Polyhedron(
        [
            numpy.array([ 0.5,  depth, 0.0]),  # A
            B,                                 # B
            -D,                                # C
            D,                                 # D
            -B,                                # E
            numpy.array([ 0.0,  depth, 0.5]),  # G
            numpy.array([ 0.0,    0.0, 0.5])], # J
        [
            (0,1,2,3,4),
            (0,4,5),
            (5,6,1,0),
            (6,4,3),
            (6,5,4),
            (6,3,2),
            (6,2,1)],
        color = [0.1,1.0,0.1])

polyhedra = [ ABCDEGJ(slidable_depth) ]

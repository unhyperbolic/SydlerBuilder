import numpy

slidable_depth = 0.318500 # 0.1 2

slidable_h = 0.842900 # 0.1 2

def polyhedron_ABCDEGJ(depth):
    A = numpy.array([ 0.5,  depth, 0.0])
    B = numpy.array([ 0.5, -depth, 0.0])
       
    x = 0.5 / (1.0 + 1.0/(depth ** 2))
    y = x / depth
    C = numpy.array([  -x,     -y, 0.0])

    D = -C
    E = -B
    
    G = numpy.array([ 0.0,  depth, 0.5])
    J = numpy.array([ 0.0,    0.0, 0.5])

    a, b, c, d, e, g, j = range(7)

    return Polyhedron(
        [ A, B, C, D, E, G, J ],
        [ (a, b, c, d, e),
          (a, e, g),
          (g, j, b, a),
          (j, e, d),
          (j, g, e),
          (j, d, c),
          (j, c, b)],
          #name = 'ABCDEGJ',
          labels = ['A', 'B', 'C', 'D', 'E', 'G', 'J'])

def polyhedron_Q(h):
    y = 2.0 / (2.0 + h**2/2.0) - 1.0
    z = 2.0 * h / (4 + h**2) 
    A = numpy.array([ 0.0,   y,   z])
    B = numpy.array([-1.0, 0.0, 0.0])
    C = numpy.array([ 1.0, 0.0, 0.0])
    S = numpy.array([ 0.0, 1.0,   h])
    T = numpy.array([ 0.0, 1.0, 0.0])

    a, b, c, s, t = range(5)

    return Polyhedron(
        [ A, B, C, S, T ],
        [ (b, t, c),
          (b, s, t),
          (c, t, s),
          (a, b, c),
          (a, s, b),
          (a, c, s)],
          name = 'Q',
          labels = ['A', 'B', 'C', 'S', 'T'])
    
polyhedra = [ #polyhedron_ABCDEGJ(slidable_depth),
              polyhedron_Q(slidable_h)
            ]

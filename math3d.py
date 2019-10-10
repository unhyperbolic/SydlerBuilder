import numpy

from math import sqrt, sin, cos

def TransformFromFlag(v0, v1, v2):
    x = v1 - v0
    y = v2 - v0
#    z = 

def center_of_mass(polyhedra):
    return sum([p.center() for p in polyhedra]) / len(polyhedra)

def explode_offsets(polyhedra, amt, addl_offset = None):
    centers = [ p.center() for p in polyhedra ]

    center = sum(centers) / len(polyhedra)

    result = [ amt * (c - center) for c in centers ]
    if addl_offset is None:
        return result
    return [ r + addl_offset for r in result ]

def explode_polyhedra(polyhedra, amt):

    total_center = total_center(polyhedra)
    
    return [
        p.moved(amt * (p.center() - total_center))
        for p in polyhedra ]

class Polyhedron:
    def __init__(self, vertices, faces,
                 color = [1, 0.2, 0.2],
                 name = '',
                 labels = None):
        self.vertices = vertices
        self.faces = faces
        self.color = color
        self.name = name
        self.labels = labels

    def facesWithNormal(self):
        for face in self.faces:
            v0 = self.vertices[face[0]]
            v1 = self.vertices[face[1]]
            v2 = self.vertices[face[2]]
            n = numpy.cross(v1 - v0, v2 - v0)

            yield ([self.vertices[i] for i in face],
                   n / numpy.linalg.norm(n))

    def center(self):
        return sum(self.vertices) / len(self.vertices)

    def moved(self, t):
        return Polyhedron(
            [ v + t for v in self.vertices],
            self.faces,
            color = self.color,
            name = self.name,
            labels = self.labels)

import numpy
import math

### Helper functions

def distance(x, y):
    return numpy.linalg.norm(x - y)

def proj(x, y):
    return x - y * numpy.dot(x,y) / numpy.dot(y, y)

def specialCross(V1, V2, V3, V4, V5):
    d1=V1[0]
    d2=V1[2]
    d3=V1[1]
    m1=V2[0]
    m2=V2[2]
    m3=V2[1]
    e1=V3[0]
    e2=V3[2]
    j1=V4[0]
    j2=V4[2]
    k1=V5[0]
    k2=V5[2]
    k3=V5[1]
        
    s1=-e2*j1+e1*j2+e2*m1 - j2*m1 - e1*m2 + j1*m2
    s2=d2*e1-d1*e2-d2*j1+d1*j2+e2*m1-j2*m1-e1*m2+j1*m2
    s=s1/s2


    p1=s*d1+ (1-s)*k1
    p2=s*d2+ (1-s)*k2
    p3=s*d3+ (1-s)*k3

    return numpy.array([p1,p3,p2])

### Parameters

slidable_a0 = 0.644000 # 0 1
slidable_a1 = 0.537000 # 0 1
slidable_a2 = 0.126000 # 0 1

aa = math.sqrt(1/slidable_a0 - 1)
bb = math.sqrt(1/slidable_a1 - 1)
cc = math.sqrt(1/slidable_a2 - 1)

A = numpy.array([0, 0, aa])
B = numpy.array([0, 0, 0])
C = numpy.array([aa*bb,0,0])
D = numpy.array([aa*bb,bb,0])

t = (aa*cc)/math.sqrt(aa*aa*bb*bb+bb*bb)
E = numpy.array([t*aa*bb,t*bb,0])

t = math.sqrt(aa*aa*cc*cc+cc*cc)
F = numpy.array([t, 0, 0])

G = (D+F) / 2

H = G.copy()
t1 = distance(B,G)**2+distance(A,B)**2-distance(C,G)**2
t2 = 2 * distance(A, B)
H[2] = t1 / t2

I = H.copy()
I[1] = 0

J = proj(H, numpy.array([D[1],-D[0], 0]))

K = 2 * H - A

L = 2 * I - A

M = 2 * J - A

points = {
    'A': A,
    'B': B,
    'C': C,
    'D': D,
    'E': E,
    'F': F,
    'G': G,
    'H': H,
    'I': I,
    'J': J,
    'K': K,
    'L': L,
    'M': M,
    'N' : specialCross(D, M, E, J, M),
    'O' : specialCross(D, M, E, J, K),
    'P' : specialCross(D, J, A, E, J),
    'Q' : specialCross(D, M, A, E, M),
    'R' : specialCross(D, M, A, E, K),
    'S' : specialCross(D, J, A, E, H) }

tet_topology = [
    (0, 1, 2),
    (0, 2, 3),
    (0, 3, 1),
    (3, 2, 1) ]

cone_topology = [
    (0, 1, 4),
    (1, 2, 4),
    (2, 3, 4),
    (3, 0, 4),
    (3, 2, 1, 0) ]

prism_topology = [
    (0, 1, 2),
    (5, 4, 3),
    (0, 3, 4, 1),
    (1, 4, 5, 2),
    (2, 5, 3, 0) ]

def makePoly(pts_dict, pts_string, topology, name = '', color = (1, 0.2, 0.2)):
    return Polyhedron(
        [ pts_dict[l] for l in pts_string ],
        topology,
        name = name,
        #name = name if name else ''.join(sorted([l for l in pts_string])),
        labels = [ l for l in pts_string ],
        color = color)

O_color = (0.75, 0.75, 0.2)
Osplit_color = (0.9, 0.5, 0.2)
pseudo_color = (0.2, 0.8, 0.2)

O1 = makePoly(points, 'ABCD', tet_topology, name = 'O1', color = O_color)
O2 = makePoly(points, 'ABFE', tet_topology, name = 'O2', color = O_color)
O3 = makePoly(points, 'ADKM', tet_topology, name = 'O3', color = O_color)
O4 = makePoly(points, 'AFLK', tet_topology, name = 'O4', color = O_color)

AFHI = makePoly(points, 'AFIH', tet_topology, color = Osplit_color)
AHIJ = makePoly(points, 'AHIJ', tet_topology)
FHKO = makePoly(points, 'FHOK', tet_topology)

ACDHI = makePoly(points, 'IHDCA', cone_topology, color = pseudo_color)
AEFJH = makePoly(points, 'EFHJA', cone_topology, color = pseudo_color)
CDFHI = makePoly(points, 'CDHIF', cone_topology, color = pseudo_color)
DEFHJ = makePoly(points, 'EFHJD', cone_topology, color = pseudo_color)
DHJKM = makePoly(points, 'HJMKD', cone_topology, color = pseudo_color)
FHIKL = makePoly(points, 'KLIHF', cone_topology, color = pseudo_color)

ADHJNO = makePoly(points, 'AHJDON', prism_topology, color = Osplit_color)
HJKMNO = makePoly(points, 'HOKJNM', prism_topology, color = Osplit_color)
EFKMNO = makePoly(points, 'ENMFOK', prism_topology)

defhno_topology = [
   (0,3,5),
   (0,2,3),
   (0,1,2),
   (0,4,1),
   (0,5,4),
   (5,3,2,1,4)
]

DEFHNO = makePoly(points, 'DEFHNO', defhno_topology)

slidable_decomp = 5.284710 # 0 9.99

anim = slidable_decomp - int(slidable_decomp)

def lerp(a, b, anim = anim):

    anim = min(1, max(0, (anim - 0.5) * 1.5 + 0.5))

    return a * (1.0 - anim) + b * anim

slidable_stage1 = 0.830000 # 0 1
slidable_stage2 = 0.948000 # 0 1
slidable_stage3 = 0.433000 # 0 1
slidable_stage5 = 0.575000 # 0 1
slidable_stage6 = 0.685000 # 0 1

stage0_O1_pos, stage0_O3_pos = explode_offsets(
    [O1, O3], slidable_stage1)

stage0 = [ O1.moved(stage0_O1_pos),
           O3.moved(stage0_O3_pos) ]

stage1_ADHJNO_pos, stage1_HJKMNO_pos = explode_offsets(
    [ADHJNO, HJKMNO], slidable_stage2, stage0_O3_pos)

stage1 = [ O1.moved(stage0_O1_pos),
           ADHJNO.moved(lerp(stage0_O3_pos, stage1_ADHJNO_pos)),
           HJKMNO.moved(lerp(stage0_O3_pos, stage1_HJKMNO_pos)) ]
           
stage2 = [ O1.moved(stage0_O1_pos),
           ADHJNO.moved(stage1_ADHJNO_pos),
           HJKMNO.moved(stage1_HJKMNO_pos),
           DEFHJ.moved(stage1_HJKMNO_pos)]

stage3_DHJKM_pos, stage3_DEFHNO_pos = explode_offsets(
    [ DHJKM, DEFHNO], slidable_stage3, stage1_HJKMNO_pos)

stage3 = [ O1.moved(stage0_O1_pos),
           ADHJNO.moved(stage1_ADHJNO_pos),
           DHJKM.moved(lerp(stage1_HJKMNO_pos, stage3_DHJKM_pos)),
           DEFHNO.moved(lerp(stage1_HJKMNO_pos, stage3_DEFHNO_pos))]
           

stage4 = [ O1.moved(stage0_O1_pos),
           ADHJNO.moved(stage1_ADHJNO_pos),
           DEFHNO.moved(stage3_DEFHNO_pos)]

zero = numpy.array([0,0,0])

stage5_ACDHI_pos, stage5_CDFHI_pos = explode_offsets(
    [ ACDHI, CDFHI], slidable_stage5)

stage5 = [ O1.moved(lerp(stage0_O1_pos, zero)),
           ACDHI.moved(lerp(stage5_ACDHI_pos, zero)),
           CDFHI.moved(lerp(stage5_CDFHI_pos, zero)),
           ADHJNO.moved(lerp(stage1_ADHJNO_pos, zero)),
           DEFHNO.moved(lerp(stage3_DEFHNO_pos, zero))]

stage6_O2_pos, stage6_AEFJH_pos, stage6_AFHI_pos = explode_offsets(
    [ O2, AEFJH, AFHI], slidable_stage6)

stage6 = [ O2.moved(lerp(zero, stage6_O2_pos)),
           AEFJH.moved(lerp(zero, stage6_AEFJH_pos)),
           AFHI.moved(lerp(zero, stage6_AFHI_pos)) ]

stage7 = [ O2.moved(stage6_O2_pos),
           AFHI.moved(stage6_AFHI_pos) ]

stage8 = [ O2.moved(stage6_O2_pos),
           FHIKL.moved(stage6_AFHI_pos),
           AFHI.moved(stage6_AFHI_pos) ]

stage9 = [ O2.moved(stage6_O2_pos),
           O4.moved(stage6_AFHI_pos) ]

stages = [
    stage0,
    stage1,
    stage2,
    stage3,
    stage4,
    stage5,
    stage6,
    stage7,
    stage8,
    stage9
]

polyhedra = stages[int(slidable_decomp)]

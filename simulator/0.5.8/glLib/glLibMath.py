try:from glLibLocals import np
except:print "determinant() not available"
from math import *
def sign(num):
    if num < 0: return -1
    return 1
def clamp(value,low,high):
    if type(value)in [type([]),type(())]:
        result = []
        for element in value:
            result.append(clamp(element,low,high))
        return result
    else:
        return min([high,max([low,value])])
def sc_vec(sc,vec):
    result = []
    for component in vec:
        result.append(sc*component)
    return result
def vec_subt(vec1,vec2):
    result = []
    for index in xrange(len(vec1)):
        result.append(vec1[index]-vec2[index])
    return result
def vec_add(vec1,vec2):
    result = []
    for index in xrange(len(vec1)):
        result.append(vec1[index]+vec2[index])
    return result
def vec_div(vec1,vec2):
    result = []
    for index in xrange(len(vec1)):
        result.append(vec1[index]/vec2[index])
    return result
def vec_mult(vec1,vec2):
    result = []
    for index in xrange(len(vec1)):
        result.append(vec1[index]*vec2[index])
    return result
def rndint(num):
    try:return int(round(num))
    except:return [rndint(vec3[0]),
                   rndint(vec3[1]),
                   rndint(vec3[2])]
def length(vec):
    length_sq = 0.0
    for element in vec:
        length_sq += element*element
    return length_sq**0.5
def normalize(vec):
    vec_length = length(vec)
    try:
        result = []
        for element in vec:
            result.append(element/vec_length)
    except:
        return [0,0,0]
    return result
def cross(vec1,vec2):
    return [vec1[1]*vec2[2]-vec1[2]*vec2[1],
            vec1[2]*vec2[0]-vec1[0]*vec2[2],
            vec1[0]*vec2[1]-vec1[1]*vec2[0]]
def dot(vec1,vec2):
    result = 0.0
    for index in xrange(len(vec1)):
        result += vec1[index]*vec2[index]
    return result
def abs_angle_between(vec1,vec2):
    return degrees(acos(dot(vec1,vec2)/(length(vec1)*length(vec2))))
def angle_between_deg(vec1,vec2,perpendicular=[0,1,0]):
    return degrees(angle_between_rad(vec1,vec2,perpendicular))
def angle_between_rad(vec1,vec2,perpendicular=[0,1,0]):
    return atan2(dot(perpendicular,cross(vec1,vec2)),dot(vec1,vec2))
def rotate_arbitrary_deg(point,vec,theta):
    theta = radians(theta)
    return rotate_arbitrary_rad(point,vec,theta)
def rotate_arbitrary_rad(point,vec,theta):
    c = cos(theta)
    s = sin(theta)
    C = 1-c
    x,y,z = vec
    xs = x*s;   ys = y*s;   zs = z*s
    xC = x*C;   yC = y*C;   zC = z*C
    xyC = x*yC; yzC = y*zC; zxC = z*xC
    matrix = [[x*xC+c,xyC-zs,zxC+ys],
              [xyC+zs,y*yC+c,yzC-xs],
              [zxC-ys,yzC+xs,z*zC+c]]
    return glLibMathMultMatrices([[point[0],point[1],point[2]]],matrix)[0]
def glLibMathAugmentMatrix(M,B):
    for r in range(0, len(M)):
        for s in range(0, len(B[r])):
            M[r].append(B[r][s])
    return M
def glLibMathSwapRowMatrix(M,i,j):
    B = M[i]
    M[i] = M[j]
    M[j] = B
    return M
def glLibMathMultMatrices(a,b):
    return [[sum(i*j for i, j in zip(row, col)) for col in zip(*b)] for row in a]
def glLibMathMultRowMatrix(k, M, row):
    for j in range(0, len(M[0])): M[row][j] *= k
    return M
def glLibMathMultRowAddMatrix(k, M, source, dest):
    for j in range(0, len(M[0])): M[dest][j] += M[source][j] * k
    return M
def glLibMathRRefMatrix(M, n = 0):
    if n >= len(M) or n > len(M): return M
    col = -1
    for i in range(n, len(M)):
        if M[i][n] <> 0: col = i
        if col != -1:    break
    if col != n: glLibMathSwapRowMatrix(M, col, n)
    if M[n][n] != 1:
        #M[n][n] = int(M[n][n] * (1. / M[n][n]))
        glLibMathMultRowMatrix(1. / M[n][n], M, n)
    for i in range(0, len(M)):
        if i == n: continue
        if M[i][n] != 0: glLibMathMultRowAddMatrix(-M[i][n], M, n, i)
    glLibMathRRefMatrix(M, n + 1)
    return M
def glLibMathDelColMatrix(B, j):
    for r in range(0,len(B)):
        B[r].pop(j)
    return B
def glLibMathIdentMatrix(size):
    C = []
    for r in range(0, size):
        C.append([])
        for c in range(0, size):
            if c == r: C[r].append(1)
            else:      C[r].append(0)
    return C
def glLibMathGetListMatrix(A):
    A = [[A[0][0],A[0][1],A[0][2],A[0][3]],
         [A[1][0],A[1][1],A[1][2],A[1][3]],
         [A[2][0],A[2][1],A[2][2],A[2][3]],
         [A[3][0],A[3][1],A[3][2],A[3][3]]]
    return A
def glLibMathInvertMatrix(A):
    l = len(A)
    A = glLibMathAugmentMatrix(A,glLibMathIdentMatrix(l))
    A = glLibMathRRefMatrix(A)
    for i in range(0, l):
        A = glLibMathDelColMatrix(A, 0)
    return A
class spline:
    def __init__(self,control_values,loop=False):
        self.control_values = list(control_values)
        if not loop:
            self.control_values = [self.control_values[0]]+self.control_values+[self.control_values[-1]]
        else:
            self.control_values = [self.control_values[-2]]+self.control_values+[self.control_values[1]]
        t=b=c=0
        self.tans = []
        self.tand = []
        for x in xrange(len(self.control_values)-2):
            self.tans.append([])
            self.tand.append([])
        cona = (1-t)*(1+b)*(1-c)*0.5
        conb = (1-t)*(1-b)*(1+c)*0.5
        conc = (1-t)*(1+b)*(1+c)*0.5
        cond = (1-t)*(1-b)*(1-c)*0.5
        i = 1
        while i < len(self.control_values)-1:
            pa = self.control_values[i-1]
            pb = self.control_values[i]
            pc = self.control_values[i+1]
            x1 = pb - pa
            x2 = pc - pb
            self.tans[i-1] = cona*x1+conb*x2
            self.tand[i-1] = conc*x1+cond*x2
            i += 1
    def get_at(self,value):
        num_sections = len(self.control_values) - 3
        index = 1.0 + value*(len(self.control_values)-3.0)
        value = index - int(index)
        index = int(index)
        p0 = self.control_values[index]
        p1 = self.control_values[index+1]
        m0 = self.tand[index-1]
        m1 = self.tans[index]
        h00 = ( 2*(value**3)) - ( 3*(value**2)) + 1
        h10 = ( 1*(value**3)) - ( 2*(value**2)) + value
        h01 = (-2*(value**3)) + ( 3*(value**2))
        h11 = ( 1*(value**3)) - ( 1*(value**2))
        return h00*p0 + h10*m0 + h01*p1 + h11*m1
def determinant(M):
    #http://stackoverflow.com/questions/462500/can-i-get-the-matrix-determinant-by-numpy
    return np.linalg.det(np.array(M))
def polygon_area(points):
    if len(points[0]) == 2:
        #http://www.mathwords.com/a/area_convex_polygon.htm
        points = points + [points[0]]
        area = 0
        for index in xrange(len(points)-1):
            matrix = [[points[index  ][0],points[index  ][1]],
                      [points[index+1][0],points[index+1][1]]]
            det_matrix = determinant(matrix)
            area += det_matrix
        area = 0.5*area
    elif len(points[0]) == 3:
        #http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm
        points = points + [points[0]]
        result = [0.0,0.0,0.0]
        for index in xrange(len(points)-1):
            result = vec_add(result,cross(points[index],points[index+1]))
        normal = normalize(cross(vec_subt(points[0],points[1]),vec_subt(points[1],points[2])))
        area = dot(normal,result)/2.0
    return abs(area)
def triangle_ray(triangle,raypos,raydir):
    #http://geometryalgorithms.com/Archive/algorithm_0105/algorithm_0105.htm#intersect_RayTriangle()
    p1,p2,p3 = triangle
    u = vec_subt(p2,p1)
    v = vec_subt(p3,p1)
    n = normalize(cross(u,v))

    v1 = vec_subt(p1,raypos)

    w0 = VectorSubtract((0,0,0),v1)
    a = -DotProduct(n,w0)
    b = DotProduct(n,raydir)
    if abs(b) <= 0.0: #ray is parallel to triangle plane
        return False #=> no intersect

    #get intersect point of ray with triangle plane
    r = a / b
    if r < 0.0: #ray goes away from triangle
        return False #=> no intersect

    #for a segment, also test if (r > 1.0) => no intersect
    I = vec_add(raydir,sc_vec(r,raydir))#intersect point of ray and plane

    #is I inside the triangle?
    uu = dot(u,u)
    uv = dot(u,v)
    vv = dot(v,v)
    w = vec_subt(I,v1)
    wu = dot(w,u)
    wv = dot(w,v)
    D = uv * uv - uu * vv

    #get and test parametric coords
    s = (uv * wv - vv * wu) / D
    if s < 0.0 or s > 1.0: #I is outside the triangle
        return False #=> no intersect
    t = (uv * wu - uu * wv) / D
    if t < 0.0 or (s + t) > 1.0: #I is outside the triangle
        return False #=> no intersect
 
    I = vec_add(I,raypos)
    return I #I is in the triangle

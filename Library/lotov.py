# A - a matrix of M_{k, n}(R)
# b - a vector of R^k
# v1, v2 - two vectors of R^n
# err (> 0) - the maximal error
# rel - true if the error is relative (err in ]0, 1]), false if absolute (err > 0)
def lotov_algo (A, b, v1, v2, err, rel) :
    #print(b)
    # init
    err = float (err)
    Mnd2d = Matrix ([v1, v2])
    M2dnd = Mnd2d.transpose ()
    
    # 1) first approximation
    dn2d = vector ([0, 1])
    dw2d = vector ([-1, 0])
    ds2d = vector ([0, -1])
    de2d = vector ([1, 0])
    dnnd = M2dnd * dn2d
    dwnd = M2dnd * dw2d
    dsnd = M2dnd * ds2d
    dend = M2dnd * de2d
    # border points calculus
    #print dnnd[0], ' ', dnnd[1], ' ', dnnd[2]
    n = Mnd2d * extreme_point (A, b, dnnd)
    w = Mnd2d * extreme_point (A, b, dwnd)
    s = Mnd2d * extreme_point (A, b, dsnd)
    e = Mnd2d * extreme_point (A, b, dend)
    # calculus of the bounding-box and epsilon if relative err
    if rel :
        xMin = w[0]
        xMax = e[0]
        yMin = s[1]
        yMax = n[1]
        err = max ([xMax - xMin, yMax - yMin]) * err
    # first underapproximation
    fi = [[n, w], [w, s], [s, e], [e, n]]
    # first overapproximation
    oi = [intersection_point (dn2d, n, dw2d, w), intersection_point (dw2d, w, ds2d, s), intersection_point (ds2d, s, de2d, e), intersection_point (de2d, e, dn2d, n)]
    # distances calculus
    di = []
    iMax = 0
    k = 4
    for i in range (0, k) :
        di = di + [point_line_distance (fi[i], oi[i])]
        if (di[i] > di[iMax]) :
            iMax = i
    
    # 2) successive approximations
    while (di[iMax] > err) :
        #print 'k', k
        # refinement
        f = fi[iMax]
        p1 = f[0]
        p2 = f[1]
        d2d = normal_vector (p2 - p1)
        dnd = M2dnd * d2d
        pnd = extreme_point (A, b, dnd)
        p = Mnd2d * pnd
        q = intersection_point (normal_vector (p1 - oi[previous_i (iMax, k)]), p1, d2d, p)
        r = intersection_point (normal_vector (oi[next_i (iMax, k)] - p2), p2, d2d, p)
        # lists update
        fi = [fi[i] for i in range (0, iMax)] + [[p1, p], [p, p2]] + [fi[i] for i in range (iMax + 1, k)]
        oi = [oi[i] for i in range (0, iMax)] + [q, r] + [oi[i] for i in range (iMax + 1, k)]
        dq = point_line_distance ([p1, p], q)
        dr = point_line_distance ([p2, p], r)
        di = [di[i] for i in range (0, iMax)] + [dq, dr] + [di[i] for i in range (iMax + 1, k)]
        k = k + 1
        # next iMax calculus
        iMax = 0
        for i in range (1, k) :
            if (di[i] > di[iMax]) :
                iMax = i
    
    # result packaging and return
    ui = []
    for i in range (0, len (fi)) :
        ui = ui + [fi[i][0]]
    return [oi, ui]





# A - a matrix of M_{k, n}(R)
# b - a vector of R^k
# d - a vector of R^n (direction)
def extreme_point (A, b, d) :
    p = MixedIntegerLinearProgram (maximization = True)
    x = p.new_variable ()
    p.add_constraint (A*x <= b)
    f = 0
    for i in range (0, d.length ()) :
        f = f + d[i]*x[i]
    p.set_objective (f)
    p.solve ()
    l = []
    for i in range (0, d.length ()) :
        l = l + [p.get_values (x[i])]
    return vector (l)




# a1, p1 - a line defined as a1 x = a1 p1
# a2, p2 - a line defined as a2 x = a2 p2
# we assume that a1 and a2 has to be 2d vectors
# if a1 and a2 are colinears, p2 is returned by convention
def intersection_point (a1, p1, a2, p2) :
    M = Matrix ([a1, a2])
    if (M.determinant () == 0) :
        return p2
    else :
        b = vector ([a1.dot_product(p1), a2.dot_product(p2)])
        return M.solve_right (b)




# l = (a, b) - a line defined as a + t (b - a)
# p - a point
# we assume that a and b are 2d vectors
# we assume that p is a 2d point
def point_line_distance (l, p) :
    a = l[0]
    b = l[1]
    n = normal_vector (b - a)
    if (n.norm () != 0) :
        return abs (n.dot_product (p - a)) / n.norm ()
    else :
        return (p - a).norm ()




# v - a 2d vector
def normal_vector (v) :
    return vector ([v[1], -v[0]])




# i - an indice
# n - the maximum indice (excluded)
def next_i (i, n) :
    if (i == n-1) :
        return 0
    else :
        return i+1




# i - an indice
# n - the maximum indice (excluded)
def previous_i (i, n) :
    if (i == 0) :
        return n-1
    else :
        return i-1




# TEST
# lotov_algo (Matrix ([[1, 0], [0, 1], [-1, 0], [0, -1]]), vector ([1, 1, 1, 1]), vector ([1, 0]), vector ([0, 1]))

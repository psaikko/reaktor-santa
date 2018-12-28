from itertools import permutations

#
# Optimize path wrt. swapping two elements
#
def opt2(l, df):
    d = df(l)
    converged = False
    
    while not converged:
        converged = True
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                # swap i, j 
                l[i], l[j] = l[j], l[i]
                d2 = df(l)
                if d2 < d:
                    converged = False
                    d = d2
                else:
                    # swap back if no improvement
                    l[i], l[j] = l[j], l[i]

#
# Optimize path wrt. permutations of three elements
#
def opt3(l, df):
    d = df(l)
    converged = False
    
    while not converged:
        converged = True
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                for k in range(j+1, len(l)):
                    ps = list(permutations([i,j,k]))[1:]
                    for p in ps:
                        i2,j2,k2 = p
                        l2 = l.copy()
                        l2[i], l2[j], l2[k] = l2[i2], l2[j2], l2[k2]
                        d2 = df(l2)
                        if d2 < d:
                            d = d2
                            l[:] = l2
                            converged = False

#
# Optimize path wrt. permutations of four elements
#
def opt4(l, df):
    d = df(l)
    converged = False
    
    while not converged:
        converged = True
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                for k in range(j+1, len(l)):
                    for m in range(k+1, len(l)):
                        ps = list(permutations([i,j,k,m]))[1:]
                        for p in ps:
                            i2,j2,k2,m2 = p
                            l2 = l.copy()
                            l2[i], l2[j], l2[k], l2[m] = l2[i2], l2[j2], l2[k2], l2[m2]
                            d2 = df(l2)
                            if d2 < d:
                                d = d2
                                l[:] = l2
                                converged = False
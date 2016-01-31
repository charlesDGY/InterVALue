def floyd(m):
    n = len(m)
    #m = [[1 for x in range(n)] for y in range(n)]
    D = []
    D.append(m)
    for k in range(1, n):
        #D.append([[float('inf') for x in range(n)] for y in range(n)])
        D.append(D[-1])
        for i in range(1, n):
            for j in range(1, n):
                D[-1][i][j] = min(D[-2][i][j], D[-2][i][k]+D[-2][k][j] )
    return D[-1]




"""m = [[1, float('inf'), 3], [1, 2, float('inf')], [1, float('inf'), 3]]
s = floyd(m)
print  s

if float('inf')>  1:
    print True"""
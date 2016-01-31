def lcm(x, y):
    if x > y:
        greater = x
    else:
        greater = y

    while(True):
        if((greater % x == 0) and (greater % y ==0)):
            lcm = greater
            break
        greater = greater + 1

    return  lcm

L = [3, 6, 7, 9]


def LCM(L):
    i = 0
    temp = lcm(L[i], L[i + 1])
    y = i + 1
    while(True):
        if y < len(L) - 1:
            temp = lcm(temp, L[y + 1])
            y = y + 1
        else:
            break
    return  temp
    print temp

s = LCM(L)
print s
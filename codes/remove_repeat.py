def remove_repeat(a):
    m = 0
    while(m < len(a) - 1):
        if a[m] == a[m + 1]:
            a.remove(a[m + 1])
        else:
            m = m + 1

    return  a
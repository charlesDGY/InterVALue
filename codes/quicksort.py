
def partition(low, high, list):

    pivotkey = list[low]

    while(low < high):
        while(low < high and list[high] >= pivotkey):
            high = high - 1;
        list[low] = list[high]
        while(low < high and list[low] <= pivotkey):
            low = low + 1;
        list[high] = list[low]

    list[low] = pivotkey
    return low

def qsort(low, high, list):
    if(low < high):
        pivotloc = partition(low, high, list)
        qsort(low, pivotloc - 1,list)
        qsort(pivotloc + 1, high, list)
    return list


#list = [49, 38, 65, 97, 76, 13, 27]
#low = 0
#high = len(list) - 1
#qsort(low, high, list)
#qsort(low, high,, list))






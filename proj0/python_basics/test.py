import random

def quickSort(l: list):
    if len(l) <= 1:  
        return
    process(l, 0, len(l) - 1)

def process(l: list, lo: int, hi: int):
    if lo >= hi :
        return
    flag = partition(l, lo, hi)
    process(l, lo, flag - 1)
    process(l, flag + 1, hi)


def partition(l: list, lo: int, hi: int) -> int:
    pivot = l[lo]
    initLo = lo
    while lo <= hi:
        while lo <= hi and l[lo] <= pivot: 
            lo += 1
        while lo <= hi and l[hi] >= pivot:
            hi -= 1
        if lo <= hi:
            l[lo], l[hi] = l[hi], l[lo]
            lo += 1
            hi -= 1
    l[initLo], l[hi] = l[hi], l[initLo]
    return hi

if __name__ == '__main__':
    for i in range(100):
        l = [random.randint(1, 100) for _ in range(random.randint(0, 20))]
        quickSort(l)
        print(l)

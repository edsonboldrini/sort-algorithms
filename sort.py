import argparse
import os
from pathlib import Path
import csv
import time
from multiprocessing import Process

import math
import sys

"""
Sort algorithms
"""
counter = 0
timeout = 30

def selectsort(A, key, start):
    global counter
    counter = 0
    
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for i in range(len(A)):
            if (time.time() - start >= timeout):
                break
            min = i
            for j in range(i+1, len(A)):
                if (time.time() - start >= timeout):
                    break
                if (A[j][key].zfill(len(A[min][key])) < A[min][key].zfill(len(A[j][key]))):
                    min = j
            A = swap(A, i, min)
            counter +=1            

    else:
        for i in range(len(A)):
            if (time.time() - start >= timeout):
                break
            min = i
            for j in range(i+1, len(A)):
                if (time.time() - start >= timeout):
                    break
                if (A[j][key] < A[min][key]):
                    min = j
            A = swap(A, i, min)
            counter +=1            

def insertsort(A, key, start): 
    global counter
    counter = 0    

    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for i in range(1, len(A)):
            if (time.time() - start >= timeout):
                break
            current = A[i]
            j = i - 1
            while(j >= 0 and A[j][key].zfill(len(current[key])) > current[key].zfill(len(A[j][key]))):
                if (time.time() - start >= timeout):
                    break
                A[j+1] = A[j]
                j -= 1
            A[j+1] = current
            counter +=1            
    else:
        for i in range(1, len(A)):
            if (time.time() - start >= timeout):
                break
            current = A[i]
            j = i - 1
            while(j >= 0 and A[j][key] > current[key]):
                if (time.time() - start >= timeout):
                    break
                A[j+1] = A[j]
                j -= 1
            A[j+1] = current
            counter +=1 

    return A           

def mergesortBridge(A, key, start):
    mergesort(A, key, start, 0, len(A)-1)

def mergesort(A, key, start, p, r):
    if (p < r):                     
        q = math.floor((p+r)/2)
        mergesort(A, key, start, p, q)
        mergesort(A, key, start, q+1, r)
        split(A, key, start, p, q, r)

def split(A, key, start, p, q, r):
    global counter
    counter = 0
    L = A[p:q+1]
    R = A[q+1:r+1]
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        A[p:r+1] = mergeNumeric(L,R,key)
    else:
        A[p:r+1] = mergeString(L,R,key)
    return A               

def quicksortBridge(A, key, start):
    quicksort(A, key, start, 0, len(A)-1)

def quicksort(A, key, start, p, r):
    global counter
    counter = 0
    if (p < r):        
        if ( not (time.time() - start >= timeout)):    
            q = partition(A, key, start, p, r)
            quicksort(A, key, start, p, q-1)
            quicksort(A, key, start, q+1, r)

def partition(A, key, start, p, r):
    global counter
    counter = 0
    current = A[r]
    i = p - 1
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for j in range(p, r):
            if (A[j][key].zfill(len(current[key])) <= current[key].zfill(len(A[j][key]))):
                i = i + 1
                swap(A, i, j)
            counter +=1
            if (time.time() - start >= timeout):
                break
        swap(A, i+1, r)
        counter +=1        
        return i + 1
    else:
        for j in range(p, r):
            if (A[j][key] <= current[key]):
                i = i + 1
                swap(A, i, j)
            counter +=1
            if (time.time() - start >= timeout):
                break
        swap(A, i+1, r)
        counter +=1                 
        return i + 1

def heapsort(A, key, start):
    global counter
    counter = 0
    heapsize = len(A)
    buildMaxHeap(A, key, start, heapsize)
    for i in range(len(A)-1, 0, -1):
        swap(A, 0, i)
        heapsize -= 1
        counter +=1
        maxHeapify(A, key, start, 0, heapsize)
        if (time.time() - start >= timeout):
            break

def buildMaxHeap(A, key, start, heapsize):
    for i in range(math.floor(len(A)/2)-1, -1, -1):
        maxHeapify(A, key, start, i, heapsize)
        if (time.time() - start >= timeout):
            break

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2

def maxHeapify(A, key, start, i, heapsize):
    l = left(i)
    r = right(i)

    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        if(l <= heapsize-1 and A[l][key].zfill(len(A[i][key])) > A[i][key].zfill(len(A[l][key]))):
            largest = l
        else:
            largest = i
        if(r <= heapsize-1 and A[r][key].zfill(len(A[largest][key])) > A[largest][key].zfill(len(A[r][key]))):
            largest = r

        if(largest != i):
            swap(A, i, largest)
            if (not (time.time() - start >= timeout)):
                maxHeapify(A, key, start, largest, heapsize)
    else:
        if(l <= heapsize-1 and A[l][key] > A[i][key]):
            largest = l
        else:
            largest = i
        if(r <= heapsize-1 and A[r][key] > A[largest][key]):
            largest = r

        if(largest != i):
            swap(A, i, largest)
            if (not (time.time() - start >= timeout)):
                maxHeapify(A, key, start, largest, heapsize)

# def introsortBridge(A, key, start):
#     maxdepth = math.floor(math.log(len(A))) * 2
#     introsort(A, key, start, maxdepth)

# def introsort(A, key, start, maxdepth):
#     n = len(A)
#     if (maxdepth == 0):
#         heapsort(A, key, start)
#     else:
#         p = partition(A, key, start, 0, len(A))
#         introsort(A[0:p+1], key, start, maxdepth - 1)
#         introsort(A[p+1:n+1], key, start, maxdepth - 1)


def mergeNumeric(L, R, key):
    global counter
    counter = 0
    i = 0
    j = 0
    A = []

    while i < len(L) and j < len(R):
        if (L[i][key].zfill(len(R[j][key])) < R[j][key].zfill(len(L[i][key]))):
            A.append(L[i])
            i += 1
            counter +=1
        elif (L[i][key].zfill(len(R[j][key])) > R[j][key].zfill(len(L[i][key]))):
            A.append(R[j])
            j += 1
            counter +=1
        else:
            A.append(L[i])
            A.append(R[j])
            i += 1
            j += 1
            counter +=2

    while i < len(L):
        A.append(L[i])
        i += 1
        counter +=1

    while j < len(R):
        A.append(R[j])
        j += 1
        counter +=1

    return A        

def mergeString(L, R, key):
    global counter
    counter = 0
    i = 0
    j = 0
    A = []
    while i < len(L) and j < len(R):
        if (L[i][key] < R[j][key]):
            A.append(L[i])
            i += 1
            counter +=1
        elif (L[i][key] > R[j][key]):
            A.append(R[j])
            j += 1
            counter +=1
        else:
            A.append(L[i])
            A.append(R[j])
            i += 1
            j += 1
            counter +=2

    while i < len(L):
        A.append(L[i])
        i += 1
        counter +=1

    while j < len(R):
        A.append(R[j])
        j += 1
        counter +=1

    return A
   

def timsort(A, key, start):
    run = 5
    for i in range(0, len(A), run):
        A[i:i+run] = insertsort(A[i:i+run], key, start)
    runinc = run    
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        while runinc < len(A):        
            for j in range(0, len(A), 2 * runinc): 
                A[j:j+2*runinc] = mergeNumeric(A[j:j + runinc],A[j+runinc:j + 2 * runinc], key)
            runinc *= 2
    else:
        while runinc < len(A):        
            for j in range(0, len(A), 2 * runinc): 
                A[j:j+2*runinc] = mergeString(A[j:j + runinc],A[j+runinc:j + 2 * runinc], key)
            runinc *= 2
        

"""
Utilities functions
"""
def print_test(A, key):
    for i in range(len(A)):
        print(A[i][key])
    print("---")

def csv_to_dataArray(inputName):
    filepath = Path(inputName)
    arrayData = []

    with filepath.open() as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            arrayData.append(row)

    return arrayData

def dataArray_to_csv(A, outputName, header):
    A.insert(0, header)

    file = open(outputName, mode='w')
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in A:
        writer.writerow(row)

def key_to_index(key):
    keys = {
        "email": 0,
        "gender": 1,
        "uid": 2,
        "birthdate": 3,
        "height": 4,
        "weight": 5
        }

    if (key not in keys):
        return 2  # default uid
    else:
        return keys[key]

def print_array(A):
    dash = '-' * 110

    for i in range(len(A)):
        if i == 0:
          print(dash)
          print('{:<35s}{:>12s}{:>9s}{:>24s}{:>15s}{:>12s}'.format(A[i][0],A[i][1],A[i][2],A[i][3], A[i][4], A[i][5]))
          print(dash)
        else:
          print('{:<35s}{:>9s}{:>25s}{:>12s}{:>12s}{:>12s}'.format(A[i][0],A[i][1],A[i][2],A[i][3], A[i][4], A[i][5]))

def swap(A, i, j):
    aux = A[i]
    A[i] = A[j]
    A[j] = aux
    return A

def sort(A, sortAlgorithm, key, start):
    algorithms = {
        "selectsort": selectsort,
        "insertsort": insertsort,
        "mergesort": mergesortBridge,
        "quicksort": quicksortBridge,
        "heapsort": heapsort,
        # "introsort": introsortBridge,
        "timsort": timsort,
    }
    if (sortAlgorithm in algorithms):        
        algorithms[sortAlgorithm](A, key, start)
        # s = lambda sortAlgorithm, A, key : algorithms[sortAlgorithm](A, key)
        # s(sortAlgorithm, A, key)        
        return True
    else:
        print("algorithm not recognized")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm",help="choose an algorithm", required=True)
    parser.add_argument("-k", "--key", help="order by key", required=False)
    parser.add_argument("-i", "--input", help="input file name", required=True)
    parser.add_argument("-o", "--output", help="output file name", required=True)
    args = parser.parse_args()

    sortAlgorithm = args.algorithm
    inputKey = args.key
    inputName = args.input
    outputName = args.output

    if os.path.exists(inputName):
        if ".csv" in inputName:
            if ".csv" not in outputName:
                outputName = outputName + ".csv"

            A = csv_to_dataArray(inputName) # Transform a csv file in a array of data
            header = A[0] # Save header row from array of data
            A.pop(0) # Removing header row from array of data
            key = key_to_index(inputKey) # Getting the index column of the key

            start = time.time() # Starting time
            ordered = sort(A, sortAlgorithm, key, start) # Ordenation step
            end = time.time() # Ending time

            if (ordered):
                dataArray_to_csv(A, outputName, header) # Writing the csv file ordered by the key
                print("{0} {1} {2}".format(sortAlgorithm, counter, (end - start)*1000)) # Report time
                # print_array(A) # Print the array        
        else:
            print("input file is not a valid .csv file")
    else:
        print("input file not found")


if __name__ == "__main__":
    main()    

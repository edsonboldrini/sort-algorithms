import argparse
import os
from pathlib import Path
import csv
import time

import math
import sys

"""
Sort algorithms
"""

def selectionsort(A, key):
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for i in range(len(A)):
            min = i
            for j in range(i+1, len(A)):
                if (A[j][key].zfill(len(A[min][key])) < A[min][key].zfill(len(A[j][key]))):
                    min = j
            A = swap(A, i, min)

    else:
        for i in range(len(A)):
            min = i
            for j in range(i+1, len(A)):
                if (A[j][key] < A[min][key]):
                    min = j
            A = swap(A, i, min)

def insertionsort(A, key):
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for i in range(1, len(A)):
            current = A[i]
            j = i - 1
            while(j >= 0 and A[j][key].zfill(len(current[key])) > current[key].zfill(len(A[j][key]))):
                A[j+1] = A[j]
                j -= 1
            A[j+1] = current
    else:
        for i in range(1, len(A)):
            current = A[i]
            j = i - 1
            while(j >= 0 and A[j][key] > current[key]):
                A[j+1] = A[j]
                j -= 1
            A[j+1] = current

def mergesortBridge(A, key):
    mergesort(A, key, 0, len(A)-1)

def mergesort(A, key, p, r):
    if (p < r):
        q = math.floor((p+r)/2)
        mergesort(A, key, p, q)
        mergesort(A, key, q+1, r)
        merge(A, key, p, q, r)

def merge(A, key, p, q, r):
    L = A[p:q+1]
    R = A[q+1:r+1]

    i = 0
    j = 0
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for k in range(p, r+1):
            if (i < len(L) and j < len(R)):
                if (L[i][key].zfill(len(R[j][key])) < R[j][key].zfill(len(L[i][key]))):
                    A[k] = L[i]
                    i += 1
                else:
                    A[k] = R[j]
                    j += 1
            else:
                if (i == len(L)):
                    A[k] = R[j]
                    j += 1
                else:
                    A[k] = L[i]
                    i += 1
    else:
        for k in range(p, r+1):
            if (i < len(L) and j < len(R)):
                if (L[i][key] < R[j][key]):
                    A[k] = L[i]
                    i += 1
                else:
                    A[k] = R[j]
                    j += 1
            else:
                if (i == len(L)):
                    A[k] = R[j]
                    j += 1
                else:
                    A[k] = L[i]
                    i += 1

def quicksortBridge(A, key):
    quicksort(A, key, 0, len(A)-1)

def quicksort(A, key, p, r):
    if (p < r):
        q = partition(A, key, p, r)
        quicksort(A, key, p, q-1)
        quicksort(A, key, q+1, r)

def partition(A, key, p, r):
    current = A[r]
    i = p - 1
    if (A[0][key].isnumeric() and A[-1][key].isnumeric()):
        for j in range(p, r):
            if (A[j][key].zfill(len(current[key])) <= current[key].zfill(len(A[j][key]))):
                i = i + 1
                swap(A, i, j)
        swap(A, i+1, r)
        return i + 1
    else:
        for j in range(p, r):
            if (A[j][key] <= current[key]):
                i = i + 1
                swap(A, i, j)
        swap(A, i+1, r)
        return i + 1

def heapsort(A, key):
    heapsize = len(A)
    buildMaxHeap(A, key, heapsize)
    for i in range(len(A)-1, 0, -1):
        swap(A, 0, i)
        heapsize -= 1
        maxHeapify(A, key, 0, heapsize)

def buildMaxHeap(A, key, heapsize):
    for i in range(math.floor(len(A)/2)-1, -1, -1):
        maxHeapify(A, key, i, heapsize)

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2

def maxHeapify(A, key, i, heapsize):
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
            maxHeapify(A, key, largest, heapsize)
    else:
        if(l <= heapsize-1 and A[l][key] > A[i][key]):
            largest = l
        else:
            largest = i
        if(r <= heapsize-1 and A[r][key] > A[largest][key]):
            largest = r

        if(largest != i):
            swap(A, i, largest)
            maxHeapify(A, key, largest, heapsize)

"""
Utilities functions
"""

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

def sort(A, sortAlgorithm, key):
    algorithms = {
        "selectsort": selectionsort,
        "insertsort": insertionsort,
        "mergesort": mergesortBridge,
        "quicksort": quicksortBridge,
        "heapsort": heapsort,
    }
    if (sortAlgorithm in algorithms):
        algorithms[sortAlgorithm](A, key)
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
            ordered = sort(A, sortAlgorithm, key) # Ordenation step
            end = time.time() # Ending time

            if (ordered):
                dataArray_to_csv(A, outputName, header) # Writing the csv file ordered by the key
                print("{0} {1} {2}".format(sortAlgorithm, len(A)-1, (end - start)*1000)) # Report time
                print_array(A) # Print the array        
        else:
            print("input file is not a valid .csv file")
    else:
        print("input file not found")


if __name__ == "__main__":
    main()

# Linear Search
array = [x for x in range(1, 1000, 2)]


def linear_search(num, array):
    for i in array:
        if num == i:
            return "Found"
    return "Not found"


# Binary Search
def binary_search(num, array):
    start = 0
    end = len(array) - 1

    while start <= end:
        mid = (start + end) // 2
        mid_value = array[mid]

        if num == mid_value:
            return "Found"
        elif num > mid_value:
            start = mid + 1
        elif num < mid_value:
            end = mid - 1
    return "Not Found"

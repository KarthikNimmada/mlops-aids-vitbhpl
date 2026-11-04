"""Implementations of common sorting algorithms.

Each function returns a sorted copy of the input and leaves it unchanged.
"""


def insertion_sort(items):
	"""Sort values with insertion sort (O(n^2) time, O(n) copy space)."""
	result = list(items)
	for index in range(1, len(result)):
		value = result[index]
		position = index - 1
		while position >= 0 and result[position] > value:
			result[position + 1] = result[position]
			position -= 1
		result[position + 1] = value
	return result


def bubble_sort(items):
	"""Sort values with bubble sort (O(n^2) worst-case time)."""
	result = list(items)
	for end in range(len(result) - 1, 0, -1):
		swapped = False
		for index in range(end):
			if result[index] > result[index + 1]:
				result[index], result[index + 1] = result[index + 1], result[index]
				swapped = True
		if not swapped:
			break
	return result


def quick_sort(items):
	"""Sort values with quick sort (average O(n log n), worst O(n^2))."""
	result = list(items)

	def partition(low, high):
		pivot = result[high]
		boundary = low
		for index in range(low, high):
			if result[index] <= pivot:
				result[boundary], result[index] = result[index], result[boundary]
				boundary += 1
		result[boundary], result[high] = result[high], result[boundary]
		return boundary

	def sort_range(low, high):
		if low < high:
			pivot_index = partition(low, high)
			sort_range(low, pivot_index - 1)
			sort_range(pivot_index + 1, high)

	sort_range(0, len(result) - 1)
	return result


def merge_sort(items):
	"""Sort values with stable merge sort (O(n log n) time and space)."""
	values = list(items)
	if len(values) <= 1:
		return values

	middle = len(values) // 2
	left = merge_sort(values[:middle])
	right = merge_sort(values[middle:])
	merged = []
	left_index = right_index = 0

	while left_index < len(left) and right_index < len(right):
		if left[left_index] <= right[right_index]:
			merged.append(left[left_index])
			left_index += 1
		else:
			merged.append(right[right_index])
			right_index += 1

	merged.extend(left[left_index:])
	merged.extend(right[right_index:])
	return merged

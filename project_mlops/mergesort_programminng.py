from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")


def merge_sort(
	values: Sequence[T], *, key: Callable[[T], K] | None = None
) -> list[T]:
	"""Return a stable sorted copy of values using merge sort.

	Time complexity: O(n log n); auxiliary space: O(n).
	"""
	items = list(values)
	if len(items) < 2:
		return items

	key_fn = key if key is not None else lambda item: item
	auxiliary = items.copy()

	def sort(start: int, end: int) -> None:
		if end - start < 2:
			return

		middle = (start + end) // 2
		sort(start, middle)
		sort(middle, end)

		if key_fn(items[middle - 1]) <= key_fn(items[middle]):
			return

		auxiliary[start:end] = items[start:end]
		left, right = start, middle
		for index in range(start, end):
			if left == middle:
				items[index] = auxiliary[right]
				right += 1
			elif right == end:
				items[index] = auxiliary[left]
				left += 1
			elif key_fn(auxiliary[left]) <= key_fn(auxiliary[right]):
				items[index] = auxiliary[left]
				left += 1
			else:
				items[index] = auxiliary[right]
				right += 1

	sort(0, len(items))
	return items


if __name__ == "__main__":
	sample = [38, 27, 43, 3, 9, 82, 10]
	print(merge_sort(sample))

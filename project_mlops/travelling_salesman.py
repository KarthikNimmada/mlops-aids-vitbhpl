"""Exact Traveling Salesman Problem solver using the Held–Karp algorithm."""

from math import isfinite
from typing import Sequence


def solve_tsp(distance_matrix: Sequence[Sequence[float]]) -> tuple[list[int], float]:
	"""Return the minimum-cost tour and its cost.

	The tour starts and ends at city 0. The distance matrix may be asymmetric.
	This exact dynamic-programming algorithm takes O(n^2 * 2^n) time and
	O(n * 2^n) space.

	An empty matrix returns ``([], 0.0)``. A single-city matrix returns
	``([0, 0], 0.0)``.
	"""
	n = len(distance_matrix)
	if n == 0:
		return [], 0.0

	costs: list[list[float]] = []
	for row in distance_matrix:
		if len(row) != n:
			raise ValueError("distance_matrix must be square")
		try:
			converted = [float(value) for value in row]
		except (TypeError, ValueError) as exc:
			raise ValueError("distance_matrix must contain numeric costs") from exc
		if not all(isfinite(value) for value in converted):
			raise ValueError("distance_matrix costs must be finite")
		costs.append(converted)

	if n == 1:
		return [0, 0], 0.0

	# dp[(mask, last)] = (minimum cost from city 0, predecessor city).
	dp: dict[tuple[int, int], tuple[float, int]] = {}
	for city in range(1, n):
		dp[(1 << city, city)] = (costs[0][city], 0)

	full_mask = (1 << n) - 2  # All cities other than the fixed start city 0.
	for mask in range(1, full_mask + 1):
		if mask & 1:
			continue
		for last in range(1, n):
			last_bit = 1 << last
			if not (mask & last_bit) or mask == last_bit:
				continue
			previous_mask = mask ^ last_bit
			best_cost = float("inf")
			best_previous = 0
			for previous in range(1, n):
				if previous_mask & (1 << previous):
					candidate = dp[(previous_mask, previous)][0] + costs[previous][last]
					if candidate < best_cost:
						best_cost = candidate
						best_previous = previous
			dp[(mask, last)] = (best_cost, best_previous)

	best_cost = float("inf")
	last_city = 0
	for city in range(1, n):
		candidate = dp[(full_mask, city)][0] + costs[city][0]
		if candidate < best_cost:
			best_cost = candidate
			last_city = city

	reversed_path = [last_city]
	mask = full_mask
	while mask != (1 << last_city):
		previous = dp[(mask, last_city)][1]
		mask ^= 1 << last_city
		last_city = previous
		reversed_path.append(last_city)

	return [0, *reversed(reversed_path), 0], best_cost


if __name__ == "__main__":
	example = [
		[0, 10, 15, 20],
		[10, 0, 35, 25],
		[15, 35, 0, 30],
		[20, 25, 30, 0],
	]
	route, cost = solve_tsp(example)
	print(f"Shortest tour: {route}")
	print(f"Total cost: {cost:g}")

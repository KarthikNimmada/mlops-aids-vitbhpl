# Python OOP Best Practices

- Give each class one clear responsibility.
- Prefer composition over deep inheritance; use inheritance for genuine “is-a” relationships.
- Initialize required state in `__init__` and keep objects valid after construction.
- Avoid mutable default arguments. Use `None` or `field(default_factory=...)` for per-instance collections.
- Encapsulate state when necessary to protect invariants. A leading underscore marks an implementation detail by convention.
- Use instance methods for object behavior, class methods for class-level operations or alternate constructors, and static methods only for related utilities without state.
- Use `@dataclass` for classes primarily holding data.
- Use type hints and clear names to make interfaces easier to understand.
- Keep subclasses compatible with the expectations of their base classes.
- Prefer simple attributes over properties unless validation, computed values, or compatibility requires a property.
- Use context managers (`with`) to manage files and other resources reliably.
- Test public behavior and important edge cases rather than relying on private implementation details.

## Example

```python
from dataclasses import dataclass, field


@dataclass
class Task:
	title: str
	tags: list[str] = field(default_factory=list)

	def add_tag(self, tag: str) -> None:
		normalized = tag.strip().lower()
		if not normalized:
			raise ValueError("Tag cannot be empty")
		self.tags.append(normalized)
```

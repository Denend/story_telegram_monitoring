from enum import Enum

class TextAdmin(Enum):

	def format_text(self, **kwargs) -> str:
		try:
			return self.value.format(**kwargs)
		except KeyError as e:
			raise ValueError(f"Missing key for formatting: {e}") from None

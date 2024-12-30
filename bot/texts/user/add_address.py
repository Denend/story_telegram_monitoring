from enum import Enum

class TextAddAddress(Enum):
	ADDRESS = "Enter your validator address <b>story testnet</b>:"
	SUCCESSFUL = "The validator's address has been successfully linked."

	def format_text(self, **kwargs) -> str:
		try:
			return self.value.format(**kwargs)
		except KeyError as e:
			raise ValueError(f"Missing key for formatting: {e}") from None

class TextAddAddressError(Enum):
	INVALID_ADDRESS = "Invalid validator address, please try again:"

	def format_text(self, **kwargs) -> str:
		try:
			return self.value.format(**kwargs)
		except KeyError as e:
			raise ValueError(f"Missing key for formatting: {e}") from None

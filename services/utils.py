from pathlib import Path

def get_absolute_dir(*path_parts: str) -> Path:
	return Path().resolve() / Path(*path_parts)


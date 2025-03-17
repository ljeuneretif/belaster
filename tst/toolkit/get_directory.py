
from pathlib import Path


def get_directory(f):
	return str(Path(f).parent.resolve())

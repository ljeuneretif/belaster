
from .application_context_binder import ApplicationContextBinder
from importlib.machinery import SourceFileLoader
from os.path import dirname
from pathlib import Path
from types import ModuleType



BELASTER_FILE_DEFAULT_NAME = "Belaster"
USER_BELASTER_MODULE_NAME = "user_belaster_module"



def _append_default_belaster_file_name(dir: str):
	return dir + "/" + BELASTER_FILE_DEFAULT_NAME


def is_belaster_file_path(path: str):
	return Path(path).is_file() or Path(_append_default_belaster_file_name(path)).is_file()


class PathBelasterFileError(Exception):
	__slots__ = ("path")

	def __init__(self, path, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.path = path


def make_belaster_file_path(path: str):
	if Path(path).is_file():
		return path
	else:
		p = _append_default_belaster_file_name(path)
		if Path(p).is_file():
			return p
	raise PathBelasterFileError(path)



def _load_module(path):
	loader = SourceFileLoader(USER_BELASTER_MODULE_NAME, path)
	result = ModuleType(loader.name)
	loader.exec_module(result)
	return result



def import_belaster_file(path: str):
	belaster_file_path = make_belaster_file_path(path)

	print(f"Using User's Belaster script at {belaster_file_path}")

	ApplicationContextBinder.application_context.belaster_file_directory = dirname(belaster_file_path)

	user_belaster_module = _load_module(belaster_file_path)

	if user_belaster_module is None:
		raise RuntimeError(f"Cannot load the module at {belaster_file_path}. Aborting.")

	return user_belaster_module

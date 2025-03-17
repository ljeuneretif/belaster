
from .application_context_binder import ApplicationContextBinder
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import ModuleType



USER_BELASTER_MODULE_NAME = "user_belaster_module"


def _load_module(path):
	loader = SourceFileLoader(USER_BELASTER_MODULE_NAME, path)
	result = ModuleType(loader.name)
	loader.exec_module(result)
	return result


BELASTER_FILE_DEFAULT_NAME = "Belaster"


def import_belaster_file(path: str, filename: str):
	belaster_file_path = path + "/" + filename

	if not Path(belaster_file_path).is_file():
		raise RuntimeError(f"Not a file at {belaster_file_path}")

	print(f"User's Belaster file at {belaster_file_path}")

	ApplicationContextBinder.application_context.belaster_file_directory = path

	user_belaster_module = None

	try:
		user_belaster_module = _load_module(belaster_file_path)
	except FileNotFoundError:
		print(f"No Belaster file at {belaster_file_path}. Aborting.")
		exit()

	if user_belaster_module is None:
		raise RuntimeError(f"Cannot load the module at {belaster_file_path}. Aborting.")
	return user_belaster_module

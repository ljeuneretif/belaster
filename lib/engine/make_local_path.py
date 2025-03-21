
from .application_context_binder import ApplicationContextBinder


def make_local_path(path):
	return ApplicationContextBinder.application_context.belaster_file_directory + "/" + path

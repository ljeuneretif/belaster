
from os import getcwd
from belaster.engine.application_context import ApplicationContext
from belaster.engine.application_context_binder import ApplicationContextBinder
from belaster.engine.import_belaster_file import BELASTER_FILE_DEFAULT_NAME, import_belaster_file
from belaster.engine.mute_stdout import MuteStdout
from os.path import relpath
from toolkit import get_directory



def test_relative_path():
	current_directory = get_directory(__file__)

	context = ApplicationContext()
	ApplicationContextBinder.application_context = context

	with MuteStdout():
		import_belaster_file(
			path=current_directory + "/../other",
			filename=BELASTER_FILE_DEFAULT_NAME
			)
	
	expected = relpath(path=current_directory + "/../other/abc", start=getcwd())
	
	assert [str(a) for a in context.all_atoms] == [expected]

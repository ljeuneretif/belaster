
from belaster.engine.application_context import ApplicationContext
from belaster.engine.application_context_binder import ApplicationContextBinder
from belaster.engine.belaster_file import import_belaster_file, make_belaster_file_path
from belaster.engine.mute_stdout import MuteStdout
from toolkit import get_directory



def test_application_context_2_rule():
	current_directory = get_directory(__file__)

	context = ApplicationContext()
	ApplicationContextBinder.application_context = context

	with MuteStdout():
		import_belaster_file(path=make_belaster_file_path(current_directory))

	assert len(context.all_atoms) == 2


from belaster.engine.application_context import ApplicationContext
from belaster.engine.application_context_binder import ApplicationContextBinder
from belaster.engine.import_belaster_file import BELASTER_FILE_DEFAULT_NAME, import_belaster_file
from belaster.engine.mute_stdout import MuteStdout
from toolkit import get_directory



def test_application_context_1_rule():
	current_directory = get_directory(__file__)

	context = ApplicationContext()
	ApplicationContextBinder.application_context = context

	with MuteStdout():
		import_belaster_file(path=current_directory, filename=BELASTER_FILE_DEFAULT_NAME)

	assert len(context.all_atoms) == 1

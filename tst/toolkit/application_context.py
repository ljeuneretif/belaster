
from belaster.engine.application_context import ApplicationContext
from belaster.engine.application_context_binder import ApplicationContextBinder
from os import getcwd
from pytest import fixture



@fixture
def application_context():
	context = None
	if ApplicationContextBinder.application_context is None:
		context = ApplicationContext()
		context.belaster_file_directory = getcwd()
		ApplicationContextBinder.application_context = context
	else:
		context = ApplicationContextBinder.application_context

	yield context

	ApplicationContextBinder.application_context = None
	del context


from .application_context import application_context
from .arguments import arguments
from pytest import fixture



@fixture
def verify_environment(arguments):
	def result(args, environment):
		arguments.initialize(args)
		arguments.parse()
		assert arguments.goals == []
		assert arguments.environment == environment
	return result

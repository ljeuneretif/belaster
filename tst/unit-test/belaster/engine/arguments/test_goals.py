
from belaster.engine.arguments import ArgumentNotRecognizedError
from pytest import fixture, raises
from toolkit import application_context, arguments, t0, t1


@fixture
def verify_goals(arguments):
	def result(args, goals):
		arguments.initialize(args)
		arguments.parse()
		assert arguments.goals == goals
		assert arguments.environment == {}
	return result



def test_no_args(verify_goals, t0):
	verify_goals([], [])


def test_unrecognized_goal(arguments, t0):
	arg = "z"
	arguments.initialize([arg])
	with raises(ArgumentNotRecognizedError) as error:
		arguments.parse()

		error.arg == arg


def test_1_target(verify_goals, t0):
	verify_goals(["a"], [t0])


def test_1_target_twice(verify_goals, t0):
	verify_goals(["a", "a"], [t0, t0])


def test_2_targets_1(verify_goals, t0, t1):
	verify_goals(["a"], [t0])


def test_2_targets_2(verify_goals, t0, t1):
	verify_goals(["a", "b"], [t0, t1])

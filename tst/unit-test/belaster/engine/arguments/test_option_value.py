
from belaster import ArgumentMissingValueError, OptionValue
from pytest import fixture, raises
from toolkit import application_context, arguments, verify_environment



VAR_OPTION_VALUE_1 = "VAR_OPTION_VALUE_1"
VAR_OPTION_VALUE_2 = "VAR_OPTION_VALUE_2"



@fixture
def option_value_1(application_context):
	def result(names, type):
		return OptionValue(names=names, type=type, variable_name=VAR_OPTION_VALUE_1)
	return result


@fixture
def option_value_2(application_context):
	def result(names, type):
		return OptionValue(names=names, type=type, variable_name=VAR_OPTION_VALUE_2)
	return result


# Missing value.
def test_missing_value(arguments, option_value_1):
	option_value_1(names={"-v"}, type=int)
	arguments.initialize(["-v"])
	with raises(ArgumentMissingValueError):
		arguments.parse()


# Different types.
# int
def test_type_int_separated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=int)
	verify_environment(["-v", "1"], {VAR_OPTION_VALUE_1: 1})


def test_type_int_concatenated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=int)
	verify_environment(["-v1"], {VAR_OPTION_VALUE_1: 1})


# str
def test_type_str_separated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=str)
	verify_environment(["-v", "abc"], {VAR_OPTION_VALUE_1: "abc"})


def test_type_str_concatenated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=str)
	verify_environment(["-vabc"], {VAR_OPTION_VALUE_1: "abc"})


# float
def test_type_float_positive_separated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=float)
	verify_environment(["-v", "5.6"], {VAR_OPTION_VALUE_1: 5.6})


def test_type_float_positive_concatenated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=float)
	verify_environment(["-v5.6"], {VAR_OPTION_VALUE_1: 5.6})


def test_type_float_negative_separated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=float)
	verify_environment(["-v", "-5.6"], {VAR_OPTION_VALUE_1: -5.6})


def test_type_float_negative_concatenated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=float)
	verify_environment(["-v-5.6"], {VAR_OPTION_VALUE_1: -5.6})


# custom
class Scalar():
	__slots__ = ("s")
	def __init__(self, s):
		self.s = s


def test_type_custom_type_separated(arguments, option_value_1):
	option_value_1(names={"-v"}, type=Scalar)
	arguments.initialize(["-v", "abc"])
	arguments.parse()

	assert isinstance(arguments.environment[VAR_OPTION_VALUE_1], Scalar)
	assert arguments.environment[VAR_OPTION_VALUE_1].s == "abc"


def test_type_custom_type_concatenated(arguments, option_value_1):
	option_value_1(names={"-v"}, type=Scalar)
	arguments.initialize(["-vabc"])
	arguments.parse()

	assert isinstance(arguments.environment[VAR_OPTION_VALUE_1], Scalar)
	assert arguments.environment[VAR_OPTION_VALUE_1].s == "abc"


# Value separated or concatenated.
def test_short_concatenated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=int)
	verify_environment(["-v1"], {VAR_OPTION_VALUE_1: 1})


def test_short_separated(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=int)
	verify_environment(["-v", "1"], {VAR_OPTION_VALUE_1: 1})


def test_long_concatenated(verify_environment, option_value_1):
	option_value_1(names={"--value"}, type=int)
	verify_environment(["--value1"], {VAR_OPTION_VALUE_1: 1})


def test_long_separated(verify_environment, option_value_1):
	option_value_1(names={"--value"}, type=int)
	verify_environment(["--value", "1"], {VAR_OPTION_VALUE_1: 1})


# Multiple values.
def test_2_values(verify_environment, option_value_1):
	option_value_1(names={"-v"}, type=int)
	verify_environment(["-v1", "-v2"], {VAR_OPTION_VALUE_1: 2})


# Mix of OptionValue.
def test_2_options(verify_environment, option_value_1, option_value_2):
	option_value_1(names={"-v"}, type=int)
	option_value_2(names={"-w"}, type=float)
	verify_environment(["-v1", "-w4.5"], {VAR_OPTION_VALUE_1: 1, VAR_OPTION_VALUE_2: 4.5})

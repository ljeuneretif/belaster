
from belaster import ArgumentMissingValueError, OptionContainer
from pytest import raises
from toolkit import application_context, arguments, verify_environment



VAR_OPTION_CONTAINER_1 = "VAR_OPTION_CONTAINER_1"
VAR_OPTION_CONTAINER_2 = "VAR_OPTION_CONTAINER_2"



# Bad parameters.
def test_separator_first_none(arguments):
	with raises(ValueError):
		OptionContainer(
			names={"-c"}, separator_first=None, separator_middle=",",
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
			)


def test_separator_first_empty(arguments):
	with raises(ValueError):
		OptionContainer(
			names={"-c"}, separator_first="", separator_middle=",",
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
			)


def test_separator_first_length_more_than_1(arguments):
	with raises(ValueError):
		OptionContainer(
			names={"-c"}, separator_first="ab", separator_middle=",",
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
			)


def test_separator_middle_none(arguments):
	with raises(ValueError):
		OptionContainer(
			names={"-c"}, separator_first="=", separator_middle=None,
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
			)


def test_separator_middle_empty(arguments):
	with raises(ValueError):
		OptionContainer(
			names={"-c"}, separator_first="=", separator_middle="",
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
			)


def test_separator_middle_length_more_than_1(arguments):
	with raises(ValueError):
		OptionContainer(
			names={"-c"}, separator_first="=", separator_middle="ab",
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
			)


# Missing value.
def test_missing_value(arguments):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	arguments.initialize(["-c"])
	with raises(ArgumentMissingValueError):
		arguments.parse()


# 1 value.
def test_none(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment([], {VAR_OPTION_CONTAINER_1: []})


def test_empty_container(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c="], {VAR_OPTION_CONTAINER_1: []})


def test_container_length_1_separated(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c", "=5"], {VAR_OPTION_CONTAINER_1: [5]})


def test_container_length_1_concatenated(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c=5"], {VAR_OPTION_CONTAINER_1: [5]})


def test_container_length_2(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c=7,2"], {VAR_OPTION_CONTAINER_1: [7, 2]})


def test_container_length_3(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c=5,9,2"], {VAR_OPTION_CONTAINER_1: [5, 9, 2]})


# Various combinations of containers, data types and separators.
class Scalar():
	__slots__ = ("s")
	def __init__(self, s):
		self.s = int(s)


class Container():
	__slots__ = ("l")
	def __init__(self, l):
		self.l = list(l)



def test_container_list_int(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=":",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c=5:9:2"], {VAR_OPTION_CONTAINER_1: [5, 9, 2]})


def test_container_list_float(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="?", separator_middle="=",
		type_container=list, type_scalar=float, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c?-5.6=4.3=2.22"], {VAR_OPTION_CONTAINER_1: [-5.6, 4.3, 2.22]})


def test_container_list_str(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="!", separator_middle=";",
		type_container=list, type_scalar=str, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-c!abc;def;hg"], {VAR_OPTION_CONTAINER_1: ["abc", "def", "hg"]})


def test_container_set_int(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="m", separator_middle="o",
		type_container=set, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-cm5o9o2"], {VAR_OPTION_CONTAINER_1: {5, 9, 2}})


def test_container_tuple_int(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="m", separator_middle="o",
		type_container=tuple, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(["-cm5o9o2"], {VAR_OPTION_CONTAINER_1: (5, 9, 2)})


def test_container_custom_custom(arguments):
	OptionContainer(
		names={"-c"}, separator_first="m", separator_middle="o",
		type_container=Container, type_scalar=Scalar, variable_name=VAR_OPTION_CONTAINER_1
		)
	arguments.initialize(["-cm5o9o2"])
	arguments.parse()

	c = arguments.environment[VAR_OPTION_CONTAINER_1]
	assert isinstance(c, Container)
	for s in c.l:
		assert isinstance(s, Scalar)
	assert [s.s for s in c.l] == [5, 9, 2]


# Scattered elements.
def test_container_scattered(verify_environment):
	OptionContainer(
		names={"-c", "--container"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	verify_environment(
		["-c=5,9,2", "--container=8,7,6", "--container=3"],
		{VAR_OPTION_CONTAINER_1: [5, 9, 2, 8, 7, 6, 3]}
	)


# 2 OptionContainer.
def test_2_option_containers(verify_environment):
	OptionContainer(
		names={"-c"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	OptionContainer(
		names={"-d"}, separator_first=",", separator_middle="?",
		type_container=list, type_scalar=float, variable_name=VAR_OPTION_CONTAINER_2
		)
	verify_environment(
		["-c", "=3,8,1", "-d,-6.7?9?3.21"],
		{
			VAR_OPTION_CONTAINER_1: [3, 8, 1],
			VAR_OPTION_CONTAINER_2: [-6.7, 9, 3.21],
		}
	)


def test_2_option_containers_scattered(verify_environment):
	OptionContainer(
		names={"-c", "--container"}, separator_first="=", separator_middle=",",
		type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	OptionContainer(
		names={"-d", "--other"}, separator_first=",", separator_middle="?",
		type_container=list, type_scalar=float, variable_name=VAR_OPTION_CONTAINER_2
		)
	verify_environment(
		["--container", "=3,8,1", "-d,-6.7?9?3.21", "-c=6,3", "--other,0.8?.001"],
		{
			VAR_OPTION_CONTAINER_1: [3, 8, 1, 6, 3],
			VAR_OPTION_CONTAINER_2: [-6.7, 9, 3.21, 0.8, 0.001],
		}
	)


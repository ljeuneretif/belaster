
from belaster import ArgumentMissingValueError, OptionEnum
from enum import Enum
from pytest import raises
from toolkit import application_context, arguments, verify_environment



VAR_OPTION_ENUM_1 = "ENUM_1"
VAR_OPTION_ENUM_2 = "ENUM_2"



ENUM_SAMPLE_1_A = 20
ENUM_SAMPLE_1_B = 45
ENUM_SAMPLE_1_C = 90

class EnumSample1(Enum):
	A = ENUM_SAMPLE_1_A
	B = ENUM_SAMPLE_1_B
	C = ENUM_SAMPLE_1_C


ENUM_SAMPLE_2_A = -2.3
ENUM_SAMPLE_2_B = 5.9
ENUM_SAMPLE_2_C = -7.1

class EnumSample2(Enum):
	A = ENUM_SAMPLE_2_A
	B = ENUM_SAMPLE_2_B
	C = ENUM_SAMPLE_2_C


# Missing value.
def test_missing_value(arguments):
	OptionEnum(names={"-e"}, enum=EnumSample1, variable_name=VAR_OPTION_ENUM_1)
	arguments.initialize(["-e"])
	with raises(ArgumentMissingValueError):
		arguments.parse()


# 1 value.
def test_none(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, variable_name=VAR_OPTION_ENUM_1)
	verify_environment([], {VAR_OPTION_ENUM_1: None})


def test_1_short_key_no_symbol_separated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e", "A"], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_key_no_symbol_concatenated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-eA"], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_key_with_symbol_separated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, symbol_for_key="=", variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e", "=A"], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_key_with_symbol_concatenated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, symbol_for_key="=", variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e=A"], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_value_no_symbol_separated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, symbol_for_value="[",
						is_default_key=False, variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e", "[" + str(ENUM_SAMPLE_1_A)], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_value_no_symbol_concatenated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, symbol_for_value="[",
						is_default_key=False, variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e[" + str(ENUM_SAMPLE_1_A)], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_value_with_symbol_separated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, symbol_for_value="[", variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e", "[" + str(ENUM_SAMPLE_1_A)], {VAR_OPTION_ENUM_1: EnumSample1.A})


def test_1_short_value_with_symbol_concatenated(verify_environment):
	OptionEnum(names={"-e"}, enum=EnumSample1, symbol_for_value="[", variable_name=VAR_OPTION_ENUM_1)
	verify_environment(["-e[" + str(ENUM_SAMPLE_1_A)], {VAR_OPTION_ENUM_1: EnumSample1.A})


# More values.
def test_2_values(verify_environment):
	OptionEnum(names={"-a"}, enum=EnumSample1, variable_name=VAR_OPTION_ENUM_1)
	OptionEnum(names={"-b"}, enum=EnumSample2, symbol_for_value="'", variable_name=VAR_OPTION_ENUM_2)
	verify_environment(
		["-aA", "-b", "'" + str(ENUM_SAMPLE_2_C)],
		{
			VAR_OPTION_ENUM_1: EnumSample1.A,
			VAR_OPTION_ENUM_2: EnumSample2.C
		}
		)

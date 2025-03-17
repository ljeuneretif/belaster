
from belaster import Abstract, OptionContainer, OptionCount, OptionEnd, OptionEnum, OptionFlag, OptionValue
from enum import Enum
from pytest import fixture
from toolkit import application_context, arguments



@fixture
def verify(arguments):
	def result(args, goals, environment):
		arguments.initialize(args)
		arguments.parse()
		assert arguments.goals == goals
		assert arguments.environment == environment
	return result



ABSTRACT_1 = "all"
ABSTRACT_2 = "clean"

VAR_OPTION_CONTAINER_1 = "VAR_OPTION_CONTAINER_1"
VAR_OPTION_CONTAINER_2 = "VAR_OPTION_CONTAINER_2"

VAR_OPTION_COUNT_1 = "VAR_OPTION_COUNT_1"
VAR_OPTION_COUNT_2 = "VAR_OPTION_COUNT_2"

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

VAR_OPTION_ENUM_1 = "VAR_OPTION_ENUM_1"
VAR_OPTION_ENUM_2 = "VAR_OPTION_ENUM_2"

VAR_OPTION_FLAG_1 = "VAR_OPTION_FLAG_1"
VAR_OPTION_FLAG_2 = "VAR_OPTION_FLAG_2"

VAR_OPTION_VALUE_1 = "VAR_OPTION_VALUE_1"
VAR_OPTION_VALUE_2 = "VAR_OPTION_VALUE_2"



def test_all_1(verify):
	all = Abstract(ABSTRACT_1)
	clean = Abstract(ABSTRACT_2)

	OptionContainer(
			names={"+c", "--container1"}, separator_first="=", separator_middle=",",
			type_container=list, type_scalar=int, variable_name=VAR_OPTION_CONTAINER_1
		)
	OptionContainer(
			names={"-d", "--container2"}, separator_first="?", separator_middle=":",
			type_container=set, type_scalar=float, variable_name=VAR_OPTION_CONTAINER_2
		)
	
	OptionCount(names={"+a", "--count1"}, variable_name=VAR_OPTION_COUNT_1)
	OptionCount(names={"+b", "--count2"}, variable_name=VAR_OPTION_COUNT_2)

	OptionEnd(names={"++"})

	OptionEnum(
			names={"-e", "--enum1"}, enum=EnumSample1, symbol_for_key="=", symbol_for_value=")",
			is_default_key=True, variable_name=VAR_OPTION_ENUM_1
		)
	OptionEnum(
			names={"-f", "--enum2"}, enum=EnumSample2, symbol_for_key="?", symbol_for_value="[",
			is_default_key=False, variable_name=VAR_OPTION_ENUM_2
		)

	OptionFlag(names={"-g", "--flag1"}, variable_name=VAR_OPTION_FLAG_1)
	OptionFlag(names={"-h", "--flag2"}, variable_name=VAR_OPTION_FLAG_2)

	OptionValue(names={"-i", "--value1"}, type=str, variable_name=VAR_OPTION_VALUE_1)
	OptionValue(names={"-j", "--value2"}, type=complex, variable_name=VAR_OPTION_VALUE_2)

	# breakpoint()

	verify(
		[
			"+bc=7,3,1", "--enum1B", "-gj3-4j", "-f[-7.1", "all", "--count1",
			"--container2?6:-8.09:3.4:0", "--container1=6,4,8", "-ixyz",
			"+baa+", "clean", "all"
		],
		[
			all, clean, all
		],
		{
			VAR_OPTION_CONTAINER_1: [7, 3, 1, 6, 4, 8],
			VAR_OPTION_CONTAINER_2: {6, -8.09, 3.4, 0},

			VAR_OPTION_COUNT_1: 3,
			VAR_OPTION_COUNT_2: 2,

			VAR_OPTION_ENUM_1: EnumSample1.B,
			VAR_OPTION_ENUM_2: EnumSample2.C,

			VAR_OPTION_FLAG_1: True,
			VAR_OPTION_FLAG_2: False,

			VAR_OPTION_VALUE_1: "xyz",
			VAR_OPTION_VALUE_2: complex(3, -4)
		}
	)

	


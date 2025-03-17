
from belaster import OptionCount
from pytest import fixture
from toolkit import application_context, arguments, verify_environment



VAR_OPTION_COUNT_1 = "COUNT_1"
VAR_OPTION_COUNT_2 = "COUNT_2"


@fixture
def option_count_1(application_context):
	def result(names):
		return OptionCount(names=names, variable_name=VAR_OPTION_COUNT_1)
	return result


@fixture
def option_count_2(application_context):
	def result(names):
		return OptionCount(names=names, variable_name=VAR_OPTION_COUNT_2)
	return result



def test_none(verify_environment, option_count_1):
	option_count_1({"-c"})
	verify_environment([], {VAR_OPTION_COUNT_1: 0})


def test_1_short_1(verify_environment, option_count_1):
	option_count_1({"-c"})
	verify_environment(["-c"], {VAR_OPTION_COUNT_1: 1})


def test_1_short_2_separated(verify_environment, option_count_1):
	option_count_1({"-c"})
	verify_environment(["-c", "-c"], {VAR_OPTION_COUNT_1: 2})


def test_1_short_2_concatenated(verify_environment, option_count_1):
	option_count_1({"-c"})
	verify_environment(["-cc"], {VAR_OPTION_COUNT_1: 2})


def test_1_short_3_separated_concatenated(verify_environment, option_count_1):
	option_count_1({"-c"})
	verify_environment(["-cc", "-c"], {VAR_OPTION_COUNT_1: 3})


def test_1_long_1(verify_environment, option_count_1):
	option_count_1({"--count"})
	verify_environment(["--count"], {VAR_OPTION_COUNT_1: 1})


def test_1_long_2(verify_environment, option_count_1):
	option_count_1({"--count"})
	verify_environment(["--count", "--count"], {VAR_OPTION_COUNT_1: 2})


def test_1_long_short_1_short(verify_environment, option_count_1):
	option_count_1({"-c", "--count"})
	verify_environment(["-c"], {VAR_OPTION_COUNT_1: 1})


def test_1_long_short_1_long(verify_environment, option_count_1):
	option_count_1({"-c", "--count"})
	verify_environment(["--count"], {VAR_OPTION_COUNT_1: 1})


def test_1_long_short_2_mixed(verify_environment, option_count_1):
	option_count_1({"-c", "--count"})
	verify_environment(["-c", "--count"], {VAR_OPTION_COUNT_1: 2})


def test_2_long_short_1_short(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["-c"], {VAR_OPTION_COUNT_1: 1, VAR_OPTION_COUNT_2: 0})


def test_2_long_short_2_short_separated(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["-c", "-d"], {VAR_OPTION_COUNT_1: 1, VAR_OPTION_COUNT_2: 1})


def test_2_long_short_2_short_concatenated(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["-cd"], {VAR_OPTION_COUNT_1: 1, VAR_OPTION_COUNT_2: 1})


def test_2_long_short_1_long(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["--count1"], {VAR_OPTION_COUNT_1: 1, VAR_OPTION_COUNT_2: 0})


def test_2_long_short_2_long(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["--count1", "--count2"], {VAR_OPTION_COUNT_1: 1, VAR_OPTION_COUNT_2: 1})


def test_2_long_short_3_short_concatenated(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["-cdd"], {VAR_OPTION_COUNT_1: 1, VAR_OPTION_COUNT_2: 2})


def test_2_long_short_4_short_concatenated(verify_environment, option_count_1, option_count_2):
	option_count_1({"-c", "--count1"})
	option_count_2({"-d", "--count2"})
	verify_environment(["-cddc"], {VAR_OPTION_COUNT_1: 2, VAR_OPTION_COUNT_2: 2})

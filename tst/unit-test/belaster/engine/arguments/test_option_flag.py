
from belaster import OptionFlag
from pytest import fixture
from toolkit import application_context, arguments, verify_environment



VAR_OPTION_FLAG_1 = "FLAG_1"
VAR_OPTION_FLAG_2 = "FLAG_2"



@fixture
def option_flag_1(application_context):
	def result(names):
		return OptionFlag(names=names, variable_name=VAR_OPTION_FLAG_1)
	return result


@fixture
def option_flag_2(application_context):
	def result(names):
		return OptionFlag(names=names, variable_name=VAR_OPTION_FLAG_2)
	return result



def test_none(verify_environment, option_flag_1):
	option_flag_1({"-f"})
	verify_environment([], {VAR_OPTION_FLAG_1: False})


def test_1_option_flag_short_1(verify_environment, option_flag_1):
	option_flag_1({"-f"})
	verify_environment(["-f"], {VAR_OPTION_FLAG_1: True})


def test_1_option_flag_short_2_separated(verify_environment, option_flag_1):
	option_flag_1({"-f"})
	verify_environment(["-f", "-f"], {VAR_OPTION_FLAG_1: True})


def test_1_option_flag_short_2_concatenated(verify_environment, option_flag_1):
	option_flag_1({"-f"})
	verify_environment(["-ff"], {VAR_OPTION_FLAG_1: True})


def test_1_option_flag_long_1(verify_environment, option_flag_1):
	option_flag_1({"--flag"})
	verify_environment(["--flag"], {VAR_OPTION_FLAG_1: True})


def test_1_option_flag_long_2(verify_environment, option_flag_1):
	option_flag_1({"--flag"})
	verify_environment(["--flag", "--flag"], {VAR_OPTION_FLAG_1: True})

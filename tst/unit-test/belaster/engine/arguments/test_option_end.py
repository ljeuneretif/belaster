
from belaster import ArgumentOptionsEndedError, OptionEnd, OptionFlag
from pytest import raises
from toolkit import application_context, arguments



FLAG_VARIABLE_NAME = "FLAG"



def test_option_end_separated(arguments):
	OptionFlag(names={"-a"}, variable_name = FLAG_VARIABLE_NAME)
	OptionEnd(names={"--"})

	arguments.initialize(["-a", "--"])
	arguments.parse()

	assert arguments.goals == []
	assert arguments.environment == {FLAG_VARIABLE_NAME: True}



def test_option_end_concatenated(arguments):
	OptionFlag(names={"-a"}, variable_name = FLAG_VARIABLE_NAME)
	OptionEnd(names={"--"})

	arguments.initialize(["-a-"])
	arguments.parse()

	assert arguments.goals == []
	assert arguments.environment == {FLAG_VARIABLE_NAME: True}


# Cannot put options after end of options.
def test_cannot_put_options_after_end_separated(arguments):
	OptionFlag(names={"-a"}, variable_name=FLAG_VARIABLE_NAME)
	OptionEnd(names={"--"})
	arguments.initialize(["-a", "--", "-a"])
	with raises(ArgumentOptionsEndedError) as error:
		arguments.parse()

		assert error.arg == "-a"

def test_cannot_put_options_after_end_concatenated(arguments):
	OptionFlag(names={"-a"}, variable_name=FLAG_VARIABLE_NAME)
	OptionEnd(names={"--"})
	arguments.initialize(["-a-a"])
	with raises(ArgumentOptionsEndedError) as error:
		arguments.parse()

		assert error.arg == "-a"

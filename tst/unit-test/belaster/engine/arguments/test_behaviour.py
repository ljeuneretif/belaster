
from belaster import ArgumentExpectedShortOptionError, ArgumentNotRecognizedError, OptionCount, OptionDuplicateVariableError, OptionFlag
from pytest import raises
from toolkit import application_context, arguments



# Duplicate variable.
def test_duplicate_variable(arguments):
	variable_name = "var"
	o1 = OptionFlag(names={"-f"}, variable_name=variable_name)
	with raises(OptionDuplicateVariableError) as error:
		o2 = OptionCount(names={"-c"}, variable_name=variable_name)

		assert error.options == {o1, o2}
		assert error.variable_name == variable_name



# Option not recognized.
def test_option_not_recognized_isolated(arguments):
	OptionFlag(names={"-f"}, variable_name="var")
	arg = "-a"
	arguments.initialize([arg])
	with raises(ArgumentNotRecognizedError) as error:
		arguments.parse()

		assert error.arg == arg



def test_option_not_recognized_concatenated(arguments):
	OptionFlag(names={"-f"}, variable_name="var")
	arg = "-fa"
	arguments.initialize([arg])
	with raises(ArgumentNotRecognizedError) as error:
		arguments.parse()

		assert error.arg == arg



# Expected a short option.
def test_expected_a_short_option(arguments):
	OptionFlag(names={"-f", "-other"}, variable_name="var")
	arg = "-fother"
	arguments.initialize([arg])
	with raises(ArgumentExpectedShortOptionError) as error:
		arguments.parse()

		assert error.arg == arg



# Cannot mix symbols in the same chained short options.
def test_cannot_mix_symbols(arguments):
	OptionFlag(names={"-a", "+b"}, variable_name="var")
	arg = "-ab"
	arguments.initialize([arg])
	with raises(ArgumentNotRecognizedError) as error:
		arguments.parse()

		assert error.arg == arg


# Mix symbols.
def test_mix_symbols(arguments):
	OptionCount(names={"-f", "+g"}, variable_name="F")
	OptionCount(names={"+f", "-g"}, variable_name="G")
	arguments.initialize(["-fgg", "+fffgg"])
	arguments.parse()
	
	assert arguments.goals == []
	assert arguments.environment == { "F": 3, "G": 5 }

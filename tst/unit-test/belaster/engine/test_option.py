
from belaster.engine.option import NameOfOption, Option, OptionStoredInVariable
from toolkit import application_context


names = {"-s", "--long", "++plus"}
variable_name = "variable"


# NameOfOption
def test_name_of_option_short_minus():
	fullname = "-a"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "-"
	assert n.is_short


def test_name_of_option_short_plus():
	fullname = "+a"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "+"
	assert n.is_short


def test_name_of_option_long_1_minus():
	fullname = "-abc"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "-"
	assert not n.is_short


def test_name_of_option_long_2_minus():
	fullname = "--abc"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "-"
	assert not n.is_short


def test_name_of_option_long_3_minus():
	fullname = "---abc"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "-"
	assert not n.is_short


def test_name_of_option_long_1_plus():
	fullname = "+abc"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "+"
	assert not n.is_short


def test_name_of_option_long_2_plus():
	fullname = "++abc"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "+"
	assert not n.is_short


def test_name_of_option_long_3_plus():
	fullname = "+++abc"
	n = NameOfOption(fullname=fullname)

	assert n.fullname == fullname
	assert n.symbol == "+"
	assert not n.is_short


# Option.
def test_option(application_context):
	o = Option(names=names)
	for s in names:
		assert Option.application_context.map_name_to_options[s] == o


def test_option_stored_in_variable(application_context):
	o = OptionStoredInVariable(names=names, variable_name=variable_name)
	assert o.variable_name == variable_name

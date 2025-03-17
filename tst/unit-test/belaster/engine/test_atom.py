
from belaster import Abstract, AtomDuplicateNameError, Directory, File, SymbolicLink
from pytest import raises
from toolkit import application_context



abstractname = "all"
filename = "abc"


# Test the stringification.
def test_string_abstract(application_context):
	assert abstractname == str(Abstract(abstractname))


def test_string_directory(application_context):
	assert filename == str(Directory(filename))


def test_string_file(application_context):
	assert filename == str(File(filename))


def test_string_symboliclink(application_context):
	assert filename == str(SymbolicLink(filename))


# Test the mappings from strings to atoms.
def test_maps_name_to_abstract(application_context):
	a = Abstract(abstractname)
	assert application_context.map_belaster_name_to_targets == {abstractname: a}
	assert application_context.map_cwd_relative_name_to_targets == {abstractname: a}


def test_maps_name_to_directory(application_context):
	a = Directory(filename)
	assert application_context.map_belaster_name_to_targets == {filename: a}
	assert application_context.map_cwd_relative_name_to_targets == {filename: a}


def test_maps_name_to_file(application_context):
	a = File(filename)
	assert application_context.map_belaster_name_to_targets == {filename: a}
	assert application_context.map_cwd_relative_name_to_targets == {filename: a}


def test_maps_name_to_symbolic_link(application_context):
	a = SymbolicLink(filename)
	assert application_context.map_belaster_name_to_targets == {filename: a}
	assert application_context.map_cwd_relative_name_to_targets == {filename: a}


def test_duplicate(application_context):
	a0 = Abstract(abstractname)
	with raises(AtomDuplicateNameError) as error:
		a1 = File(abstractname)
		assert error.atoms == {a0, a1}
		assert error.name == abstractname

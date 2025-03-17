
from belaster.engine.arguments import Arguments
from pytest import fixture
from toolkit import application_context


@fixture
def arguments(application_context):
	return Arguments()

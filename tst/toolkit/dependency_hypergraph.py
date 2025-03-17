
from .application_context import application_context
from belaster.engine.dependency_hypergraph import DependencyHypergraph
from pytest import fixture



@fixture
def dependency_hypergraph(application_context):
	return DependencyHypergraph()


from .application_context import application_context
from belaster import Abstract
from pytest import fixture



@fixture
def t0(application_context):
	return Abstract("a")


@fixture
def t1(application_context):
	return Abstract("b")


@fixture
def t2(application_context):
	return Abstract("c")


@fixture
def t3(application_context):
	return Abstract("d")


@fixture
def t4(application_context):
	return Abstract("e")


@fixture
def t5(application_context):
	return Abstract("f")


@fixture
def t6(application_context):
	return Abstract("g")

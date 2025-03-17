
from belaster.engine.application_context import ApplicationContext
from belaster.engine.application_context_binder import ApplicationContextBinder, ApplicationContextBinderUnboundError
from pytest import raises



def test_assert_is_bound_positive():
	ApplicationContextBinder.application_context = ApplicationContext()
	ApplicationContextBinder.assert_is_bound()


def test_assert_is_bound_negative():
	ApplicationContextBinder.application_context = None
	with raises(ApplicationContextBinderUnboundError):
		ApplicationContextBinder.assert_is_bound()

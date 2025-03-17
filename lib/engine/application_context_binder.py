
from .application_context import ApplicationContext



class ApplicationContextBinderUnboundError(Exception):
	pass


class ApplicationContextBinder:
	"""ApplicationContextBinder binds an ApplicationContext to each
	class who inherits from ApplicationContextBinder.
	Such classes are Recipe, Target, Option***, etc.
	"""

	application_context: ApplicationContext = None

	@classmethod
	def assert_is_bound(cls) -> None:
		if cls.application_context is None:
			raise ApplicationContextBinderUnboundError()

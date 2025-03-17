
from .atom import AtomPath
from .application_context_binder import ApplicationContextBinder



class Rule(ApplicationContextBinder):

	__slots__ = (
		"help", "is_default", "is_visible", "prerequisites", "recipe", "targets",
	)


	def __init__(
			self,
			targets=None, prerequisites=None, recipe=None, is_default=False, is_visible=True, help=None
		):
		self.help = help
		self.is_default = is_default
		self.is_visible = is_visible
		self.prerequisites = prerequisites
		self.recipe = recipe
		self.targets = targets

		self.application_context.add_rule(self)


	def needs_processing(self):
		# The rule is processed if:
		# - one of the targets does not exist,
		# - one of the targets is older than one of the prerequisites,
		# - there is no prerequisites (no list of prerequisites or an empty one).

		if self.prerequisites is None or len(self.prerequisites) == 0:
			return True
		if self.targets is None or len(self.targets) == 0:
			return False
		for t in self.targets:
			if isinstance(t, AtomPath):
				if not t.exists():
					return True
		return any(
			[
				t.last_modification_timestamp() <= p.last_modification_timestamp()
					for p in self.prerequisites if isinstance(p, AtomPath)
					for t in self.targets if isinstance(t, AtomPath)
			]
		)


	def run_recipe(self):
		if self.recipe is not None:
			for callback in self.recipe:
				callback(Rule.application_context.environment)

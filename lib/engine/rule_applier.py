
from .application_context_binder import ApplicationContextBinder
from .atom import Atom
from .rule import Rule



class RuleApplierNotInitializedError(Exception):
	pass



class RuleApplier(ApplicationContextBinder):

	__slots__ = ("goals")


	def __init__(self):
		self.goals = None


	def initialize(self, goals):
		self.goals = goals


	def apply(self):
		# The goals and the prerequisites in a list are executed sequentially from left to right,
		# ie from the head of the list to the tail.

		if self.goals is None:
			raise RuleApplierNotInitializedError()

		atoms_processed = set()

		stack = list(self.goals)
		while len(stack) != 0:
			head = stack.pop(0)
			if isinstance(head, Atom):
				atom = head
				# Either:
				# - atom is the target of the rule r, and atom is unprocessed
				#   => prepend stack with the rule r and its prerequisites.
				#      The rule and its prerequisites will be examined.
				# - else atom is not the target of any rule or atom is aready processed
				#   => no action needed.
				if atom in RuleApplier.application_context.map_targets_rules:
					r = RuleApplier.application_context.map_targets_rules[atom]
					if r is not None and atom not in atoms_processed:
						stack = (r.prerequisites if r.prerequisites is not None else []) + [r] + stack
			elif isinstance(head, Rule):
				rule = head
				# head is a rule, the execution of its recipe needs to be tested.
				recipe_needs_execution = len(atoms_processed.intersection(rule.prerequisites)) != 0 \
					if rule.prerequisites is not None else True
				# A rule without prerequisites is always executed.

				if recipe_needs_execution or rule.needs_processing():
					rule.run_recipe()
				
				if rule.targets is not None:
					atoms_processed.update(rule.targets)

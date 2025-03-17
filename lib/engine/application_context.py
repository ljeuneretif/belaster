
from .dependency_hypergraph import DependencyHypergraph



class AtomDuplicateNameError(Exception):

	__slots__ = ("atoms", "name")

	def __init__(self, atom0, atom1, name):
		super().__init__()
		self.atoms = {atom0, atom1}
		self.name = name



class OptionDuplicateVariableError(Exception):
	
	__slots__ = ("options", "variable_name")

	def __init__(self, option0, option1, variable_name):
		super().__init__()
		self.options = {option0, option1}
		self.variable_name = variable_name



class TargetDuplicateRuleError(Exception):

	__slots__ = ("target", "rules")

	def __init__(self, target, rule0, rule1):
		super().__init__()
		self.target = target
		self.rules = {rule0, rule1}



class ApplicationContext:
	"""Instance created by the application belaster.
	
	Its lifecycle is managed by the application belaster.
	
	Belaster binds the instance of ApplicationContext to all the objects
	instances of the classes Rule, Targets, Option***, etc.
	"""


	__slots__ = (
		"all_atoms",
		"all_rules",
		"all_targets",
		"all_options",

		"belaster_file_directory",

		"dependency_hypergraph",

		"environment",

		"map_belaster_name_to_targets",
		"map_cwd_relative_name_to_targets",

		"map_name_to_options",
		"map_variables_to_options",

		"map_targets_rules",
	)


	def __init__(self):
		self.all_atoms = set()
		self.all_rules = set()
		self.all_targets = set()
		self.all_options = set()

		self.belaster_file_directory = None

		self.dependency_hypergraph = DependencyHypergraph()

		self.environment = None

		self.map_belaster_name_to_targets = {}
		self.map_cwd_relative_name_to_targets = {}

		self.map_name_to_options = {}
		self.map_variables_to_options = {}

		self.map_targets_rules = {}
	

	def add_atom(self, atom, belaster_name, cwd_relative_name):
		if belaster_name in self.map_belaster_name_to_targets:
			raise AtomDuplicateNameError(
				atom,
				self.map_belaster_name_to_targets[belaster_name],
				belaster_name,
				)
		self.map_belaster_name_to_targets[belaster_name] = atom

		if cwd_relative_name in self.map_cwd_relative_name_to_targets:
			raise AtomDuplicateNameError(
				atom,
				self.map_cwd_relative_name_to_targets[cwd_relative_name],
				cwd_relative_name,
				)
		self.map_cwd_relative_name_to_targets[cwd_relative_name] = atom
	

	def add_option(self, option):
		self.all_options.add(option)

		for n in option.names:
			self.map_name_to_options[n.fullname] = option
	

	def add_option_variable_name(self, option):
		var = option.variable_name
		if var in self.map_variables_to_options:
			raise OptionDuplicateVariableError(
				option0=self.map_variables_to_options[var], option1=option, variable_name=var
				)
		self.map_variables_to_options[var] = option



	def add_rule(self, rule):
		self.all_rules.add(rule)

		if rule.targets is not None:
			for t in rule.targets:
				self.all_targets.add(t)
				if t in self.map_targets_rules:
					raise TargetDuplicateRuleError(
						target=t, rule0=self.map_targets_rules[t], rule1=rule
						)
				self.map_targets_rules[t] = rule

		self.dependency_hypergraph.add_rule(rule)



from .application_context_binder import ApplicationContextBinder
from .option import NameOfOption, OptionContainer, OptionCount, OptionEnum, OptionExpectingValue, OptionFlag, OptionValue


class ArgumentExpectedShortOptionError(Exception):

	__slots__ = ("arg")

	def __init__(self, arg):
		super().__init__()
		self.arg = arg



class ArgumentMissingValueError(Exception):
	pass



class ArgumentNotRecognizedError(Exception):

	__slots__ = ("arg")

	def __init__(self, arg):
		super().__init__()
		self.arg = arg



class ArgumentOptionsEndedError(Exception):

	__slots__ = ("arg")

	def __init__(self, arg):
		super().__init__()
		self.arg = arg



class Arguments(ApplicationContextBinder):
	"""Arguments is a stateful class.
	Each instance is dedicated to parsing an input.
	This statefulness helps in factoring the code into intelligible
	private methods.
	"""

	__slots__ = (
		"arg", "args", "args_copy", "awaits_short_option", "current_option",
		"environment", "global_optioncontainer_values", "goals", "is_options_ended",
		"rest_of_arg"
	)


	def __init__(self):
		self.arg = None
		self.args = None
		self.args_copy = None
		self.awaits_short_option = None
		self.current_option = None
		self.environment = None
		self.global_optioncontainer_values = None
		self.goals = None
		self.is_options_ended = None
		self.rest_of_arg = None


	def initialize(self, args):
		self.arg = None
		self.args = args
		self.args_copy = args

		# `self.awaits_short_option` is True when the while loop is parsing
		# a series of short options concatenated.
		# From one iteration to the next one short options are expected
		# until the current bloc of short options concatenated is depleted.
		self.awaits_short_option = False

		# `self.current_option` stores the value-awaiting option that was
		# parsed in the previous iteration of the while loop.
		# When `self.current_option` is not None, the while loop should
		# parse a value.
		# When `self.current_option` is None, the while loop should expect
		# a target or option(s).
		self.current_option = None

		self.environment = {}

		# Each option of type OptionContainer can have its values scattered
		# along the arguments.
		# This dictionary stores their accumulated values during the parsing.
		# After the parsing is finished, the dictionary is integrated into
		# the environment.
		self.global_optioncontainer_values = {}

		self.goals = []
		self.is_options_ended = False
		self.rest_of_arg = None


	def __is_target(self):
		# `self.arg` may be a target.
		if self.arg in Arguments.application_context.map_cwd_relative_name_to_targets:
			if self.awaits_short_option:
				# Bad format to write something like
				# "-starget" for "-s target".
				raise ArgumentExpectedShortOptionError(self.arg)
			self.goals.append(
				Arguments.application_context.map_cwd_relative_name_to_targets[self.arg]
			)
			# The loop can immediately process the next argument.
			return True
		return False


	def __get_option_prefix_of_arg(self):
		# `self.arg` is not a target, it should start with an option name.
		prefixes = [
			option_name
				for option_name in Arguments.application_context.map_name_to_options
				if self.arg.startswith(option_name)
		]

		if len(prefixes) == 0:
			# `self.arg` is not a target and does not start with an option,
			# `self.arg` is badly formatted.
			raise ArgumentNotRecognizedError(arg=self.arg)

		# `self.arg` starts with an option.
		return prefixes[0]


	def __process_value_of_option(self, option):
		# Value processing:
		# - the option is an `OptionCoung` or an `OptionFlag`,
		#   the processing of the value is immediate;
		# - else the value of the option is expected in the
		#   next iteration of the while loop.
		if isinstance(option, OptionCount):
			var = option.variable_name
			if var not in self.environment:
				self.environment[var] = 0
			self.environment[var] += 1
		elif isinstance(option, OptionFlag):
			self.environment[option.variable_name] = True
		elif isinstance(option, OptionExpectingValue):
			# `option` demands a value.
			# That value may be in `self.rest_of_arg` or 
			# in the next element in `self.args`.
			self.current_option = option
			# The next iteration of the while loop
			# will process that value awaited by `current_option`.


	def __process_value_of_current_option(self):
		# `self.current_option` awaits a value of some sort.
		# This is where that value is processed.
		
		# The value always stop at the next space, so `self.arg` contains
		# the whole value expected by `self.current_option`.

		# The way to parse the value is defined by the type of the
		# object stored in `self.current_option`.

		if isinstance(self.current_option, OptionContainer):
			if self.current_option not in self.global_optioncontainer_values:
				self.global_optioncontainer_values[self.current_option] = []

			self.arg = self.arg.removeprefix(self.current_option.separator_first)

			if len(self.arg) != 0:
				# `self.arg` does not represent an empty container.
				list_of_values = self.arg.split(self.current_option.separator_middle)

				value = [self.current_option.type_scalar(v) for v in list_of_values]
				self.global_optioncontainer_values[self.current_option] += value
		
		elif isinstance(self.current_option, OptionEnum):
			value = None

			if self.current_option.symbol_for_key is not None \
					and self.arg[0] == self.current_option.symbol_for_key:
				new_index = self.arg.removeprefix(self.current_option.symbol_for_key)
				value = self.current_option.enum[new_index]

			elif self.current_option.symbol_for_value is not None \
					and self.arg[0] == self.current_option.symbol_for_value:
				new_index_string = self.arg.removeprefix(self.current_option.symbol_for_value)
				new_index = self.current_option.type_enum_alias(new_index_string)
				value = self.current_option.enum(new_index)

			elif self.current_option.is_default_key:
				value = self.current_option.enum[self.arg]

			else:
				value = self.current_option.enum(self.arg)

			self.environment[self.current_option.variable_name] = value

		elif isinstance(self.current_option, OptionValue):
			value = self.current_option.type(self.arg)
			self.environment[self.current_option.variable_name] = value
		# END if

		# The value is fully processed. The next element is either a
		# target or an option.
		self.current_option = None


	def __integrate_option_container_values_into_environment(self):
		# Integrate `self.global_optioncontainer_values` into `self.environment`.
		for option_container in self.global_optioncontainer_values:
			self.environment[option_container.variable_name] = \
				option_container.type_container(
					self.global_optioncontainer_values[option_container]
				)


	def __add_default_values_of_missing_options(self):
		# All the options missing from the command line have their variables
		# set to their default value.

		missing_options = [
			o
				for o in Arguments.application_context.all_options
				if o.has_variable_name() and o.variable_name not in self.environment
		]

		for o in missing_options:
			self.environment[o.variable_name] = o.default_value()


	def parse(self):
		while len(self.args) != 0:
			self.arg = self.args.pop(0)

			if self.current_option is None:
				# BEGIN Neutral Case.

				# Need to detect if `self.arg` is a target or starts with an option.

				# `self.arg` may be a target.
				if self.__is_target():
					# The loop can immediately process the next argument.
					continue

				if self.is_options_ended:
					# Nothing else than targets can appear after the options are ended.
					raise ArgumentOptionsEndedError(arg=self.arg)

				# `self.arg` is not a target, so it should start with an option.
				option_name = self.__get_option_prefix_of_arg()

				option = Arguments.application_context.map_name_to_options[option_name]
				self.is_options_ended =  option.is_end_of_options()

				self.rest_of_arg = self.arg.removeprefix(option_name)
				# `self.arg` == `option_name` + `self.rest_of_arg`

				is_short_option = NameOfOption(fullname=option_name).is_short

				if not is_short_option and self.awaits_short_option:
					# A short option was expected, not a long one.
					# It is a bad format to write something like
					# "-sother" for "-s -other".
					raise ArgumentExpectedShortOptionError(self.arg)

				self.__process_value_of_option(option)

				if len(self.rest_of_arg) == 0:
					# `self.arg` is not the concatenation of short options.
					self.awaits_short_option = False
				else:
					# `option` detected is concatenated to either its value or
					# to other short options.
					# After the following treatment, `self.rest_of_arg` is put back
					# on top of `self.args` for immediate processing in the next
					# iteration of the loop.
					if option.is_expecting_value():
						# `option` awaits a value, and `self.rest_of_arg` is that value.
						# `self.rest_of_arg` is put back on `self.args` to be processed in
						# the next iteration of the while loop.
						self.args.insert(0, self.rest_of_arg)
						self.awaits_short_option = False
					elif is_short_option:
						# `option` is short and does not await a value,
						# so `self.rest_of_arg` starts with a short option.
						# `self.rest_of_arg` is prepended with the symbol
						# `self.arg[0]` then put back on `self.args` to be processed
						# in the next iteration of the loop.
						self.args.insert(0, self.arg[0] + self.rest_of_arg)
						# The next iteration of the while loop expects
						# to detect a short option.
						self.awaits_short_option = True
					else:
						# This is a problem:
						# - `self.rest_of_arg` is not empty;
						# - `option` does not await any value;
						# - the name of the option is a long name,
						#   so it cannot be concatenated to other option names.
						# That means that `self.arg` contains too much, it is an error.
						raise ArgumentNotRecognizedError(arg=self.arg)

				# All subcases of Neutral Case are covered.

				# END Neutral Case.

			else:
				# `self.current_option is not None`

				if self.awaits_short_option:
					raise ArgumentExpectedShortOptionError(arg=self.arg)

				self.__process_value_of_current_option()

				# The while loop resumes.
				continue
			# END if self.current_option is None

		# End of while loop

		if self.current_option is not None:
			raise ArgumentMissingValueError()

		self.__integrate_option_container_values_into_environment()
		self.__add_default_values_of_missing_options()
	
	pass
	# End of Arguments.parse(self)


from .application_context_binder import ApplicationContextBinder



class NameOfOption():

	__slots__ = ("fullname", "is_short", "symbol")

	def __init__(self, fullname: str):
		self.fullname = fullname

		self.symbol = fullname[0]
		name = fullname.removeprefix(self.symbol)
		self.is_short = (len(name) == 1)

	def __str__(self):
		return self.fullname



class Option(ApplicationContextBinder):

	__slots__ = ("names")

	def __init__(self, names=None):
		self.names = {NameOfOption(n) for n in names}
		Option.application_context.add_option(self)
	
	def has_variable_name(self):
		NotImplemented
	
	def is_end_of_options(self):
		NotImplemented
	
	def is_expecting_value(self):
		NotImplemented
	
	def default_value(self):
		NotImplemented



class OptionEnd(Option):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def has_variable_name(self):
		return False

	def is_end_of_options(self):
		return True
	
	def is_expecting_value(self):
		return False
	
	def default_value(self):
		return None



class OptionStoredInVariable(Option):

	__slots__ = ("variable_name")

	def __init__(self, variable_name: str=None, **kwargs):
		super().__init__(**kwargs)
		self.variable_name = variable_name
		OptionStoredInVariable.application_context.add_option_variable_name(self)
	
	def has_variable_name(self):
		return True

	def is_end_of_options(self):
		return False



class OptionExpectingValue(OptionStoredInVariable):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def is_expecting_value(self):
		return True



class OptionNotExpectingValue(OptionStoredInVariable):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def is_expecting_value(self):
		return False



class OptionContainer(OptionExpectingValue):

	__slots__ = ("separator_first", "separator_middle", "type_container", "type_scalar")

	def __init__(self, separator_first=None, separator_middle=None,
							 type_container=None, type_scalar=None, **kwargs):
		super().__init__(**kwargs)

		if separator_first is None or len(separator_first) != 1:
			raise ValueError(f"separator_first {separator_first} should be a string of length 1.")
		self.separator_first = separator_first

		if separator_middle is None or len(separator_middle) != 1:
			raise ValueError(f"separator_middle {separator_middle} should be a string of length 1.")
		self.separator_middle = separator_middle

		self.type_container = type_container
		self.type_scalar = type_scalar
	
	def default_value(self):
		return self.type_container([])



class OptionCount(OptionNotExpectingValue):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def default_value(self):
		return 0



class OptionEnum(OptionExpectingValue):

	__slots__ = (
		"default", "enum", "is_default_key", "type_enum_alias",
		"symbol_for_key", "symbol_for_value"
		)

	def __init__(
			self, default_value=None, enum=None, is_default_key=True,
			symbol_for_key=None, symbol_for_value=None, **kwargs
		):
		super().__init__(**kwargs)
		self.default = default_value
		self.enum = enum
		self.is_default_key = is_default_key

		self.type_enum_alias = type(list(enum._value2member_map_.keys())[0])

		if symbol_for_key is not None and symbol_for_value is not None \
				and symbol_for_key == symbol_for_value:
			raise ValueError(f"symbol_for_key and symbol_for_value are the same {symbol_for_key}")

		if symbol_for_key is not None and len(symbol_for_key) != 1:
			raise ValueError(f"symbol_for_key {symbol_for_key} should be of length 1.")
		self.symbol_for_key = symbol_for_key

		if symbol_for_value is not None and len(symbol_for_value) != 1:
			raise ValueError(f"symbol_for_value {symbol_for_value} should be of length 1.")
		self.symbol_for_value = symbol_for_value
	
	def default_value(self):
		return self.default



class OptionFlag(OptionNotExpectingValue):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def default_value(self):
		return False



class OptionValue(OptionExpectingValue):
	
	__slots__ = ("type")

	def __init__(self, type=None, **kwargs):
		# The argument `type` contains the type directly: str, int, float, etc.
		# The type should be able to be defined by calling its constructor
		# on one value only.
		super().__init__(**kwargs)
		self.type = type
	
	def default_value(self):
		return self.type()

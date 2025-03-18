
OPTIONS_BELASTER_FILE = ["--belaster-file"]
OPTIONS_HELP = ["--help"]
OPTIONS_VERSION = ["--version"]


RETURN_CODE_OK = 0
RETURN_CODE_MISSING_BELASTER_FILE = 1
RETURN_CODE_MISSING_ARGUMENTS = 2



def default_help_message():
	message = """Usage: belaster [options] [targets]

Create a Belaster file in the current working directory. In that Belaster file,
declare options, rules and targets. These options and targets can then be used
as arguments."""

	return message



def error_message_missing_belaster_file(custom_path: bool, path: str):
	if custom_path:
		message = f"""There is no User Belaster script at {path}."""
	else:
		message = """There is no User Belaster script in the current working directory."""

	return message

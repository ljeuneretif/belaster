
from subprocess import run
from toolkit import get_directory



def test_2_rule():
	current_directory = get_directory(__file__)
	
	result = run(
		"bash-completer-helper-for-belaster",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)
	possibilities = result.stdout.strip().split(" ")
	assert possibilities == ["all", "clean"]

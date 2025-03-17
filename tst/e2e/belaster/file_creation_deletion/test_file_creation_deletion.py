
from os.path import exists
from pathlib import Path
from subprocess import run
from toolkit import get_directory



def test_file_creation_deletion():
	current_directory = get_directory(__file__)
	filepath = current_directory + "/blank"
	
	run(
		"belaster blank",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	p = Path(filepath)
	assert p.is_file()


	run(
		"belaster clean",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	assert not exists(filepath)

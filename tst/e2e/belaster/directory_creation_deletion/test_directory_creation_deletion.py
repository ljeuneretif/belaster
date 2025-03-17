
from os.path import exists
from pathlib import Path
from subprocess import run
from toolkit import get_directory



def test_directory_creation_deletion():
	current_directory = get_directory(__file__)
	directory_path = current_directory + "/blank"
	
	run(
		"belaster blank",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	p = Path(directory_path)
	assert p.is_dir()
	
	run(
		"belaster clean",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	assert not exists(directory_path)

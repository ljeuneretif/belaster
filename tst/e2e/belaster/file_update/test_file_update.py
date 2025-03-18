
from os.path import exists, getmtime
from pathlib import Path
from subprocess import run
from toolkit import get_directory



def test_file_update():
	# Initialize test.
	current_directory = get_directory(__file__)

	p_source = current_directory + "/source"
	path_source = Path(p_source)

	p_target = current_directory + "/target"
	path_target = Path(p_target)

	# Empty the source file.
	path_source.touch()
	with open(p_source, "w"):
		pass
	
	# Remove the target file.
	if exists(p_target):
		path_target.unlink()
	assert not exists(p_target)


	# Create the target file.
	run(
		"belaster target",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	assert path_target.is_file()


	# Save the timestamp of the modification of the target.
	timestamp_modification_target_0 = getmtime(p_target)

	# Update the source file.
	with open(p_source, "w") as f:
		f.write("a")
	
	# Verify the timestamp of the modification of the target
	# is greater than the one of the source.
	timestamp_modification_source = getmtime(p_source)

	assert timestamp_modification_target_0 < timestamp_modification_source


	# Update the target file.
	run(
		"belaster target",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	# Verify the content of the target file.
	content = ""
	with open(p_target, "r") as f:
		content += f.read(1)

	assert content == "a"


	# Save the new timestamp of the modification of the target.
	timestamp_modification_target_1 = getmtime(p_target)

	# No update should happen since the source did not change.
	run(
		"belaster target",
		shell=True, executable="/bin/bash", cwd=current_directory,
		capture_output=True, check=True, timeout=10, encoding="utf-8"
	)

	# Verify that the target was not changed.
	assert timestamp_modification_target_1 == getmtime(p_target)


	# Clean test
	path_source.unlink()
	path_target.unlink()

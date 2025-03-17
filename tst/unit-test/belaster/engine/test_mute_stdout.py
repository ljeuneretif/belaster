
from belaster.engine.mute_stdout import MuteStdout
from io import StringIO
import sys



def test_mute_stdout():
	_stdout = sys.stdout
	sys.stdout = stringio = StringIO()
	print("a")
	with MuteStdout():
		print("b")
	print("c")
	assert stringio.getvalue() == "a\nc\n"
	sys.stdout = _stdout

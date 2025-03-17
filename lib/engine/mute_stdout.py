
from contextlib import _RedirectStream
from os import devnull



class MuteStdout(_RedirectStream):
  _stream = "stdout"

  def __init__(self):
    self.nullOutput = open(file=devnull, mode="w")
    super().__init__(self.nullOutput)

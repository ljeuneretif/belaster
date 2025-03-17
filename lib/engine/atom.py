
from abc import ABC, abstractmethod
from .application_context_binder import ApplicationContextBinder
from os import getcwd
from os.path import getmtime, relpath
from pathlib import Path



class Atom(ApplicationContextBinder, ABC):

	def __init__(self):
		Atom.application_context.all_atoms.add(self)


	@abstractmethod
	def __str__(self):
		pass



class Abstract(Atom):

	__slots__ = ("name")


	def __init__(self, name):
		super().__init__()
		self.name = name
		Abstract.application_context.add_atom(self, name, name)
	

	def __str__(self):
		return self.name



class AtomPath(Atom):

	__slots__ = ("path")


	def __init__(self, path):
		super().__init__()
		# The User gives the path relative to the Belaster file.
		# One can see the Belaster file as the root of the tree of resources it manages.
		self.path = Path(AtomPath.application_context.belaster_file_directory + "/" + path)
		# The path is entered in the command-line relatively to the current working directory.
		AtomPath.application_context.add_atom(
			self,
			relpath(path=self.path, start=AtomPath.application_context.belaster_file_directory),
			relpath(path=self.path, start=getcwd()),
		)
	

	def __str__(self):
		# The path of the atom is printed relative to the caller's current working directory.
		# This is coherent with the behaviour of bash, where the paths are described relatively
		# to the current working directory.
		# This is coherence with bash helps with automation.
		return relpath(path=self.path.resolve(), start=getcwd())


	def last_modification_timestamp(self):
		return getmtime(self.path)
	

	def exists(self):
		NotImplemented



class File(AtomPath):
	def exists(self):
		return self.path.is_file()



class Directory(AtomPath):
	def exists(self):
		return self.path.is_dir()



class SymbolicLink(AtomPath):
	def exists(self):
		return self.path.is_symlink()

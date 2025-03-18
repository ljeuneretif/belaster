
from abc import ABC
from .application_context_binder import ApplicationContextBinder
from os import getcwd
from os.path import getmtime, relpath
from pathlib import Path



class Atom(ApplicationContextBinder, ABC):

	__slots__ = ("id")


	def _normalize(self, id):
		NotImplemented


	def __init__(self, id):
		self.id = self._normalize(id)
		Atom.application_context.all_atoms.add(self)
		Abstract.application_context.add_atom(self)


	def __str__(self):
		return self.id



class Abstract(Atom):

	def _normalize(self, id):
		return id



class AtomPath(Atom):

	def _normalize(self, id):
		p = AtomPath.application_context.belaster_file_directory + "/" + id
		path = relpath(path=p, start=getcwd())
		return path


	def last_modification_timestamp(self):
		return getmtime(self.id)


	def exists(self):
		NotImplemented



class File(AtomPath):
	def exists(self):
		return Path(self.id).is_file()



class Directory(AtomPath):
	def exists(self):
		return Path(self.id).is_dir()



class SymbolicLink(AtomPath):
	def exists(self):
		return Path(self.id).is_symlink()

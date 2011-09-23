import hashlib
import os

class suffix_sha1:
	def __init__(self):
		self._hashes = {}

	def add(self, path):
		dir, file = os.path.split(path)
		if not self._hashes.has_key(file):
			self._hashes[file] = hashlib.sha1()
		f = open(path)
		self._hashes[file].update(f.read())
		f.close()

	def getName(self, origName):
		base, ext = os.path.splitext(origName)
		return base + "." + self._hashes[origName].hexdigest() + ext

	def keys(self):
		return self._hashes.keys()
  
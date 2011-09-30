import os
import shutil
import dfs
from suffix_sha1 import suffix_sha1

class Deploy(object):
	def __init__(self, source, target):
		self.target = target
		self.source = source
		self.sfx = suffix_sha1()

	def getExtension(self, filename):
		basename, ext = os.path.splitext(filename)
		return ext

	def IsStatic(self, filename):
		extension = self.getExtension(filename)
		return extension == ".js"

	def IsStaticContained(self, item):
		ext = self.getExtension(item)
		return ext.lower() in [".aspx", ".ascx", ".htm", ".master"]

	def GetSuffix(self, path):
		if self.IsStatic(path):
			self.sfx.add(path)

	def Copy(self, path):
		if self.IsStatic(path) or self.IsStaticContained(path):
			self.copyReplaced(path)
		else:
			self.copy_as_is(path)

	def Deploy(self):
		search = dfs.Search(self.source)
		search.Go(self.GetSuffix)
		search.Go(self.Copy)

	def find_and_replace(self, item, line):
		i = line.lower().find(item)
		while i > 0 and (line[i-1] == "\"" or line[i-1] == "'" or line[i-1] == "/"):
			new_name = self.sfx.getName(item)
			line = line[0:i] + new_name + line[i+len(item):len(line)]
			i = line.lower().find(item)
		return line

	def copyReplaced(self, path):
		rel = os.path.relpath(path, self.source)
		if self.IsStatic(rel):
			basedir, filename = os.path.split(rel)
			new_filename = self.sfx.getName(filename)
			target = os.path.join(self.target, basedir, new_filename)
		else:
			target = os.path.join(self.target, rel)

		ftarget = open(target, "w")
		for line in open(path).readlines():
			for item in self.sfx.keys():
				line = self.find_and_replace(item, line)
			ftarget.writelines(line)

	def copy_as_is(self, path):
		rel = os.path.relpath(path, self.source)
		destination = os.path.join(self.target, rel)
		if os.path.isdir(path):
			os.mkdir(destination)
		else:
			shutil.copyfile(path, destination)

import os

class Search(object):
	def __init__(self, path):
		self.path = path

	def search(self, path, onItemFound):
		for child in os.listdir(path):
			fullPath = os.path.join(path, child)
			onItemFound(fullPath)
			if os.path.isdir(fullPath):
				self.search(fullPath, onItemFound)

	def Go(self, onItemFound):
		self.search(self.path, onItemFound)
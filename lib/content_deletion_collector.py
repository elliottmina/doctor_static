from pathlib import PurePath
from lib import file_util

def get(config):
	return ContentDeletionCollector(
		file_util,
		config.RENDER_DIR)

class ContentDeletionCollector(object):

	def __init__(self, file_util, render_dir):
		self.file_util = file_util
		self.render_dir = render_dir

	def get_list(self):
		files = []
		for basename in self.file_util.listdir(self.render_dir):
			path = self.render_dir + '/' + basename
			if self.file_util.isfile(path):
				files.append(path)
		return files

	def __iter__(self):
		return iter(self.get_list())

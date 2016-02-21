from pathlib import PurePath
from lib import file_util
from lib import source_path

def get(config):
	return ContentBuildCollector(
		source_path.get(config), 
		file_util, 
		config.CONTENT_SOURCE_DIR)

class ContentBuildCollector(object):

	def __init__(self, source_path, file_util, source_dir):
		self.source_path = source_path
		self.file_util = file_util
		self.source_dir = source_dir

	def get_list(self):
		items = []
		for basename in self.file_util.listdir(self.source_dir):
			path = self.source_dir + '/' + basename
			if self.is_markdown(path):
				key = self.source_path.build_key(path)
				items.append(key)
		return items

	def is_markdown(self, path):
		return PurePath(path).suffix == '.md'

	def __iter__(self):
		return iter(self.get_list())


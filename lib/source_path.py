from pathlib import PurePath

def get(config):
	return SourcePath(config.CONTENT_SOURCE_DIR)

class SourcePath(object):
	def __init__(self, source_dir):
		self.source_dir = source_dir

	def build_path(self, key):
		return self.source_dir + '/' + key + '.md'

	def build_key(self, path):
		pure_path = PurePath(path)

		if str(pure_path.parent) != self.source_dir:
			raise InvalidSourcePath()

		return pure_path.stem

class InvalidSourcePath(RuntimeError):
	pass
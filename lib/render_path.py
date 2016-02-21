from pathlib import PurePath
import os

def get(config):
	return RenderPath(config.RENDER_DIR)

class RenderPath(object):
	def __init__(self, output_dir):
		self.output_dir = output_dir

	def build_path(self, key, extension='.html'):
		path = self.output_dir + '/' + key
		return os.path.splitext(path)[0] + extension

	def build_key(self, path):
		pure_path = PurePath(path)

		if str(pure_path.parent) != self.output_dir:
			raise InvalidRenderPath()

		return pure_path.stem

class InvalidRenderPath(RuntimeError):
	pass
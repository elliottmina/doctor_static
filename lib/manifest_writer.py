import json
from lib import render_path

def get(config):
	return ManifestWriter(
		open, 
		render_path.get(config),)

class ManifestWriter(object):
	def __init__(self, file_opener, render_path):
		self.file_opener = file_opener
		self.render_path = render_path

	def write(self, manifest):
		path = self.render_path.build_path('manifest', '.json')
		with self.file_opener(path, 'w') as handle:
			handle.write(json.dumps(manifest))

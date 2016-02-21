from lib import meta_extractor
from lib import content_build_collector
from lib import source_path
from lib import meta_patcher
from lib import console_outputter

def get(config):
	return ManifestPopulator(
		open, 
		meta_extractor.get(), 
		content_build_collector.get(config), 
		source_path.get(config),
		meta_patcher.get(),
		console_outputter,)

class ManifestPopulator(object):
	def __init__(self, file_opener, meta_extractor, content_build_collector, 
		source_path, meta_patcher, console_outputter):
		self.file_opener = file_opener
		self.meta_extractor = meta_extractor
		self.content_build_collector = content_build_collector
		self.source_path = source_path
		self.meta_patcher = meta_patcher
		self.console_outputter = console_outputter

	def generate(self):
		manifest = {}
		for key in self.content_build_collector:
			self.populate_key(key, manifest)
		return manifest

	def populate_key(self, key, manifest):
		self.console_outputter.out('Buidling manifest for {}'.format(key))

		with self.file_opener(self.source_path.build_path(key), 'r') as handle:
			self.meta_patcher.patch(handle)
			manifest[key] = self.meta_extractor.extract(handle)

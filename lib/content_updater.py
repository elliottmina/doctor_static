from lib import content_page_generator
from lib import source_path

def get(config):
	return ContentUpdater(
		open,
		content_page_generator.get(config),
		source_path.get(config),)

class ContentUpdater(object):
	
	def __init__(self, file_opener, page_generator, source_path):
		self.file_opener = file_opener
		self.page_generator = page_generator
		self.source_path = source_path

	def update(self, manifest, tag_map, chron_list):
		for key, meta_data in manifest.items():
			path = self.source_path.build_path(key)
			with self.file_opener(path, 'r') as handle:
				self.page_generator.generate(
					key, 
					meta_data, 
					handle, 
					tag_map,
					manifest,
					chron_list,)

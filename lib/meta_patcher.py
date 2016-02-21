from lib import meta_extractor
from lib import meta_writer
import time

def get():
	return MetaPatcher(
		meta_extractor.get(), 
		meta_writer.get(), 
		time,)

class MetaPatcher(object):

	def __init__(self, meta_extractor, meta_writer, time_util):
		self.meta_extractor = meta_extractor
		self.meta_writer = meta_writer
		self.time_util = time_util

	def patch(self, stream):
		meta_data = self.meta_extractor.extract(stream)

		if meta_data.get('is_content'):
			if 'tags' not in meta_data:
				self.meta_writer.add('tags', '[]', stream)

			if 'create_date' not in meta_data:
				self.meta_writer.add('create_date', self.time_util.time(), stream)

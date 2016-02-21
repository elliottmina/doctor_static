import markdown
import markdown.extensions.codehilite
import markdown.extensions.tables
from lib import meta_line_extractor

def convert(text_stream):
	extensions = [
		'markdown.extensions.codehilite', 
		'markdown.extensions.tables',
	]
	return SourceConverter(
			markdown, 
			meta_line_extractor, 
			extensions).convert(text_stream)

class SourceConverter(object):

	def __init__(self, markdown_lib, meta_line_extractor, extensions):
		self.markdown_lib = markdown_lib
		self.meta_line_extractor = meta_line_extractor
		self.extensions = extensions

	def convert(self, text_stream):
		self.move_cursor_past_meta_data(text_stream)

		return self.markdown_lib.markdown(
			text_stream.read(), 
			extensions=self.extensions)

	def move_cursor_past_meta_data(self, text_stream):
		meta_lines = self.meta_line_extractor.extract(text_stream)
		for i in range(0, len(meta_lines)):
			text_stream.readline()

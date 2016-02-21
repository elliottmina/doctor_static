from lib import file_util
from lib import render_path
from lib import template_renderer
from lib import source_converter
from lib import console_outputter

def get(config):
	return ContentPageGenerator(
		source_converter,
		template_renderer.get(config), 
		file_util,
		render_path.get(config),
		console_outputter,)

class ContentPageGenerator(object):

	def __init__(self, source_converter, template_renderer, 
		file_util, render_path, outputter):
		self.source_converter = source_converter
		self.template_renderer = template_renderer
		self.file_util = file_util
		self.render_path = render_path
		self.outputter = outputter

	def generate(self, key, meta_data, stream, tag_map, manifest, chron_list):
		self.outputter.out('Generating {}'.format(key))
		content_html = self.source_converter.convert(stream)
		contents = self.template_renderer.render(
			meta_data['template'], 
			{
				'content':content_html,
				'meta_data':meta_data,
				'tag_map':tag_map,
				'key':key,
				'manifest':manifest,
				'chron_list':chron_list,
			})
		self.file_util.write(
			self.render_path.build_path(key), 
			contents)

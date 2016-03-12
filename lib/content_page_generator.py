from lib import file_util
from lib import render_path
from lib import template_renderer
from lib import source_converter
from lib import console_outputter
from datetime import date

def get(config):
	return ContentPageGenerator(
		source_converter,
		template_renderer.get(config), 
		file_util,
		render_path.get(config),
		console_outputter,
		date,)

class ContentPageGenerator(object):

	def __init__(self, source_converter, template_renderer, 
		file_util, render_path, outputter, date_lib):
		self.source_converter = source_converter
		self.template_renderer = template_renderer
		self.file_util = file_util
		self.render_path = render_path
		self.outputter = outputter
		self.date_lib = date_lib

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
				'today':self.date_lib.today(),
			})
		self.file_util.write(self.get_path(key, meta_data), contents)

	def get_path(self, key, meta_data):
		if meta_data.get('extension'):
			return self.render_path.build_path(key, meta_data['extension'])
		return self.render_path.build_path(key)


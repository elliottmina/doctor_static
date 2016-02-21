import fixture
import unittest
from test_doubles import ContentSourceConverterSpy
from test_doubles import TemplateRendererSpy
from test_doubles import FileSpy
from test_doubles import FileUtilSpy
from test_doubles import ConsoleOutputterStub
from lib.render_path import RenderPath
from lib.content_page_generator import ContentPageGenerator

class ContentPageGeneratorTest(unittest.TestCase):
	def setUp(self):
		self.source_converter = ContentSourceConverterSpy()
		self.source_converter.convert_return = 'some html'
		self.template_renderer = TemplateRendererSpy()
		self.template_renderer.render_return = 'some content'
		self.source_stream = FileSpy()
		self.file_util = FileUtilSpy([])
		self.tag_map = {'a tag':['a key']}
		self.manifest = {}
		self.chron_list = []
		self.meta_data = {
			'template':'a template',
			'other meta':'some other meta',
		}

		self.test_obj = ContentPageGenerator(
			self.source_converter,
			self.template_renderer,
			self.file_util,
			RenderPath('a render dir'),
			ConsoleOutputterStub(),)

		self.test_obj.generate(
			'a key', 
			self.meta_data, 
			self.source_stream,
			self.tag_map,
			self.manifest,
			self.chron_list,)

	def test_HtmlIsGeneratedFromSourceConverter(self):
		self.assertEqual(
			self.source_stream, 
			self.source_converter.last_convert)

	def test_ContentIsRenderedWithABunchOfStuff(self):
		self.assertEqual(
			(
				'a template', 
				{
					'content':'some html',
					'meta_data':self.meta_data,
					'tag_map':self.tag_map,
					'key':'a key',
					'manifest':self.manifest,
					'chron_list':self.chron_list,
				}
			), 
			self.template_renderer.last_render)

	def test_ContentIsWrittenToFile(self):
		self.assertEqual(
			('a render dir/a key.html', 'some content'), 
			self.file_util.last_write)

if __name__ == '__main__':
	unittest.main()

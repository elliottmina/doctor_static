import fixture
import unittest
from test_doubles import FileOpenerSpy
from test_doubles import FileSpy
from test_doubles import ContentPageGeneratorSpy
from lib.source_path import SourcePath
from lib.content_updater import ContentUpdater

class ContentUpdaterTest(unittest.TestCase):

	def setUp(self):
		self.manifest = {
			'a file': {
				'template':'a template',
				'tags':['tag 1', 'tag 2']
			}
		}
		self.content_page_generator = ContentPageGeneratorSpy()
		self.stream = FileSpy()
		FileOpenerSpy.return_stream = self.stream
		self.tag_map = {}
		self.chron_list = []
		self.test_obj = ContentUpdater(
			FileOpenerSpy,
			self.content_page_generator,
			SourcePath('a source dir'),)
		
	def test_ContentPageIsGenerated(self):
		self.test_obj.update(self.manifest, self.tag_map, self.chron_list)

		result = self.content_page_generator.last_generate
		self.assertEqual(
			(
				'a file',
				{
					'template':'a template',
					'tags':['tag 1', 'tag 2'],
				},
				self.stream,
				self.tag_map,
				self.manifest,
				self.chron_list,
			), 
			result)

if __name__ == '__main__':
	unittest.main()

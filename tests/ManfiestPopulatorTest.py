import fixture
import unittest
from lib.source_path import SourcePath
from test_doubles import FileSpy
from test_doubles import FileOpenerSpy
from test_doubles import MetaExtractorSpy
from test_doubles import ConsoleOutputterStub
from test_doubles import MetaPatcherSpy
from lib.manifest_populator import ManifestPopulator

class ManifestPopulatorTest(unittest.TestCase):
	def setUp(self):
		self.extractor = MetaExtractorSpy({
			'template':'a template',
			'tags':['tag 1', 'tag 2']
		})
		self.build_test_obj()

	def build_test_obj(self):
		self.stream = FileSpy()
		FileOpenerSpy.return_stream = self.stream
		self.meta_patcher = MetaPatcherSpy()
		self.test_obj = ManifestPopulator(
			FileOpenerSpy,
			self.extractor,
			['a file'],
			SourcePath('a source dir'),
			self.meta_patcher,
			ConsoleOutputterStub(),)

	def test_MetaExtractorIsGivenStream(self):
		self.test_obj.generate()
		self.assertEqual(self.stream, self.extractor.last_extract)

	def test_OpenedFileIsCorrect(self):
		self.assertEqual('a source dir/a file.md', FileOpenerSpy.last_open[0])

	def test_ManifestIsUpdated(self):
		manifest = self.test_obj.generate()
		self.assertEqual(
			{
				'a file':{
					'template':'a template',
					'tags':['tag 1', 'tag 2'],
				}
			}, 
			manifest)

	def test_MetaIsPatched(self):
		self.test_obj.generate()
		self.assertEqual(self.stream, self.meta_patcher.last_patch)

if __name__ == '__main__':
	unittest.main()

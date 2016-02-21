import fixture
import unittest
from lib.source_path import SourcePath
from test_doubles import FileUtilSpy
from lib.content_build_collector import ContentBuildCollector

class ContentBuildCollectorTest(unittest.TestCase):

	def setUp(self):
		self.test_obj = ContentBuildCollector(
			SourcePath('a dir'),
			FileUtilSpy(['a file.md', 'b file.md', 'c.html']),
			'a dir')

	def test_ListContainsOnlyKeysFromMarkdownFiles(self):
		self.assertEqual(['a file', 'b file'], list(self.test_obj))

if __name__ == '__main__':
	unittest.main()

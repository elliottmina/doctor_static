import fixture
import unittest
from test_doubles import FileUtilSpy
from lib.render_path import RenderPath
from lib.content_deletion_collector import ContentDeletionCollector

class ContentDeletionCollectorTest(unittest.TestCase):

	def setUp(self):
		self.test_obj = ContentDeletionCollector(
			FileUtilSpy([
				'a.html',
				'b.html',
				'c.txt'
			]),
			'a dir')

	def test_GivenMixedFiles_ListHasOnlyHtmlFiles(self):
		self.assertEqual(
			['a dir/a.html', 'a dir/b.html'], 
			sorted(self.test_obj.get_list()))

	def test_IsIterable(self):
		self.assertEqual(
			['a dir/a.html', 'a dir/b.html'], 
			sorted(list(self.test_obj)))

if __name__ == '__main__':
	unittest.main()

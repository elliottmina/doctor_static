import fixture
import unittest
from lib.source_path import InvalidSourcePath
from lib.source_path import SourcePath

class SourcePathTest(unittest.TestCase):
	def setUp(self):
		self.test_obj = SourcePath('a dir')

	def test_build_path_ReturnsKeyMungedWithDir(self):
		self.assertEqual('a dir/a key.md', self.test_obj.build_path('a key'))

	def test_build_key_ReturnsKeyExtractedFromPath(self):
		self.assertEqual('a key', self.test_obj.build_key('a dir/a key.md'))

	def test_GivenPathOutsideSourceDir_ErrorRaised(self):
		with self.assertRaises(InvalidSourcePath):
			self.test_obj.build_key('b dir/a key.md')

if __name__ == '__main__':
	unittest.main()

import fixture
import unittest
from lib.render_path import InvalidRenderPath
from lib.render_path import RenderPath

class RenderPathTest(unittest.TestCase):
	def setUp(self):
		self.test_obj = RenderPath('a dir')

	def test_build_path_ReturnsKeyMungedWithDir(self):
		self.assertEqual(
			'a dir/a key.html', 
			self.test_obj.build_path('a key.md'))

	def test_build_key_ReturnsStem(self):
		self.assertEqual(
			'a key', 
			self.test_obj.build_key('a dir/a key.html'))

	def test_GivenPathOutsideRenderDir_ErrorRaised(self):
		with self.assertRaises(InvalidRenderPath):
			self.test_obj.build_key('b dir/a key.html')

	def test_GivenExtensionOverride_PathUsesOverride(self):
		self.assertEqual(
			'a dir/a key.xml', 
			self.test_obj.build_path('a key', '.xml'))

if __name__ == '__main__':
	unittest.main()

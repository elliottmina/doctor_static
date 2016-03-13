import fixture
import unittest
from test_doubles import FileSpy
from test_doubles import FileOpenerSpy
from lib.render_path import RenderPath
from lib.manifest_writer import ManifestWriter

class ManifestWriterTest(unittest.TestCase):
	def setUp(self):
		self.write_stream = FileSpy()
		FileOpenerSpy.reset()
		FileOpenerSpy.return_stream = self.write_stream
		self.test_obj = ManifestWriter(
			FileOpenerSpy,
			RenderPath('a dir'),)
		self.manifest = {'a':'manifest'}

	def test_CorrectFileIsWritten(self):
		self.test_obj.write(self.manifest)
		self.assertEqual('a dir/manifest.json', FileOpenerSpy.last_open[0])

	def test_ManifestJsonIsWritten(self):
		self.test_obj.write(self.manifest)
		self.assertEqual(
			'{"a": "manifest"}', 
			self.write_stream.write_buffer)


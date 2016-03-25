import fixture
import unittest
from test_doubles import FileSpy
from test_doubles import FileOpenerSpy
from lib.meta_writer import MetaWriter

class MetaWriterTest(unittest.TestCase):
	def setUp(self):
		self.read_stream = FileSpy()
		self.read_stream.read_return = 'a string'
		self.write_stream = FileSpy()
		FileOpenerSpy.reset()
		FileOpenerSpy.return_stream = self.write_stream
		self.test_obj = MetaWriter(FileOpenerSpy)
		
	def test_KeyAndValueAreWrittenToBeginningOfFile(self):
		self.test_obj.add('a key', 'a value', self.read_stream)

		self.assertEqual(
			'a key: a value\na string', 
			self.write_stream.write_buffer)

	def test_WriteStreamIsSameFileAsReadStream(self):
		self.test_obj.add('a key', 'a value', self.read_stream)
		self.assertEqual('some file', FileOpenerSpy.last_open[0])

	def test_ReadStreamCursorIsResetPriorToReading(self):
		self.test_obj.add('a key', 'a value', self.read_stream)
		self.assertEqual(['seek', 'read',], self.read_stream.operations)
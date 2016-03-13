import fixture
import unittest
from test_doubles import FileUtilSpy
from test_doubles import ConsoleOutputterStub
from lib.cruft_remover import CruftRemover

class CruftRemoverTest(unittest.TestCase):

	def setUp(self):
		self.file_util = FileUtilSpy([])
		self.test_obj = CruftRemover(
			self.file_util,
			['a dir/b file.html'],
			ConsoleOutputterStub(),)

	def test_DeletedPagesAreRemoved(self):
		self.test_obj.update()
		self.assertEqual(['a dir/b file.html'], self.file_util.deletes)


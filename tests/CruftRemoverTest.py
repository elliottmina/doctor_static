import fixture
import unittest
from test_doubles import FileUtilSpy
from test_doubles import ConsoleOutputterStub
from lib.cruft_remover import CruftRemover

class CruftRemoverTest(unittest.TestCase):

	def setUp(self):
		self.enabled = True
		self.file_util = FileUtilSpy([])
		self.deletion_collector = ['a dir/b file.html']

	def build_test_obj(self):
		self.test_obj = CruftRemover(
			self.enabled,
			self.file_util,
			self.deletion_collector,
			ConsoleOutputterStub(),)

	def assert_delete_list(self, delete_list):
		self.build_test_obj()
		self.test_obj.update()
		self.assertEqual(delete_list, self.file_util.deletes)

	def test_GivenEnabled_DeletedPagesAreRemoved(self):
		self.assert_delete_list(['a dir/b file.html'])

	def test_GivenDisabled_NothingRemoved(self):
		self.enabled = False
		self.assert_delete_list([])

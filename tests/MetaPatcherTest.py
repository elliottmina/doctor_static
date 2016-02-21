import fixture
import unittest
from test_doubles import MetaExtractorSpy
from test_doubles import MetaWriterSpy
from test_doubles import FileStub
from test_doubles import TimeUtilStub
from lib.meta_patcher import MetaPatcher

class MetaPatcherTest(unittest.TestCase):
	def setUp(self):
		self.meta_writer = MetaWriterSpy()
		self.stream = FileStub()

	def assert_meta_writes(self, meta_data, expected):
		self.meta_extractor = MetaExtractorSpy(meta_data)
		self.test_obj = MetaPatcher(
			self.meta_extractor, 
			self.meta_writer,
			TimeUtilStub(),)
		self.test_obj.patch(self.stream)
		self.assertEqual(expected, self.meta_writer.adds)

	def test_GivenCompleteMetaData_NothingIsDone(self):
		self.assert_meta_writes(
			{
				'is_content':True,
				'tags':['tag 1', 'tag 2'],
				'create_date':'long long ago',
			},
			[])

	def test_GivenMissingCreateDate_CurrentDateAdded(self):
		self.assert_meta_writes(
			{
				'is_content':True,
				'tags':['tag 1', 'tag 2'],
			},
			[('create_date', 1234567890.000000, self.stream)])

	def test_GivenMissingTags_EmptyTagsAdded(self):
		self.assert_meta_writes(
			{
				'is_content':True,
				'create_date':'long long ago',
			},
			[('tags', '[]', self.stream)])

	def test_GivenIsNotContent_NothingAdded(self):
		self.assert_meta_writes({}, [],)

if __name__ == '__main__':
	unittest.main()

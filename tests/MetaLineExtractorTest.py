import fixture
import unittest
from test_doubles import TextStreamStub
from lib import meta_line_extractor

class MetaLineExtractorTest(unittest.TestCase):
	def setUp(self):
		self.text_stream = TextStreamStub()

	def assertListMatches(self, expected):
		result = meta_line_extractor.extract(self.text_stream)
		self.assertEqual(expected, result)

	def test_GivenNoMeta_EmptyListReturned(self):
		self.assertListMatches([])

	def test_GivenMeta_PopulatedListReturned(self):
		self.text_stream.lines.append('key 1: value 1')
		self.assertListMatches(['key 1: value 1'])

	def test_GivenWhiteSpaceLine_ListExcludesSubsequentItems(self):
		self.text_stream.lines.append('key 1: value 1')
		self.text_stream.lines.append(' ')
		self.text_stream.lines.append('key 2: value 2')
		self.assertListMatches(['key 1: value 1'])

	def test_GivenTooManyLines_ListContainsMaxItems(self):
		self.text_stream.lines.append('key 1: value')
		self.text_stream.lines.append('key 2: value')
		self.text_stream.lines.append('key 3: value')
		self.text_stream.lines.append('key 4: value')
		self.text_stream.lines.append('key 5: value')
		self.text_stream.lines.append('key 6: value')
		self.text_stream.lines.append('key 7: value')
		self.text_stream.lines.append('key 8: value')
		self.text_stream.lines.append('key 9: value')
		self.text_stream.lines.append('key 10: value')
		self.text_stream.lines.append('key 11: value')
		self.assertListMatches([
			'key 1: value',
			'key 2: value',
			'key 3: value',
			'key 4: value',
			'key 5: value',
			'key 6: value',
			'key 7: value',
			'key 8: value',
			'key 9: value',
			'key 10: value',
		])

	def test_GivenPreviousCursorMovement_ListIsStillCorrect(self):
		self.text_stream.lines.append('key 1: value 1')
		self.text_stream.lines.append('key 2: value 2')
		self.text_stream.lines.append('key 3: value 3')
		self.text_stream.lines.append('key 4: value 4')
		self.text_stream.lines.append('key 5: value 5')

		self.text_stream.readline()
		self.text_stream.readline()

		self.assertListMatches([
			'key 1: value 1',
			'key 2: value 2',
			'key 3: value 3',
			'key 4: value 4',
			'key 5: value 5',
		])

	def test_ExtractLeavesCursorAtBeginning(self):
		self.text_stream.lines.append('key 1: value 1')
		self.text_stream.lines.append('key 2: value 2')
		meta_line_extractor.extract(self.text_stream)
		self.assertEqual(0, self.text_stream.curr_index)

if __name__ == '__main__':
	unittest.main()

import fixture
import unittest
from test_doubles import TextStreamStub
from test_doubles import MarkdownSpy
from lib import meta_line_extractor
from lib.source_converter import SourceConverter

class SourceConverterTest(unittest.TestCase):
	def setUp(self):
		self.stream = TextStreamStub()
		self.stream.lines.append('key 1: value 1')
		self.stream.lines.append('key 2: value 2')
		self.stream.lines.append('key 3: value 3')
		self.stream.lines.append('')
		self.stream.lines.append('content')
		self.markdown = MarkdownSpy()
		self.markdown.markdown_return = 'markdown return'
		self.test_obj = SourceConverter(
			self.markdown, 
			meta_line_extractor,
			['extension 1', 'extension 2'],)

	def test_MarkdownIsCalledWithoutMetaData(self):
		self.test_obj.convert(self.stream)
		self.assertEqual('\ncontent\n', self.markdown.last_markdown[0])

	def test_MarkdownReturnsOutput(self):
		result = self.test_obj.convert(self.stream)
		self.assertEqual('markdown return', result)

	def test_InjectedExtensionsAreUsed(self):
		self.test_obj.convert(self.stream)
		self.assertEqual(
			['extension 1', 'extension 2'], 
			self.markdown.last_markdown[1])

if __name__ == '__main__':
	unittest.main()

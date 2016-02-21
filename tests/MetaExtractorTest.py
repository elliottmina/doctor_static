import fixture
import unittest
from test_doubles import MetaLineExtractorStub
from lib.meta_extractor import MetaExtractor

class MetaExtractorTest(unittest.TestCase):
	def setUp(self):
		self.line_extractor = MetaLineExtractorStub()
		self.test_obj = MetaExtractor(self.line_extractor)

	def assertDictMatches(self, expected):
		result = self.test_obj.extract('ignored')
		self.assertEqual(expected, result)

	def test_GivenEmptyContent_EmptyDictReturned(self):
		self.assertDictMatches({})

	def test_GivenStringMeta_PopulatedDictReturned(self):
		self.line_extractor.lines = [
			'foo: some foo',
			'bar: some bar',
		]
		self.assertDictMatches({
			'foo':'some foo',
			'bar': 'some bar',
		})

	def test_GivenSquareBrackets_ValueIsList(self):
		self.line_extractor.lines = ['foo: [spam, ham, eggs]',]
		self.assertDictMatches({
			'foo':['spam', 'ham', 'eggs']
		})

	def self_GivenExtraWhitespaceCsvValue_DictContainsNoWhitespace(self):
		self.line_extractor.lines = ['foo: [  abc  ,  123  ] ',]
		self.assertDictMatches({
			'foo':['abc', '123']
		})

	def self_GivenExtraWhitespaceStringValue_ValueContainsNoWhitespace(self):
		self.line_extractor.lines = ['foo:   abc  ']
		self.assertDictMatches({
			'foo':'abc'
		})

	def test_GivenEmptyString_ValueIsNone(self):
		self.line_extractor.lines = ['foo:']
		self.assertDictMatches({
			'foo':None
		})

	def test_GivenStrBoolean_ValueIsBoolean(self):
		self.line_extractor.lines = [
			'foo: true ',
			'bar: True ',
			'baz: false ',
			'quux: False ',
		]
		self.assertDictMatches({
			'foo':True,
			'bar':True,
			'baz':False,
			'quux':False,
		})

	def test_GivenStrFloat_ValueIsFloat(self):
		self.line_extractor.lines = ['foo:1.2']
		self.assertDictMatches({
			'foo':1.2
		})
		

if __name__ == '__main__':
	unittest.main()

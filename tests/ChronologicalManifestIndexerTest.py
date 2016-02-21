import fixture
import unittest
from lib import chronological_manifest_indexer

class ChronologicalManifestIndexerTest(unittest.TestCase):
	def test_ItemsWithoutCreateDateAreOmitted(self):
		result = chronological_manifest_indexer.generate({
			'a':{'is_content':True, 'create_date':1},
			'b':{'is_content':True, },
		})
		self.assertEqual(['a'], result)

	def test_NonContentItemsAreOmitted(self):
		result = chronological_manifest_indexer.generate({
			'a':{'is_content':True, 'create_date':1},
			'b':{'create_date':1},
		})
		self.assertEqual(['a'], result)

	def test_KeysAreSortedChronologically(self):
		result = chronological_manifest_indexer.generate({
			'a':{'is_content':True, 'create_date':1},
			'b':{'is_content':True, 'create_date':2},
			'c':{'is_content':True, 'create_date':3},
		})
		self.assertEqual(['c', 'b', 'a'], result)

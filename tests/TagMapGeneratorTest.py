import fixture
import unittest
from lib import tag_map_generator

class TagMapTest(unittest.TestCase):

	def test_TagsPopulatedWithAppropriateKeys(self):
		manifest = {
			'key 1':{'tags':['spam', 'ham']},
			'key 2':{'tags':['eggs', 'ham']},
		}

		tag_map = tag_map_generator.generate(manifest)

		self.assertEqual(['key 2'], sorted(tag_map['eggs']))
		self.assertEqual(['key 1', 'key 2'], sorted(tag_map['ham']))
		self.assertEqual(['key 1'], sorted(tag_map['spam']))
		self.assertEqual(['eggs', 'ham', 'spam'], sorted(tag_map))

	def test_GivenNoneValue_KeyIsOmitted(self):
		manifest = {
			'key 1':{'tags':['spam']},
			'key 2':{},
		}

		self.assertEqual(
			{'spam':['key 1']},
			tag_map_generator.generate(manifest)
		)

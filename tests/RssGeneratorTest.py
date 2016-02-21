import fixture
import unittest
from test_doubles import FeedGeneratorFactoryStub
from test_doubles import FeedGeneratorSpy
from test_doubles import TimeUtilStub
from test_doubles import ConsoleOutputterStub
from lib.render_path import RenderPath
from lib.rss_generator import RssGenerator

class RssGeneratorTest(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None
		self.feed_generator_factory = FeedGeneratorFactoryStub()
		self.feed = FeedGeneratorSpy()
		self.feed_generator_factory.build_return = self.feed
		self.SYNDICATION = {
			'id':'http://example.com',
			'link': {'href':'http://example.com',},
			'title':'Dumb and Pointless',
			'subtitle':'A site about arguing on the internet.',
			'author':{
				'name':'Joe Mama',
				'email':'jmama@example.com',
			},
			'category':['A category', 'B category'],
			'contributor':[{
				'name':'Joe Mama', 
				'email':'jmama@example.com',
			},{
				'name':'Joe Daddy', 
				'email':'jdaddy@example.com',
			}],
			'icon':'http://example.com/icon.jpg',
			'logo':'http://example.com/logo.jpg',
			'rights':'Copyright Joe Mama 2016',
			'language':'en',
			'ttl':1000,
			'render_prefix':'http://example.com/stuff',
			'image_prefix':'http://example.com/images',
			'entry_title_template':'Read {}',
			'max_entries':10,
		}
		self.manifest = {
			'a_key':{
				'title':'a title',
				'summary':'a summary',
				'create_date':1455076346.491485,
				'is_content':True,
				'author':'Robert Paulson',
				'tags':['a_tag', 'b_tag'],
				'images':['image_a.jpg', 'image_b.jpg'],
			}
		}

	def build_test_obj(self):
		self.test_obj = RssGenerator(
			self.SYNDICATION,
			self.feed_generator_factory,
			TimeUtilStub(),
			RenderPath('a dir'),
			ConsoleOutputterStub(),)

	def test_FeedConfiguredWithRssConfigValues(self):
		self.build_test_obj()
		self.test_obj.generate(self.manifest)

		self.assertEqual(
			{
				'id':'http://example.com',
				'title':'Dumb and Pointless',
				'author':{'name':'Joe Mama','email':'jmama@example.com',},
				'link': [
					{'href':'http://example.com'}, 
					{'href':'http://example.com/stuff/atom.xml', 'rel':'self',}
				],
				'category':['A category', 'B category'],
				'icon':'http://example.com/icon.jpg',
				'logo':'http://example.com/logo.jpg',
				'rights':'Copyright Joe Mama 2016',
				'subtitle':'A site about arguing on the internet.',
				'language':'en',
				'contributor':[{
					'name':'Joe Mama', 
					'email':'jmama@example.com',
				},{
					'name':'Joe Daddy', 
					'email':'jdaddy@example.com',
				}],
				'ttl':1000,
				'generator':'Doctor Static',
				'pubDate':'Fri, 13 Feb 2009 23:31:30 -0000',
			},
			self.feed.data)

	def test_ContentItemsAreAddedFromManifest(self):
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual(
			{
				'id':'http://example.com/stuff/a_key.html',
				'title':'a title',
				'summary':'a summary',
				'pubdate':'Wed, 10 Feb 2016 03:52:26 -0000', 
				'author':'Robert Paulson',
				'enclosure': [
					'http://example.com/images/image_a.jpg', 
					'http://example.com/images/image_b.jpg', 
				],
				'category':['a_tag', 'b_tag'], 
				'link':{
					'rel':'alternate',
					'href':'http://example.com/stuff/a_key.html',
					'title':'Read a title',
				}
			},
			self.feed.entries[0].data)

	def test_NonContentItemsAreOmitted(self):
		self.manifest['b_key'] = {}
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual(1, len(self.feed.entries))

	def test_ContentIsWrittenToFile(self):
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual('a dir/atom.xml', self.feed.last_atom_file)

	def test_OptionalFeedKeysAbsentFromManifestAreOmitted(self):
		self.SYNDICATION = {
			'id':'http://example.com',
			'title':'Dumb and Pointless',
			'render_prefix':'http://example.com/stuff',
			'entry_title_template':'Read {}',
			'max_entries':10,
		}
		self.build_test_obj()
		self.test_obj.generate(self.manifest)

		self.assertEqual(
			{
				'id':'http://example.com',
				'title':'Dumb and Pointless',
				'link': [{
					'href':'http://example.com/stuff/atom.xml', 
					'rel':'self'
				}],
				'pubDate':'Fri, 13 Feb 2009 23:31:30 -0000',
				'generator':'Doctor Static',
			},
			self.feed.data)

	def test_GivenNoImagePrefix_EnclosureOmitted(self):
		del self.SYNDICATION['image_prefix']
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual(
			{
				'id':'http://example.com/stuff/a_key.html',
				'title':'a title',
				'summary':'a summary',
				'pubdate':'Wed, 10 Feb 2016 03:52:26 -0000', 
				'author':'Robert Paulson',
				'category':['a_tag', 'b_tag'], 
				'link':{
					'rel':'alternate',
					'href':'http://example.com/stuff/a_key.html',
					'title':'Read a title',
				}
			},
			self.feed.entries[0].data)

	def test_GivenManfiestAuthorAbsent_ConfigAuthorSubstituted(self):
		del self.manifest['a_key']['author']
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual(
			{
				'id':'http://example.com/stuff/a_key.html',
				'title':'a title',
				'summary':'a summary',
				'pubdate':'Wed, 10 Feb 2016 03:52:26 -0000', 
				'author':'Joe Mama',
				'enclosure': [
					'http://example.com/images/image_a.jpg', 
					'http://example.com/images/image_b.jpg', 
				],
				'category':['a_tag', 'b_tag'], 
				'link':{
					'rel':'alternate',
					'href':'http://example.com/stuff/a_key.html',
					'title':'Read a title',
				}
			},
			self.feed.entries[0].data)

	def test_OptionalEntryKeysAbsentFromManifestAreOmitted(self):
		self.manifest = {
			'a_key':{
				'title':'a title',
				'create_date':1455076346.491485,
				'is_content':True,
				'author':'Robert Paulson',
			}
		}
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual(
			{
				'id':'http://example.com/stuff/a_key.html',
				'title':'a title',
				'pubdate':'Wed, 10 Feb 2016 03:52:26 -0000', 
				'author':'Robert Paulson',
				'link':{
					'rel':'alternate',
					'href':'http://example.com/stuff/a_key.html',
					'title':'Read a title',
				}
			},
			self.feed.entries[0].data)

	def test_EntriesLimitedByMaxEntries(self):
		self.manifest = {
			'a_key':{
				'title':'a title',
				'create_date':1455076346.491485,
				'is_content':True,
				'author':'Robert Paulson',
			},
			'b_key':{
				'title':'a title',
				'create_date':1455076346.491485,
				'is_content':True,
				'author':'Robert Paulson',
			},
			'c_key':{
				'title':'a title',
				'create_date':1455076346.491485,
				'is_content':True,
				'author':'Robert Paulson',
			},
		}
		self.SYNDICATION['max_entries'] = 2
		self.build_test_obj()
		self.test_obj.generate(self.manifest)
		self.assertEqual(2, len(self.feed.entries))

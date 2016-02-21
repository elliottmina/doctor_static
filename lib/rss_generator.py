from feedgen.feed import FeedGenerator
from email import utils
import time
from lib import render_path
from lib import console_outputter

def get(config):
	return RssGenerator(
		config.SYNDICATION, 
		FeedGeneratorFactory(), 
		time, 
		render_path.get(config),
		console_outputter)

class RssGenerator(object):
	required_feed_keys = ['id', 'title',]
	optional_simple_feed_keys = ['author', 'link', 
		'icon', 'logo', 'rights', 'subtitle', 'language', 'ttl',]

	def __init__(self, SYNDICATION, feed_generator_factory, time_util,
		render_path, outputter,):
		self.SYNDICATION = SYNDICATION
		self.feed_generator_factory = feed_generator_factory
		self.time_util = time_util
		self.render_path = render_path
		self.outputter = outputter

	def generate(self, manifest):
		self.outputter.out('Creating atrom feed')
		feed_generator = self.feed_generator_factory.build()
		self.populate_feed_required_keys(feed_generator)
		self.populate_feed_simple_optional_keys(feed_generator)
		self.populate_feed_link(feed_generator)
		self.populate_feed_pubDate(feed_generator)
		self.populate_feed_contributor(feed_generator)
		self.populate_feed_category(feed_generator)
		self.populate_feed_generator(feed_generator)
		self.populate_entries(feed_generator, manifest)
		self.write_file(feed_generator)

	def populate_feed_required_keys(self, feed_generator):
		for key in self.required_feed_keys:
			self.populate_feed_key_from_config(feed_generator, key)

	def populate_feed_simple_optional_keys(self, feed_generator):
		for key in self.optional_simple_feed_keys:
			if self.SYNDICATION.get(key):
				self.populate_feed_key_from_config(feed_generator, key)

	def populate_feed_key_from_config(self, feed_generator, key):
		func = getattr(feed_generator, key)
		func(self.SYNDICATION[key])

	def populate_feed_link(self, feed_generator):
		url = '{}/{}'.format(self.SYNDICATION['render_prefix'], 'atom.xml')
		feed_generator.link({
			'rel':'self',
			'href':url
		})

	def populate_feed_pubDate(self, feed_generator):
		feed_generator.pubDate(utils.formatdate(self.time_util.time()))

	def populate_feed_contributor(self, feed_generator):
		if self.SYNDICATION.get('contributor') is None:
			return

		for contributor in self.SYNDICATION['contributor']:
			feed_generator.contributor(contributor)

	def populate_feed_category(self, feed_generator):
		if self.SYNDICATION.get('category') is None:
			return

		for category in self.SYNDICATION['category']:
			feed_generator.category(term=category)

	def populate_feed_generator(self, feed_generator):
		feed_generator.generator('Doctor Static')

	def populate_entries(self, feed_generator, manifest):
		num_entries = 0
		for key, data in manifest.items():
			if data.get('is_content'):
				num_entries += 1
				self.generate_entry(feed_generator, key, data)

				if num_entries >= self.SYNDICATION['max_entries']:
					break

	def generate_entry(self, feed_generator, key, data):
		self.outputter.out('Creating atom entry for {}'.format(key))
		entry = feed_generator.add_entry()
		entry.title(data['title'])
		entry.pubdate(utils.formatdate(data['create_date']))
		entry.id(self.get_entry_url(key))

		self.populate_alt_link(entry, data, key)
		self.populate_entry_summary(entry, data)
		self.populate_entry_author(entry, data)
		self.populate_entry_enclosure(entry, data)
		self.populate_entry_category(entry, data)

	def populate_alt_link(self, entry, data, key):
		entry.link({
			'rel':'alternate',
			'href':self.get_entry_url(key),
			'title':self.SYNDICATION['entry_title_template'].format(data['title']),
		})

	def get_entry_url(self, key):
		return '{}/{}.html'.format(self.SYNDICATION['render_prefix'], key)

	def populate_entry_summary(self, entry, data):
		if data.get('summary') is not None:
			entry.summary(data['summary'])

	def populate_entry_category(self, entry, data):
		if data.get('tags') is None:
			return

		for tag in data['tags']:
			entry.category(term=tag)

	def populate_entry_enclosure(self, entry, data):
		if self.SYNDICATION.get('image_prefix') is None:
			return

		if data.get('images') is None:
			return

		for image_suffix in data['images']:
			entry.enclosure('{}/{}'.format(
				self.SYNDICATION['image_prefix'], 
				image_suffix))

	def populate_entry_author(self, entry, data):
		if data.get('author') is not None:
			entry.author(name=data['author'])
		elif self.SYNDICATION.get('author') is not None:
			entry.author(name=self.SYNDICATION['author']['name'])

	def write_file(self, feed_generator):
		self.outputter.out('Writing atom file')
		file_path = self.render_path.build_path('atom', '.xml')
		feed_generator.atom_file(file_path)

class FeedGeneratorFactory(object):
	def build(self):
		return FeedGenerator()

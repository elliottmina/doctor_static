import fixture
import unittest
from test_doubles import ManifestPopulatorSpy
from test_doubles import ContentUpdaterSpy
from test_doubles import TemplateErroringContentUpdater
from test_doubles import CruftRemoverSpy
from test_doubles import ManifestDependentGeneratorSpy
from test_doubles import RssGeneratorSpy
from test_doubles import ConsoleOutputterSpy
from jinja2.exceptions import TemplateNotFound
from lib.commands.build import Builder

class BuilderTest(unittest.TestCase):

	def setUp(self):
		self.manifest_populator = ManifestPopulatorSpy()
		self.manifest_populator.populate_return = {}
		self.content_updater = ContentUpdaterSpy()
		self.cruft_remover = CruftRemoverSpy()
		self.tag_map_generator = ManifestDependentGeneratorSpy()
		self.tag_map_generator.generate_return = {}
		self.chronological_manifest_indexer = ManifestDependentGeneratorSpy()
		self.chronological_manifest_indexer.generate_return = []
		self.rss_generator = RssGeneratorSpy()
		self.outputter = ConsoleOutputterSpy()
		self.build_test_obj()

	def build_test_obj(self):
		self.test_obj = Builder(
			self.manifest_populator,
			self.content_updater,
			self.cruft_remover,
			self.tag_map_generator,
			self.chronological_manifest_indexer,
			self.rss_generator,
			self.outputter,)

	def test_ManifestPopulated(self):
		self.test_obj.execute()
		self.assertTrue(self.manifest_populator.populate_called)

	def test_ContentUpdaterCalledWithStuff(self):
		self.test_obj.execute()
		self.assertEqual(
			(
				self.manifest_populator.populate_return, 
				self.tag_map_generator.generate_return, 
				self.chronological_manifest_indexer.generate_return,
			), 
			self.content_updater.last_update)

	def test_CruftRemoverCalled(self):
		self.test_obj.execute()
		self.assertTrue(self.cruft_remover.update_called)

	def test_TagMapIsGenerated(self):
		self.test_obj.execute()
		self.assertTrue(self.tag_map_generator.generate_called)

	def test_ChronologicalIndexIsGenerated(self):
		self.test_obj.execute()
		self.assertTrue(self.chronological_manifest_indexer.generate_called)

	def test_RssGeneratorIsCalled(self):
		self.test_obj.execute()
		self.assertEqual(
			self.manifest_populator.populate_return, 
			self.rss_generator.last_generate)

	def test_GivenJinjaTemplateError_FriendlyMessageDisplayed(self):
		self.content_updater = TemplateErroringContentUpdater()
		self.build_test_obj()
		self.test_obj.execute()
		self.assertTrue(
			'\nError: Could not find template "a template"\n', 
			self.outputter.last_out)

if __name__ == '__main__':
	unittest.main()

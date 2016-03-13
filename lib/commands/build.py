from lib import content_updater
from lib import cruft_remover
from lib import manifest_populator
from lib import tag_map_generator
from lib import chronological_manifest_indexer
from lib import rss_generator
from lib import post_build_scripts_runner
from lib import console_outputter
from lib import manifest_writer
from jinja2.exceptions import TemplateNotFound

def execute(config):
	Builder(
		manifest_populator.get(config),
		content_updater.get(config),
		cruft_remover.get(config),
		tag_map_generator,
		chronological_manifest_indexer,
		rss_generator.get(config),
		post_build_scripts_runner.get(config),
		console_outputter,
		manifest_writer.get(config),).execute()

class Builder(object):
	def __init__(self, manifest_populator, content_updater, 
		cruft_remover, tag_map_generator, chronological_manifest_indexer,
		rss_generator, script_runner, outputter, manifest_writer):
		self.manifest_populator = manifest_populator
		self.content_updater = content_updater
		self.cruft_remover = cruft_remover
		self.tag_map_generator = tag_map_generator
		self.chronological_manifest_indexer = chronological_manifest_indexer
		self.rss_generator = rss_generator
		self.script_runner = script_runner
		self.outputter = outputter
		self.manifest_writer = manifest_writer

	def execute(self):
		try:
			self.cruft_remover.update()
			manifest = self.manifest_populator.generate()
			tag_map = self.tag_map_generator.generate(manifest)
			chron_list = self.chronological_manifest_indexer.generate(manifest)
			self.content_updater.update(manifest, tag_map, chron_list)
			self.rss_generator.generate(manifest)
			self.manifest_writer.write(manifest)
			self.script_runner.execute()
			self.outputter.out('Done')
		except TemplateNotFound as e:
			message = '\nError: Could not find template "{}"\n'.format(e)
			self.outputter.out(message)

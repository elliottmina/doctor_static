from lib import file_util
from lib import console_outputter
from lib import content_deletion_collector

def get(config):
	enabled = False
	if hasattr(config, 'PURGE_RENDER_DIR'):
		enabled = config.PURGE_RENDER_DIR
	return CruftRemover(
		enabled,
		file_util,
		content_deletion_collector.get(config),
		console_outputter,)

class CruftRemover(object):
	
	def __init__(self, enabled, file_util, delete_collector, outputter):
		self.enabled = enabled
		self.file_util = file_util
		self.delete_collector = delete_collector
		self.outputter = outputter

	def update(self):
		if not self.enabled: return

		for path in self.delete_collector:
			self.outputter.out('Removing {}'.format(path))
			self.file_util.delete(path)

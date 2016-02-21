from lib import file_util
from lib import console_outputter
from lib import content_deletion_collector

def get(config):
	return CruftRemover(
		file_util,
		content_deletion_collector.get(config),
		console_outputter,)

class CruftRemover(object):
	
	def __init__(self, file_util, delete_collector, 
		outputter):
		self.file_util = file_util
		self.delete_collector = delete_collector
		self.outputter = outputter

	def update(self):
		for path in self.delete_collector:
			self.outputter.out('Removing {}'.format(path))
			self.file_util.delete(path)

import os
from lib.script_runner import ScriptRunner
from lib import console_outputter

def get(config):
	scripts = []
	if hasattr(config, 'POST_BUILD_SCRIPTS'):
		scripts = config.POST_BUILD_SCRIPTS

	return PostBuildScriptsRunner(
		ScriptRunner(os), 
		scripts, 
		console_outputter)

class PostBuildScriptsRunner(object):
	def __init__(self, runner, scripts, console_outputter):
		self.runner = runner
		self.scripts = scripts
		self.console_outputter = console_outputter

	def execute(self, manifest):
		self.console_outputter.out('Running post build scripts')
		for script in self.scripts:
			self.runner.run(script, manifest)


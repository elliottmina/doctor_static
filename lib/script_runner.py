import json

class ScriptRunner(object):
	def __init__(self, os, outputter):
		self.os = os
		self.outputter = outputter

	def run(self, command, *args):
		self.outputter.out(command)
		arg_strings = ["'" + json.dumps(arg) + "'" for arg in args]
		params = ' '.join(arg_strings)
		command = '{} {}'.format(command, params).strip()
		self.os.system(command)
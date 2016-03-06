import json

class ScriptRunner(object):
	def __init__(self, os):
		self.os = os

	def run(self, command, *args):
		arg_strings = ["'" + json.dumps(arg) + "'" for arg in args]
		params = ' '.join(arg_strings)
		command = '{} {}'.format(command, params).strip()
		self.os.system(command)
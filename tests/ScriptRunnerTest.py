import fixture
import unittest
from test_doubles import OsSpy
from lib.script_runner import ScriptRunner

class ScriptsRunnerTest(unittest.TestCase):
	def setUp(self):
		self.os = OsSpy()
		self.test_obj = ScriptRunner(self.os)

	def test_GivenNoArgs_OnlyCommandIsRun(self):
		self.test_obj.run('echo "test"')
		self.assertEqual('echo "test"', self.os.last_system)

	def test_GivenExtra_ArgsPassedAsJson(self):
		result = self.test_obj.run('echo', {'this':'that'}, 123)
		self.assertEqual(
			'echo \'{"this": "that"}\' \'123\'', 
			self.os.last_system)


import fixture
import unittest
from test_doubles import ScriptRunnerSpy
from test_doubles import ConsoleOutputterSpy
from lib.post_build_scripts_runner import PostBuildScriptsRunner

class PostBuildScriptsRunnerTest(unittest.TestCase):
	def setUp(self):
		self.runner = ScriptRunnerSpy()
		self.scripts = []
		self.manifest = 'manifest'

	def assert_runs_equal(self, expected):
		test_obj = PostBuildScriptsRunner(
			self.runner, 
			self.scripts, 
			ConsoleOutputterSpy())
		test_obj.execute(self.manifest)
		self.assertEqual(expected, self.runner.runs)
		
	def test_GivenConfigWithEmptyScripts_NoScriptsAreRun(self):
		self.assert_runs_equal([])

	def test_GivenConfigWithScripts_ScriptsAreRun(self):
		self.scripts = ['spam', 'ham']
		self.assert_runs_equal([
			('spam', 'manifest'),
			('ham', 'manifest'),
		])

import fixture
import unittest
from test_doubles import JinjaTemplateSpy
from test_doubles import JinjaEnvStub
from lib.template_renderer import TemplateRenderer

class TemplateRendererTest(unittest.TestCase):
	
	def setUp(self):
		self.template = JinjaTemplateSpy()
		self.env = JinjaEnvStub({'a template':self.template})
		self.test_obj = TemplateRenderer(self.env)
	
	def test_TemplateIsRendered(self):
		self.test_obj.render('a template', {'key':'value'})
		self.assertEqual({'key':'value'}, self.template.last_render)

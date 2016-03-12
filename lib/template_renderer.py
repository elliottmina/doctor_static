from jinja2 import Environment, FileSystemLoader
import json
import datetime

def get(config):
	template_loader = FileSystemLoader(searchpath=config.TEMPLATE_DIR)
	env = Environment(
		loader=template_loader, 
		extensions=['jinja2.ext.loopcontrols'])
	env.filters['tojson'] = tojson
	env.filters['isdisjoint'] = isdisjoint
	env.filters['timestamp_to_date'] = timestamp_to_date
	env.filters['strftime'] = strftime
	return TemplateRenderer(env)

def tojson(data):
	return json.dumps(data)

def isdisjoint(a, b):
	if a is None or b is None:
		return True
	return set(a).isdisjoint(set(b))

def timestamp_to_date(timestamp):
	return datetime.datetime.fromtimestamp(int(timestamp))

def strftime(date, format):
	return date.strftime(format)

class TemplateRenderer(object):
	def __init__(self, env):
		self.env = env

	def render(self, template_name, data):
		template = self.env.get_template(template_name)
		return template.render(data)

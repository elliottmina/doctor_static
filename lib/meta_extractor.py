import re
from lib import meta_line_extractor

def get():
	return MetaExtractor(meta_line_extractor)

class MetaExtractor(object):
	def __init__(self, line_extractor):
		self.line_extractor = line_extractor
	
	def extract(self, text_stream):
		data = {}
		for line in self.line_extractor.extract(text_stream):
			self.process_line(line, data)
		return data

	def process_line(self, line, data):
		parts = line.split(':', 1)
		data[parts[0].strip()] = self.get_value(parts[1])

	def get_value(self, raw_value):
		raw_value = raw_value.strip()

		matches = re.search('^\s*\[(.*)\]\s*$', raw_value)
		if matches:
			return self.get_list_value(matches)

		if raw_value == '':
			return None

		if raw_value.lower() == 'true':
			return True

		if raw_value.lower() == 'false':
			return False

		matches = re.search('^\s*[0-9]+\.[0-9]+\s*$', raw_value)
		if matches:
			return float(raw_value)

		return raw_value

	def get_list_value(self, matches):
		parts = matches.group(1).split(',')
		return [part.strip() for part in parts if len(part.strip())]

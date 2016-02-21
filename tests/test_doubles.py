from jinja2.exceptions import TemplateNotFound

class FileUtilSpy(object):
	def __init__(self, existing_paths):
		self.existing_paths = existing_paths
		self.last_write = None
		self.deletes = []

	def listdir(self, path):
		return self.existing_paths
	
	def write(self, path, contents):
		self.last_write = (path, contents)

	def delete(self, path):
		self.deletes.append(path)

class FileNotFoundFileOpener(object):
	def __init__(self, path, mode):
		pass
	def __enter__(self):
		raise FileNotFoundError()
	def __exit__(self, exc_type, exc_value, traceback):
		pass

class NonJSONFileOpener(object):
	def __init__(self, path, mode):
		pass
	def __enter__(self):
		return NoneJSONFileHandle()
	def __exit__(self, exc_type, exc_value, traceback):
		pass

class NoneJSONFileHandle(object):
	def read(self):
		return ''

class FileOpenerSpy(object):
	return_stream = None
	last_open = None

	# This is a totally legitimate hack.
	@classmethod
	def __init__(cls, path, mode):
		cls.last_open = (path, mode)

	@classmethod
	def reset(cls):
		cls.return_stream = None
		cls.last_open = None

	def __enter__(self):
		return self.return_stream

	def __exit__(self, exc_type, exc_value, traceback):
		pass

class FileSpy(object):
	def __init__(self):
		self.write_buffer = ""
		self.read_return = ""

	def read(self):
		return self.read_return

	def write(self, str):
		self.write_buffer += str

class FileOpenerStub(object):
	def __init__(self, path, mode):
		pass
	def __enter__(self):
		return FileStub()
	def __exit__(self, exc_type, exc_value, traceback):
		pass

class FileStub(object):
	def __init__(self):
		self.name = 'some file'

	def read(self):
		return 'a string'

class MetaExtractorSpy(object):
	def __init__(self, data):
		self.data = data
		self.last_extract = None

	def extract(self, stream):
		self.last_extract = stream
		return self.data

class MetaWriterSpy(object):
	def __init__(self):
		self.adds = []

	def add(self, key, value, stream):
		self.adds.append((key, value, stream))

class TimeUtilStub(object):
	def time(self):
		return 1234567890.000000

class ContentPageGeneratorSpy(object):
	def __init__(self):
		self.last_generate = None

	def generate(self, key, meta_data, stream, tag_map, manifest, chron_list):
		self.last_generate = (key, meta_data, stream, tag_map, 
			manifest, chron_list)

class ContentUpdaterSpy(object):
	def __init__(self):
		self.last_update = None

	def update(self, manifest, tag_map, chron_list):
		self.last_update = (manifest, tag_map, chron_list)

class TemplateErroringContentUpdater(object):
	def update(self, manifest, tag_map, chron_list):
		raise TemplateNotFound('a template')

class CruftRemoverSpy(object):
	def __init__(self):
		self.update_called = False

	def update(self):
		self.update_called = True

class ContentSourceConverterSpy(object):
	def __init__(self):
		self.last_convert = None
		self.convert_return = None

	def convert(self, stream):
		self.last_convert = stream
		return self.convert_return

class TemplateRendererSpy(object):
	def __init__(self):
		self.last_render = None
		self.render_return = None

	def render(self, template, data):
		self.last_render = (template, data)
		return self.render_return

class JinjaEnvStub(object):
	def __init__(self, template_map):
		self.template_map = template_map

	def get_template(self, key):
		return  self.template_map[key]

class JinjaTemplateSpy(object):
	def __init__(self):
		self.last_render = None

	def render(self, data):
		self.last_render = data

class TextStreamStub:
	def __init__(self):
		self.lines = []
		self.curr_index = 0;

	def readline(self):
		if self.curr_index >= len(self.lines):
			return ''

		line = self.lines[self.curr_index]
		self.curr_index += 1
		return line

	def read(self):
		output = ''
		for i in range(self.curr_index, len(self.lines)):
			output += self.lines[i] + '\n'
		return output

	def seek(self, offset):
		self.curr_index = 0

class MarkdownSpy(object):
	def __init__(self):
		self.last_markdown = None
		self.markdown_return = None

	def markdown(self, text, extensions=None):
		self.last_markdown = (text, extensions)
		return self.markdown_return

class MetaLineExtractorStub(object):
	def __init__(self):
		self.lines = []

	def extract(self, text_stream):
		return self.lines

class ConsoleOutputterStub(object):
	def out(self, text):
		pass

class ConsoleOutputterSpy(object):
	def __init__(self):
		self.last_out = None

	def out(self, text):
		self.last_out = text

class ManifestPopulatorSpy(object):
	def __init__(self):
		self.populate_return = None
		self.populate_called = False

	def generate(self):
		self.populate_called = True
		return self.populate_return

class MetaPatcherSpy(object):
	def __init__(self):
		self.last_patch = None

	def patch(self, stream):
		self.last_patch = stream

class ManifestDependentGeneratorSpy(object):
	def __init__(self):
		self.generate_return = None
		self.generate_called = False

	def generate(self, manifest):
		self.generate_called = True
		return self.generate_return

class FeedGeneratorFactoryStub(object):
	def __init__(self):
		self.build_return = None

	def build(self):
		return self.build_return

class FeedGeneratorSpy(object):
	def __init__(self):
		self.data = {}
		self.entries = []
		self.last_atom_file = None

	def id(self, val):
		self.data['id'] = val
	def title(self, val):
		self.data['title'] = val
	def author(self, val):
		self.data['author'] = val
	def link(self, val):
		self.data['link'] = val
	def category(self, **kwargs):
		if kwargs.get('term'):
			if 'category' not in self.data:
				self.data['category'] = []
			self.data['category'].append(kwargs['term'])
	def contributor(self, val):
		if 'contributor' not in self.data:
			self.data['contributor'] = []
		self.data['contributor'].append(val)
	def icon(self, val):
		self.data['icon'] = val
	def logo(self, val):
		self.data['logo'] = val
	def rights(self, val):
		self.data['rights'] = val
	def subtitle(self, val):
		self.data['subtitle'] = val
	def link(self, val):
		if 'link' not in self.data:
			self.data['link'] = []
		self.data['link'].append(val)
	def language(self, val):
		self.data['language'] = val
	def pubDate(self, val):
		self.data['pubDate'] = val
	def ttl(self, val):
		self.data['ttl'] = val
	def generator(self, val):
		self.data['generator'] = val

	def add_entry(self):
		entry = FeedEntrySpy()
		self.entries.append(entry)
		return entry

	def atom_file(self, path):
		self.last_atom_file = path

class FeedEntrySpy(object):
	def __init__(self):
		self.data = {}

	def id(self, val):
		self.data['id'] = val
	def title(self, val):
		self.data['title'] = val
	def summary(self, val):
		self.data['summary'] = val
	def pubdate(self, val):
		self.data['pubdate'] = val
	def link(self, val):
		self.data['link'] = val
	def author(self, **kwargs):
		if kwargs.get('name'):
			self.data['author'] = kwargs['name']
	def enclosure(self, val):
		if 'enclosure' not in self.data:
			self.data['enclosure'] = []
		self.data['enclosure'].append(val)
	def category(self, **kwargs):
		if kwargs.get('term'):
			if 'category' not in self.data:
				self.data['category'] = []
			self.data['category'].append(kwargs['term'])
	def link(self, val):
		self.data['link'] = val

class ConfigStub(object):
	pass

class RssGeneratorSpy(object):
	def __init__(self):
		self.last_generate = None

	def generate(self, manifest):
		self.last_generate = manifest


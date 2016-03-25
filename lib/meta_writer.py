def get():
	return MetaWriter(open)
	
class MetaWriter(object):
	def __init__(self, file_opener):
		self.file_opener = file_opener

	def add(self, key, value, read_stream):
		read_stream.seek(0)
		contents = read_stream.read()
		with self.file_opener(read_stream.name, 'w') as write_stream:
			write_stream.write('{}: {}\n'.format(key, value))
			write_stream.write(contents)

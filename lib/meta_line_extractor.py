_MAX_LINES_TO_PROCESS = 10

def extract(text_stream):
	text_stream.seek(0)
	lines = []
	for i in range(0, _MAX_LINES_TO_PROCESS):
		line = text_stream.readline().strip()
		if line == '':
			break
		lines.append(line)
	text_stream.seek(0)
	return lines

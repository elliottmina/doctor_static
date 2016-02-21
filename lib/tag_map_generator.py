def generate(manifest):
	tag_map = {}
	for key, meta_data in manifest.items():
		process(key, meta_data, tag_map)
	return tag_map

def process(key, meta_data, tag_map):
	if meta_data.get('tags'):
		for tag in meta_data['tags']:
			add(key, tag, tag_map)

def add(key, tag, tag_map):
	if tag not in tag_map:
		tag_map[tag] = []
	tag_map[tag].append(key)

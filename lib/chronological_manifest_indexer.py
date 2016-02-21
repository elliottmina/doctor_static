def generate(manifest):
	sorted_keys = []
	for key, data in manifest.items():
		if data.get('is_content') and data.get('create_date'):
			sorted_keys.append(key)

	return sorted(
		sorted_keys, 
		key=lambda mkey: manifest[mkey]['create_date'],
		reverse=True)

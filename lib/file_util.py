import os
import hashlib

def delete(path):
	os.unlink(path)

def write(path, contents):
	with open(path, 'w') as handle:
		handle.write(contents)

def exists(path):
	return os.path.exists(path)

def listdir(dir):
	return os.listdir(dir)

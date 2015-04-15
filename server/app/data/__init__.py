from flask_sqlalchemy import SQLAlchemy

mydb = SQLAlchemy()

import inspect
from functools import wraps, partial

def mapper(f=None):
	if f is None:
		return partial(mapper)
	@wraps(f)
	def _wrap(*args):
		return model_as_dict(*args)
	return _wrap

def mapperConfig(f=None, only=[], exclude=[], include_relationships=True):
	if f is None:
		return partial(mapperConfig, only=only, exclude=exclude, include_relationships=include_relationships)
	@wraps(f)
	def _wrap(*args, **kwargs):
		return config_mapper(*args, only=only, exclude=exclude, include_relationships=include_relationships)
	return _wrap

def model_as_dict(obj, only=[], exclude=[], include_relationships=False, follow_default_rules=True):
	#read default config
	map_conf = obj.getMapperConfig()
	if not map_conf:
		obj.defineMapper()
		map_conf = obj.getMapperConfig()
	hiddens = ["query_class", "query", "metadata"]
	pr = {}
	for name in dir(obj):
		value = getattr(obj, name)
		if isinstance(value, mydb.Model) or isinstance(value, list):
			if (map_conf['include_relationships'] and follow_default_rules or include_relationships) and ((map_conf['only'] and follow_default_rules) and (name in map_conf['only'] and not only) or not map_conf['only'] and not only or name in only) and not name in map_conf['exclude'] and not name in exclude:
				#re.match('('+name+').(.*)', 'hola.saludo.x.id').groups()
				if isinstance(value, mydb.Model):
					pr[name] = value.toDict()
		elif ((map_conf['only'] and follow_default_rules) and (name in map_conf['only'] and not only) or not map_conf['only'] and not only or name in only) and not name.startswith('_') and not name.startswith('__') and not inspect.ismethod(value) and not name in hiddens and not name in map_conf['exclude'] and not name in exclude:
			pr[name] = value
	return pr

def config_mapper(obj, only=[], exclude=[], include_relationships=True):
		obj.setMapperConfig({
		'only': only,
		'exclude': exclude,
		'include_relationships': include_relationships	
		})

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

class DictMapper():
	_mapper = {}
	
	def __init__(self):
		self._mapper = self.defineMapper()

	def setMapperConfig(self, config):
		self._mapper = config

	def getMapperConfig(self):
		return self._mapper

	@mapperConfig
	def defineMapper(self):
		pass

	@mapper
	def toDict(self):
		pass

	def toCustomDict(self, only=[], exclude=[], include_relationships=True, merge=None):
		if merge:
			return merge_two_dicts(model_as_dict(self, only=only, exclude=exclude, include_relationships=include_relationships), merge)
		else:
			return model_as_dict(self, only=only, exclude=exclude, include_relationships=include_relationships)

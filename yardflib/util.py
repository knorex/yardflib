class Cache(object):
	
	def __init__(self, capacity = -1):
		self.capacity = capacity
		self.cache = {}
		self.index = {}
		
	@property
	def size(self):
		return len(self.cache)
		
	@property
	def has_capacity(self):
		return (self.capacity == -1) or (self.capacity > len(self.cache))
		
	def set(self, key, value):
		if self.has_capacity:
			self.cache[key] = value
			self.index[id(value)] = key
	
	def get(self, key):
		return self.cache.get(key)
			
	def clear():
		self.cache.clear()
		self.index.clear()
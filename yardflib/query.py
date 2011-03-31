import model

class Variable(model.Term):
	
	def __init__(self, name = None, value = None):
		if name:
			self.name = name
		else:
			self.name = "g%d" % id(self)
		self.value = value

	@property
	def is_variable(self):
		return True

	@property
	def is_named(self):
		return True

	@property
	def is_unbound(self):
		return self.value == None

	@property
	def is_bound(self):
		return not self.is_unbound

	def bind(self, value):
		old_value = self.value
		self.value = value
		return old_value

	def unbind(self, value):
		old_value = self.value
		self.value = None
		return old_value

	@property	
	def variables(self):
		return { self.name: self}

	@property
	def bindings(self):
		if self.is_unbound:
			return {}
		else:
			return { self.name : self.value }

	@property
	def hash(self):
		return self.name.__hash__()
		
	def __eq__(self, other):
		return (type(other) == Variable) and (self.name == other.name)
		
	def __str__(self):
		if self.is_unbound:
			return "?%s" % self.name
		else:
			return "?%s=$s" % (self.name, self.value)	
			
	def __repr__(self):
		if self.is_unbound:
			return "Variable(?%s)" % self.name
		else:
			return "Variable(?%s=$s)" % (self.name, self.value)	

class Solution(object):
	
	def __init__(self, bindings = {}):
		self.bindings = bindings
		
	def each_key(self):
		for binding_key in self.bindings.keys():
			yield binding_key
			
	def each_value(self):
		for binding_value in self.bindings.values():
			yield binding_value
			
	def has_variables(self, variables):
		for v in variables:
			if self.bound(variable):
				return True
		return False		
	
	def each_variable(self):
		for item in self.bindings.items():
			yield Variable(name, value)
		
	def is_bound(self, name):
		return not self.is_unbound(name)
		
	def is_unbound(self, name):
		return self.bindings[name] == None
	
	def get(self, name):
		return self.bindings.get(name)
	
	def bind(self, name, value):
		self.bindings[name] = value
		
	def merge(self, other_hash):
		self.bindings.update(other_hash)
	
	def __str__(self):
		return "#<%s:%x(%s)>" % (self.__class__.name, id(self), str(self.bindings))
	
class Solutions(dict):
	
	def filter(self, criteria):
		l = []
		if type(fn) == dict:
			for solution in self:
				for key, value in criteria.items():
					flag = True
					if solution.get(key) != value:
						flag = False
						break
				if flag:
					l.append(solution)
		elif hasattr(obj, '__call__'):
			for solution in self:
				if type(solution) != Solution:
					solution = Solution(solution)
				if criteria(solution):
					l.append(solution)				
		return l

	def order(self, *variables):
		def compare(a,b):
			a = variable.map(lambda v: str(a.get(v)))
			b = variable.map(lambda v: str(b.get(v)))
			return cmp(a,b)
		sorted(self, cmp = compare)

	def project(self, *variables):
		for i in xrange(0,len(self)):
			for key, value in self[i].bindings.items():
				if key not in variables:
					self[i].bindings.pop(key)
			
	@property		
	def variable_names(self):
		variables = set()
		for solution in self:
			for key in solution.each_key():
				variables.update(key)
		return variables
		
	@property
	def has_variables(self, variables):
		for solution in self:
			if not solution.has_variables(variables):
				return False
		return True
		
class Pattern(model.Statement):
	
	def __init__(self, subject = None, predicate = None, object = None, options = {}):

		super(Pattern, self).__init__(subject, predicate, object, options)
		if type(self.subject) == str:
			self.subject = Variable(self.subject)
		
		if type(self.context) == str:
			self.context = Variable(self.context)
			
		if type(self.predicate) == str:
			self.predicate = Variable(self.predicate)
			
		if type(self.object) == str:
			self.object = Variable(self.object)

		self.cost = 0

	@classmethod
	def factory(self, pattern, options = {}):
		if isinstance(pattern, list):
			return Pattern(pattern[0], pattern[1], pattern[2], options.update({'context' : pattern[3]}))
 		elif isinstance(pattern, model.Statement):
	 		options.update({'context' : pattern.context })
			return Pattern(pattern.subject, pattern.predicate, pattern.object, options)
		elif isinstance(pattern, Pattern):
			return pattern
		elif isinstance(pattern, dict):
			options.update(pattern)
			return Pattern(options)

	@property
	def is_blank(self):
		return (self.subject == None) and (self.predicate == None) and (self.object == None) and (self.context == None)

	@property
	def is_constant(self):
		return not self.variable
		
	@property
	def is_variable(self):
		return (self.subject == None) or (self.predicate == None) or (self.object == None) or self.has_variable
		
	@property
	def has_variable(self):
		return (type(self.subject) == Variable) or (type(self.predicate) == Variable) or (type(self.object) == Variable) or (type(self.context) == Variable)
		
	@property
	def is_optional(self):
		return self.options.get("optional") == True
		
	def execute(self, queryable, bindings = {}):
		query = {
			'subject' : bindings.get(self.subject) if self.subject.is_variable else self.subject,
			'predicate' : bindings.get(self.predicate) if self.predicate.is_variable else self.predicate,
			'object' : bindings.get(self.object) if self.object.is_variable else self.object					
		}
		
		variables = self.variables()
		if self.variable_count == len(variables):
			for statement in queryable.query(query):
				yield statement
		else:
			terms = None
			for key in variables.keys():
				t = variable_terms(key)
				if len(t) > 1:
					terms = t
					break
			for statement in queryable.query(query):
				s = set()
				for term in terms:
					s.update(getattr(statement,term)())
				if len(s) == 1:
					yield statement

	def solution(self, statement):
		solution = Solution()
		if self.subject.is_variable:
			solution.bind('subject', statement.subject)
			
		if self.predicate.is_variable:
			solution.bind('predicate', statement.predicate)
			
		if self.object.is_variable:
			solution.bind('object', statement.object)
			
	def variable_terms(self, name = None):
		terms = []
		if (type(self.subject) == Variable) and ( (not name) or (name == self.subject.name) ):
			terms.append('subject')
			
		if (type(self.predicate) == Variable) and ( (not name) or (name == self.predicate.name) ):
			terms.append('predicate')
			
		if (type(self.object) == Variable) and ( (not name) or (name == self.object.name) ):
			terms.append('object')					
		
		return terms
		
	@property	
	def variable_count(self):
		count = 0
		if type(self.subject) == Variable: 
			count += 1
		if type(self.predicate) == Variable: 
			count += 1
		if type(self.object) == Variable: 
			count += 1					
		
		return count
		
	@property
	def variables(self):
		variables = {}
		if type(self.subject) == Variable: 
			variables.update(self.subject.variables)
		if type(self.predicate) == Variable: 
			variables.update(self.predicate.variables)
		if type(self.object) == Variable: 
			variable.update(self.object.variables)	
			
		return variables
		
	@property
	def is_bindings(self):
		return len(self.bindings) > 0
		
	@property
	def binding_count(self):
		return len(self.bindings)	
		
	@property
	def bindings(self):
		bindings = {}
		if type(self.subject) == Variable: 		
			bindings.merge(self.subject.bindings)
		if type(self.predicate) == Variable: 		
			bindings.merge(self.predicate.bindings)
		if type(self.object) == Variable: 		
			bindings.merge(self.object.bindings)		
			
		return bindings
		
	@property
	def is_bound(self):
		if len(self.variables) == 0:
			return False
		for variable in self.variables.values():
			if not variable.is_bound:
				return False
		return True

	@property
	def is_unbound(self):
		if len(self.variables) == 0:
			return False
		for variable in self.variables.values():
			if not variable.is_unbound:
				return False
		return True

	def bound_variables(self):
		variables = self.variables.copy()
		for key, value in variables.items():
			if value.is_unbound:
				variables.pop(key)
		return variables
			
	def unbound_variables(self):
		variables = self.variables.copy()
		for key, value in variables.items():
			if value.is_bound:
				variables.pop(key)
		return variables

	def __str__(self):
		s = "["
		if self.is_optional:
			s += "OPTIONAL "

		s += str(self.subject) + " "
		s += str(self.predicate) + " "
		s += str(self.object) + " ."
		s += "]"
		return s

class Query(object):

	def __init__(self, patterns = None, options = {}):
		self.options = options
		self.variables = {}
		self.solutions = options.get('solutions')
		if not self.solutions:
			self.solutions = Solutions()
			
		if isinstance(patterns, dict):
			self.patterns = self.compile_hash_patterns(patterns)
		elif isinstance(patterns, list):
			self.patterns = patterns
		else:
			self.patterns = []

	def append(self, pattern, options = {}):
		self.patterns.append(Pattern.factory(pattern, options))	
		
	def optimize(self):
		def compare(a, b):
			cmp(a.cost, b.cost)
		sorted(self.pattern, cmp = compare)

	def execute(self, queryable, options = {}):
		if not options.get('bindings'):
			options['bindings'] = {}
			
		self.solutions = Solutions()
		solutions.append(Solution({}))
		
		for pattern in self.patterns:
			old_solutions, self.solutions = self.solutions, Solutions()
			
			for variable in options['bindings']:
				if variable in pattern.variables:
					unbound_solutions, old_solutions = old_solutions, Solutions()
					for binding in options['bindings'][variable]:
						for solution in unbound_solutions:
							solution.update({'variable': binding})
							old_solutions.append(solution)
					options['bindings'].pop(variable)

			for solution in old_solutions:
				for statement in pattern.execute(queryable, solution):
					solution.update(pattern.solution(statement))
					self.solutions.append(solution)
					
			if len(self.solutions) == 0:
				return self.solutions
			
			if not pattern.optional:
				for variable in pattern.variables.keys():
					if variable not in self.solutions.variable_names:
						return Solution()
						
			
		return self.solutions
		
	@property
	def failed(self):
		return len(self.solutions) == 0
		
	@property
	def matched(self):
		return not self.failed

	def each_solution(self):
		for solution in self.solutions:
			yield solution
			
	def compile_hash_patterns(self, hash_patterns):
		patterns = []
		for s, pos in hash_patterns.items():
			if isinstance(pos, dict):
				for p, os in pos.items():
					if isinstance(os, dict):
						patterns.update(os.keys.map( lambda o: [s, p, o]))
						patterns.update(self.compile_hash_patterns(os))
					elif isinstance(os, list):
						patterns.update(os.map( lambda o: [s, p, o]))
					else:
						patterns.append([s, p, os])
			else:
				raise Exception("Invalid hash pattern: %s", hash_patterns)
				
	def __add__(self, other):
		for pattern in other.patterns:
			self.patterns.append(pattern)

	def __repr__(self):
		return "Query(%s)%s" % (self.options.get('context') or 'None', repr(self.patterns))
		return res
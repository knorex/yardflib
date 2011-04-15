import re
import copy
from urlparse import urlparse, ParseResult
from util import *
import datetime

class Value(object):

	@property
	def is_graph(self):
		return False

	@property
	def is_literal(self):
		return False

	@property
	def is_node(self):
		return False

	@property
	def is_resource(self):
		return False

	@property
	def is_statement(self):
		return False

	@property
	def is_iri(self):
		return self.uri

	@property
	def is_variable(self):
		return False

	def to_rdf(self):
		return self

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, str(self))

class Term(Value):
	
	def __cmp__(self, other):
		return cmp(str(self), str(other))
	
	def evaluate(self, bindings):
		return self

	@property
	def is_constant(self):
		return not self.is_variable
	
class Resource(Term):
	
	@property
	def is_resource(self):
		return True
	
	@classmethod
	def new(self, *args):
		arg = args.pop(0)
		if type(arg) == str:
			match = re.match("^_:(.*)$", arg)
			if match:
				return Node(match.group(1), *args)
			else:
				return Node.intern(arg, *args)
		else:
			return URI(arg, *args)
			
class URI(Resource):
	
	CACHE_SIZE = -1
	
	_cache = None

	@classmethod	
	def intern(self, s):
		if not URI._cache:
			URI._cache = Cache(URI.CACHE_SIZE)
		uri = URI._cache.get(str(s))
		if not uri:
			uri = URI(s)
			URI._cache.set(s, uri)
		return uri
		
			
	@classmethod			
	def parse(self, s):
		return URI(s)
		
	def __init__(self, uri_or_options):
		#TODO: uri_or_options could be a dict e.g {'scheme' : 'http', 'host' : 'rdf.rubyforge.org', 'path' : '/'}
		if type(uri_or_options) == ParseResult:
			self.uri = uri_or_options
		else:
			self.uri = urlparse(str(uri_or_options))
		self._qname = ""
			
	def starts_with(string):
		return str(self).find(string) == 0		

		
	def ends_with(self, s):
		return str(self)[-len(s):] == s
			
	@property
	def is_anonymous(self):
		return False

	@property
	def is_uri(self):
		return True
		
	@property
	def is_urn(self):
		return self.starts_with('urn:')
		
	@property
	def is_url(self):
		return not self.is_urn
		
	@property
	def length(self):
		len(str(self))
	
	@property
	def size(self):
		return self.length
		
	def validate(self):
		return self
		
	def canonicalize(self):
		return self
		
	def join(self, *uris):
		result = self.uri[:]
		for uri in uris:
			result = result + uri
		return URI(result)
		
	def __divmod__(self, fragment):
		if 'to_uri' in dir(fragment):
			fragment = fragment.to_uri()
		else:
			fragment = URI.Intern(str(fragment))
		
		if self.is_urn:
			return URI.intern(re.sub(":+$", "", str(self)) + ":" + re.sub("^:+", "", fragment))
		else:  
			if str(self)[-1] == "#":
				if str(fragment)[0] == "/": # Base ending with '#', fragment beginning with '/'.  The fragment wins, we use '/'.
					return URI.intern(re.sub("#+$", "", str(self)) + "/" + re.sub("^\/+", "", str(fragment)))
				else:
					return URI.intern(re.sub("#+$", "", str(self)) + "#" + re.sub("^#+", "", str(fragment)))
			else:  # includes '/'.  Results from bases ending in '/' are the same as if there were no trailing slash.
				if str(fragment)[0] == "#": # Base ending with '/', fragment beginning with '#'.  The fragment wins, we use '#'.
					return URI.intern(re.sub("\/+$", "", str(self)) + "#" + re.sub("^#+", "", str(fragment)))
				else:
					return URI.intern(re.sub("\/+$", "", str(self)) + "/" + re.sub("^\/+", "", str(fragment)))				

	def __add__(self, other):
		return URI.intern(str(self) + str(other))

	def __eq__(self, other):
		return str(self) == str(other)

	@property
	def is_root(self):
		return (len(self.path) == 0) or (self.path == "/")

	def root(self):
		if self.is_root:
			return self
		else:
			uri = self.dup()
			uri.path = "/"
			return uri

	@property
	def has_parent(self):
		return not self.is_root

	@property
	def hash(self):
		return self.uri.__hash__()
		
	def to_uri(self):
		return self	
		
	def parent(self):
		if self.is_root:
			return None
		else:
			path = Pathname(self.path).parent
			if path:
				uri = self.dup()
				uri.path = str(path)
				if uri.is_root:
					uri.path += "/"
				return uri		
			
	def qname(self):
		if self._qname:
			return self._qname
		else:
			import vocab
			match = re.search("[:/#]([^:/#]*)$", str(self))
			if match:
				local_name = match.group(1)
				if len(local_name) == 0:
					vocab_uri = str(self)
				else:
					vocab_uri = str(self)[0:-len(local_name)]
				for v in vocab.VOCABS():
					if v.uri == vocab_uri:
						prefix = v.__prefix__
						return [prefix, local_name if len(local_name) else None]
			else:
				for v in VOCABS():
					vocab_uri = v.to_uri
					if self.starts_with(vocab_uri):
						prefix = v.__prefix__
					local_name = str(self)[len(vocab_uri):]
					return [prefix, local_name]
			
		return None

	def dup(self):
		return URI(this.uri)
		
	def __str__(self):
		return self.uri.geturl()

class Node(Resource):
	
	def __init__(self, i = None):
		if i: 
			self.id = i
		else: 
			self.id = str(id(self))
	
	@classmethod
	def intern(self, id):
		return Node(id)
	
	@property
	def is_node(self):
		return True
		
	@property
	def is_labeled(self):
		return not self.is_unlabeled
		
	@property
	def is_anonymous(self):
		return True	
	
	@property
	def is_unlabeled(self):
		return self.is_anonymous
		
	def __eq__(self, other):
		return type(other) == Node and other.is_node and ('node' in dir(other)) and ('id' in dir(other)) and (self.id == other.id)

	def __str__(self):
		return "_:%s" % self.id	

class Statement(Value):
	
	def __init__(self, subject = None, predicate = None, object = None, options = {}):

		if isinstance(subject, dict):
			self.options = subject.copy()
			self.subject = self.options.get('subject')
			self.predicate = self.options.get('predicate')
			self.object = self.options.get('object')
		else:
			self.options = options.copy()
			self.subject = subject
			self.predicate = predicate
			self.object = object
		self.context = options.get('context')
		
		self.id = options.get('id')

		if isinstance(self.context, str):
			self.context = Node.intern(self.context)

		if isinstance(self.subject, str):
			self.subject = Node.intern(self.subject)
			
		if isinstance(self.predicate, str):
			self.subject = Node.intern(self.predicate)
		
		if self.object != None:
			if isinstance(self.object, str):
				self.object = Node.intern(self.object)
			elif isinstance(self.object, Term):
				pass
			else:
				self.object = Literal(self.object)

	@classmethod
	def factory(self, statement, options = {}):
		if isinstance(statement, list):
			return Statement(statement[0], statement[1], statement[2], options.update({'context' : statement[3] if len(statement) > 3 else None}))
		elif isinstance(statement, Pattern):
			return Statement(statement.subject, statement.predicate, statement.object, options.update({'context' : statement.context }))
		elif isinstance(statement, Statement):
			return statement
		elif isinstance(statement, dict):
			options.update(statement)
			return Statement(options)
			
	@property
	def has_subject(self):
		return self.subject != None
			
	@property
	def has_object(self):
		return self.object != None

	@property
	def has_predicate(self):
		return self.predicate != None

	@property
	def has_context(self):
		return self.context != None

	@property
	def is_valid(self):		
		return self.has_subject and self.has_predicate and self.has_object

	@property
	def is_invalid(self):
		return not self.is_valid
		
	@property
	def has_blank_nodes(self):
		return (self.has_object and self.object.is_node) or (self.has_subject and subject.is_node)
		
	@property 
	def is_asserted(self):
		return not self.is_quoted
		
	@property
	def is_quoted(self):
		return False
		
	@property
	def is_inferred(self):
		return False
		
	@property
	def has_graph(self):
		return self.has_context
	
	def __eq__(self, other):
		return hasattr(other, 'to_a') and (self.to_triple() == other.to_a())
		
	def to_triple(self):
		return [self.subject, self.predicate, self.object]
			
	def to_quad(self):	
		return [self.subject, self.predicate, self.object, self.context]
		
	def to_dict(self):	
		return {'subject' : self.subject, 'predicate': self.predicate, 'object': self.object, 'context': self.context}
		
	def __str__(self):
		s = ""
		if type(self.subject) == Node:
			s += str(self.subject)
		elif type(self.subject) == URI:
			s += "<%s>" % self.subject
		else:
			s += repr(self.subject)
			
		s += " <%s>" % self.predicate
		
		if (type(self.object) == Node) or (type(self.object) == Literal):
			s += str(self.object)
		elif type(self.subject) == URI:
			s += "<%s>" % self.object
		else:
			s += repr(self.subject)		
		
		if self.context == None:
			s += " ."
		else:
			s += " <%s>" % self.context

		return s

	def __repr__(self):
		return repr(self.to_sxa())

	def to_sxa(self):
		return ['triple', self.subject, self.predicate, self.object]

	def reified(self, options = {}):
		#TODO: not completed
		pass

def Literal(value, options = {}):

	import literal
	import vocab
	
	datatype = options.get('datatype')
	if datatype:
		datetype_uri = URI(datatype)
		if datetype_uri == vocab.XSD.get_prop('boolean'):
			cls = literal.Boolean
		elif datetype_uri == vocab.XSD.get_prop('integer'):
			cls = literal.Integer
		elif datetype_uri == vocab.XSD.get_prop('decimal'):		
			cls = literal.Decimal
		elif datetype_uri == vocab.XSD.get_prop('double'):
			cls = literal.double
		elif datetype_uri == vocab.XSD.get_prop('dateTime'):
			cls = literal.DateTime
		elif datetype_uri == vocab.XSD.get_prop('date'):
			cls = literal.Date
		elif datetype_uri == vocab.XSD.get_prop('time'):
			cls = literal.Time
		elif datetype_uri == vocab.XSD.get_prop('token'):
			cls = literal.Token
		else:
			cls = None
	else:
		if type(value) == bool:
			cls = literal.Boolean
		elif type(value) == int:
			cls = literal.Integer
		elif type(value) == long:
			cls = literal.Decimal
		elif type(value) == float:
			cls = literal.Double
		elif type(value) == datetime.datetime:
			cls = literal.DateTime
		elif type(value) == datetime.date:
			cls = literal.Date
		elif type(value) == datetime.time:
			cls = literal.Time
		elif type(value) == str:
			cls = literal.Token
		else: 
			cls = None
			
	if cls:
		return cls(value, options)
	else:
		return None
			
			
			
			
			
			
			
			
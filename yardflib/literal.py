from dateutil import parser as datetime_parser
import re
import datetime
import model
import vocab

class BaseLiteral(model.Term):
	
	datatype = None
	language = None
	
	def __init__(self, value, options = {}):
		self.object = value
		
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None
			
		self.language = options.get('language')
		

	def __str__(self):
		return self.string
		
	@property
	def is_plain(self):
		return (self.datatype == None) and (self.language == None)

	@property
	def is_typed(self):
		return self.datatype != None

class Numeric(BaseLiteral):

	def __init__(self):
		pass

class Boolean(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('boolean')
	GRAMMAR = re.compile("^(true|false|1|0)$",re.I)

	def __init__(self, value, options = {}):
		super(Boolean, self).__init__(value, options)
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		value = str(value).lower()
		if (value == "true") or (value == "1"):
			self.object = True
		else:
			self.object = False
		
	def __eq__(self, other):
		return other == self.object

	def __cmp__(self, other):
		return cmp(str(self.object), str(other))
	
	def __repr__(self):
		if self == True:
			return "literal.Boolean(TRUE)"
		else:
			return "literal.Boolean(FALSE)"

class Date(BaseLiteral):

	DATATYPE = vocab.XSD.get_prop('date')
	GRAMMAR  = re.compile("(\A-?\d{4}-\d{2}-\d{2}(([\+\-]\d{2}:\d{2})|UTC|Z)?\Z)")
	
	def __init__(self, value, options = {}):
		super(Date, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		if type(value) == datetime.date:
			self.object = value
		else:
			self.object = datetime_parser.parse(value).date()

	def __eq__(self, other):
		return other == self.object

	def __cmp__(self, other):
		return cmp(self.object, other.object)

	def __str__(self):
		if self.string:
			return self.string
		else:
			return self.object.strftime("%Y-%m-%d%Z")

class DateTime(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('dateTime')
	GRAMMAR  = re.compile("(\A-?\d{4}-\d{2}-\d{2}(([\+\-]\d{2}:\d{2})|UTC|Z)?\Z)")
	
	def __init__(self, value, options = {}):
		super(DateTime, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		if type(value) == datetime.datetime:
			self.object = value
		else:
			self.object = datetime_parser.parse(value)
		
	def __eq__(self, other):
		return other == self.object

	def __cmp__(self, other):
		return cmp(self.object, other.object)
		
	def __str__(self):
		if self.string:
			return self.string
		else:
			return self.object.strftime("%Y-%m-%dT%H:%M:%S%Z")	
		
class Decimal(Numeric):
	
	DATATYPE = vocab.XSD.get_prop('decimal')
	
	def __init__(self, value, options = {}):
		super(Decimal, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		if (type(value) == long) or (type(value) == int):
			self.object = value
		else:
			self.object = long(value)
			
	def __cmp__(self, other):
		return cmp(self.object, long(other))
			
	@property
	def to_i(self):
		return self.object			

	def __div__(self, other):
		Literal(self.to_i / other.to_i)		

	def __add__(self, other):
		Literal(self.to_i + other.to_i)
		
	def __sub__(self, other):
		Literal(self.to_i - other.to_i)
		
	def __mull__(self, other):
		Literal(self.to_i * other.to_i)
			
	def __neg__(self):
		Literal(-self.to_i)

class Double(Numeric):
	
	DATATYPE = vocab.XSD.get_prop('double')
	
	def __init__(self, value, options = {}):
		super(Double, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		if (type(value) == float):
			self.object = value
		else:
			self.object = float(value)
			
	def __cmp__(self, other):
		return cmp(self.object, float(other))
			
class Integer(Decimal):
	
	DATATYPE = vocab.XSD.get_prop('integer')
	
	def __init__(self, value, options = {}):
		super(Integer, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = model.URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		if (type(value) == long) or (type(value) == int):
			self.object = value
		else:
			self.object = int(value)

	def __cmp__(self, other):
		if isinstance(other, Integer) or isinstance(other, Decimal):
			return cmp(self.object, other.object)
		else: 
			return 1
	
	def to_i(self):
		return self.object	

class Time(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('time')
	
	def __init__(self, value, options = {}):
		super(Time, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		if type(value) == datetime.time:
			self.object = value
		else:
			self.object = datetime_parser.parse(value).time()

	def __str__(self):
		if self.string:
			return self.string
		else:
			return self.object.strftime("%H:%M:%S%Z")

class Token(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('token')
	
	def __init__(self, value, options = {}):
		super(Token, self).__init__(value, options)	
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE

		self.object = str(value)

	def __str__(self):
		if self.string:
			return self.string
		else:
			return str(self.value)
from dateutil import parser as datetime_parser
import re
import datetime
import model
import vocab

class BaseLiteral(model.Term):
	
	def __init__(self):
		pass

class Boolean(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('boolean')
	GRAMMAR = re.compile("^(true|false|1|0)$",re.I)

	def __init__(self, value, options = {}):
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

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
			return "literal.TRUE"
		else:
			return "literal.FALSE"
			
class Date(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('date')
	GRAMMAR  = re.compile("(\A-?\d{4}-\d{2}-\d{2}(([\+\-]\d{2}:\d{2})|UTC|Z)?\Z)")
	
	def __init__(self, value, options = {}):
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

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
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

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
		
class Decimal(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('decimal')
	
	def __init__(self, value, options = {}):
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

		if (type(value) == long) or (type(value) == int):
			self.object = value
		else:
			self.object = long(value)
			
	def __cmp__(self, other):
		return cmp(self.object, long(other))
			
			
class Double(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('double')
	
	def __init__(self, value, options = {}):
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

		if (type(value) == float):
			self.object = value
		else:
			self.object = float(value)
			
	def __cmp__(self, other):
		return cmp(self.object, float(other))
			
class Integer(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('integer')
	
	def __init__(self, value, options = {}):
		if options.get('datatype'):
			self.datatype = model.URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

		if (type(value) == long) or (type(value) == int):
			self.object = value
		else:
			self.object = int(value)
			
	def __cmp__(self, other):
		if isinstance(other, Integer) or isinstance(other, Decimal):
			return cmp(self.object, other.object)
		else: 
			return False
		

class Time(BaseLiteral):
	
	DATATYPE = vocab.XSD.get_prop('time')
	
	def __init__(self, value, options = {}):
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

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
		if options.get('datatype'):
			self.datatype = URI(options['datatype'])
		else:
			self.datatype = self.DATATYPE
			
		if options.has_key('lexical'):
			self.string = options['lexical']
		elif type(value) == str:
			self.string = value
		else:
			self.string = None

		self.object = str(value)

	def __str__(self):
		if self.string:
			return self.string
		else:
			return str(self.value)
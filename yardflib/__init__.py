__version__ = "0.1"
__date__ = "2011/03/24"

__all__ = [
	'Statement',
	'URI',
	'Node',
	'Literal',
	
	'Query'
    ]

import sys

# generator expressions require 2.4
assert sys.version_info >= (2, 4, 0), "yardflib requires Python 2.4 or higher"
del sys

import logging
_LOGGER = logging.getLogger("yardflib")
_LOGGER.info("version: %s" % __version__)


from yardflib.model import Statement, URI, Node, Literal
from yardflib.query import Query

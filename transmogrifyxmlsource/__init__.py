#

from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher
from transmogrify.pathsorter.treeserializer import TreeSerializer

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from urlparse import urlparse, urljoin
import logging
import lxml

class XMLSource(object):
    classProvides(ISectionBlueprint)
    implements(ISection)


    def __init__(self, transmogrifier, name, options, previous):
        self.previous = TreeSerializer(transmogrifier, name, options, previous)
        self.context = transmogrifier.context

        self.xmlfile = options.get('filename',options.get('xmlfile',''))    
        self.path = options.get('path', '')
        self.type = options.get('type', 'Document')
        self.itemtag = options.get('itemtag')
        self.pathtag = options.get('pathtag')
        self.logger = logging.getLogger(name)

    def __iter__(self):
        for item in self.previous:
            yield item

        f = open(self.xmlfile, "r")
        events = ("start", "end", "start-ns", "end-ns")
        context = lxml.etree.iterparse(f, events=events)
        item = {}
        for action, elem in context:
            if action in ('start') and elem.tag == self.itemtag:
                item = {}
            elif action == 'end' and elem.tag == self.itemtag:
                item['_path'] = item[self.pathtag]
                item['_type'] = self.type
                self.logger.debug(str(item))
                yield item
                item = None
            elif action == 'end' and item is not None:
                #import pdb; pdb.set_trace()
                item[elem.tag] = elem.text

            




#

from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher
from transmogrify.siteanalyser.treeserializer import TreeSerializer
from pprint import pformat
from collective.transmogrifier.utils import Expression
import datetime
import re


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
        self.pathattribute = options.get('pathattribute')
        self.dropfields = [f for f in options.get('dropfields').split() if f]
        self.fieldsexpr = []
        for f in options.get('fieldsexpr').split('\n'):
            f = f.strip()
            if not f or '=' not in f:
                continue
            key, tal = [v.strip() for v in f.split('=')]
            expr = Expression(tal, transmogrifier, name, options, datetime=datetime, re=re)
            self.fieldsexpr.append((key, expr))

        self.logger = logging.getLogger(name)

    def __iter__(self):
        for item in self.previous:
            yield item

        f = open(self.xmlfile, "r")
        events = ("start", "end", "start-ns", "end-ns")
        context = lxml.etree.iterparse(f, events=events)
        item = {}
        depth = 0
        for action, elem in context:
            if action in ('start') and elem.tag == self.itemtag:
                item = {}
                itemdepth = depth
            elif action == 'end' and elem.tag == self.itemtag:
                if self.pathattribute:
                    item['_path'] = elem.get(self.pathattribute)
                else:
                    item['_path'] = item[self.pathtag]
                item['_type'] = self.type

                self.transform_item(item, elem)

                self.logger.debug(pformat(item))

                yield item
                item = None
            elif action == 'end' and item is not None and depth <= itemdepth + 2:
                #import pdb; pdb.set_trace()
                if len(elem) == 0:
                    item[elem.tag] = elem.text
                else:
                    item[elem.tag] = lxml.etree.tostring(elem)


            if action in ('start'):
                depth += 1
            elif action == 'end':
                depth -= 1

    def transform_item(self, item, elem):
        for key, expression in self.fieldsexpr:
            item[key] = expression(item, elem=elem, **item)
        for key in self.dropfields:
            if key in item:
                del item[key]


            




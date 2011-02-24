from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='transmogrify.xmlsource',
      version=version,
      description="Simple xml reader for a transmogrifier pipeline",
      long_description="""\
"""+open('README.rst').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='transmogrifier xml plone',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='https://github.com/collective/transmogrify.xmlsource',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.transmogrifier',
          'lxml',
          ],
      entry_points="""
            [z3c.autoinclude.plugin]
            target = transmogrify
            """,
      )

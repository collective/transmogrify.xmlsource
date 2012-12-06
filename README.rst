XMLSource
=========

A simple transmogrifier blueprint to read xml files of the form ::

    <container>
      <item>
        <field1>value1</field1>
        <field2>value2</field2>
        ...
      </item>
      ...
    </container>

and will spit out items of the form ::

 {'field1':'value',
  'field2':'value',
  '_path':'value1',
  '_type':'MyCustomType'
  }



Example
-------

The following example uses `funnelweb` and `ploneremote` to upload
content in an xml file from the commandline

First create a custom `pipeline.cfg` ::

    [transmogrifier]
    pipeline =
        xmlsource
        ploneupload
        ploneupdate

    [xmlsource]
    blueprint = transmogrify.xmlsource
    filename = items.xml
    pathtag = field1
    itemtag = item
    type = MyCustomType

    [ploneupload]
    blueprint = transmogrify.ploneremote.remoteconstructor
    target = http://admin:admin@localhost/Plone/mycontent

    [ploneupdate]
    blueprint = transmogrify.ploneremote.remoteschemaupdater
    target = ${ploneupload:target}

Now install `funnelweb` using a `buildout.cfg` ::

    [buildout]
    parts = convertxml

    [convertxml]
    recipe = funnelweb
    pipeline=wynhotels.cfg
    eggs = transmogrify.xmlsource

bootstrap ::

    $> easy_install zc.buildout
    $> buildout init
    $> bin/buildout

and now run your custom converter ::

    $> bin/convertxml

or ::

    $> bin/convertxml --xmlsource:filename=test.xml --ploneupload:target=http://admin:admin@localhost/Plone/folder1

The converter parses the xml and uploads to plone via xmlrpc. or
construct your own pipeline to transform the content into whatever or whereever.

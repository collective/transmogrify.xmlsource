XMLSource
=========

A simple transmogrifier blueprint to read xml files of the form ::

    <container>
      <item>
        <field1>value</field1>
        <field2>value</field2>
        ...
      </item>
      ...
    </container>


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
    xmlfile = items.xml
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

and now run your custom converter

    $> bin/convertxml

The converter parses the xml and uploads to plone via xmlrpc. or
construct your own pipeline to transform the content into whatever or whereever.

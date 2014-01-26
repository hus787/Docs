

import os, shutil

import inspect
path = inspect.getfile( inspect.currentframe() )
path = path.replace("\\", "/")
if path.startswith("/"):
    base_dir = os.path.dirname(path)
    base_dir = os.path.dirname(base_dir)
else:
    base_dir = ".."


build_dir = "%s/build" % base_dir
if not os.path.exists(build_dir):
    os.makedirs(build_dir)


books = [
    'tactic-developer',
    'tactic-end-user',
    'tactic-setup'
]




for book in books:
    cmd = 'asciidoc -b docbook %s/book/%s.adoc' % (base_dir, book)
    print
    print cmd
    print
    os.system(cmd)

    xml_path = "%s/build/%s.xml" % (base_dir, book)
    if os.path.exists(xml_path):
        os.unlink(xml_path)
    shutil.move("%s/book/%s.xml" % (base_dir, book), xml_path)

    #cmd = 'xsltproc --nonet /etc/asciidoc/docbook-xsl/chunked.xsl %s.xml' % book
    cmd = 'a2x -D %s/build -f chunked %s' % (base_dir, xml_path)
    print
    print cmd
    print
    os.system(cmd)

    cmd = 'a2x -D %s/build -f xhtml %s' % (base_dir, xml_path)
    print
    print cmd
    print
    os.system(cmd)

    cmd = 'a2x -D %s/build -f pdf %s' % (base_dir, xml_path)
    print
    print cmd
    print
    os.system(cmd)


    os.unlink(xml_path)






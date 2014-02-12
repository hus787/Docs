

import os, shutil

import inspect




path = inspect.getfile( inspect.currentframe() )
path = path.replace("\\", "/")
if path.startswith("/"):
    base_dir = os.path.dirname(path)
    base_dir = os.path.dirname(base_dir)
elif path.startswith("bin"):
    base_dir = "."
else:
    base_dir = ".."


build_dir = "%s/build" % base_dir
if not os.path.exists(build_dir):
    os.makedirs(build_dir)


def find_media(base_dir):

    paths = []
    for root, dirnames, basenames in os.walk(base_dir):

        for dirname in dirnames:
            if dirname == "media":
                media_dir = "%s/%s" % (root, dirname)
                media_basenames = os.listdir(media_dir)
                for media_basename in media_basenames:
                    path = "%s/%s" % (media_dir, media_basename)
                    paths.append(path)
    return paths




books = [
    'tactic-developer',
    'tactic-end-user',
    'tactic-setup',
    'tactic-sys-admin',
    'tactic-quickstart',
    'tactic-tutorial'
]




for book in books:

    print "Looking for media: "
    media_dir = "%s/section/doc/%s" % (base_dir, book)
    paths = find_media(media_dir)
    print " ... found %s images" % len(paths)

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






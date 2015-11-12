#!/usr/bin/env python
#----------------------------------------------------------------------------
from sys import argv
from os import makedirs
from os.path import basename, abspath, isdir, isfile, exists, join, dirname
from shutil import rmtree
from xml.dom.minidom import parse, Node
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context
from StringIO import StringIO

ITEMS = dict()
KINDS = dict()
SEQUENCE = 1

#----------------------------------------------------------------------------
# Usage information and error reporting
#----------------------------------------------------------------------------

USAGE = """
Usage:

    %s inputdir outputdir

Where:

    inputdir  - the directory containing the XML files generated by doxygen.
    outputdir - the output directory to place the generated Jekyll files.

IMPORTANT: The output directory will be deleted prior to generating new files.
"""

def showUsage(msg = None):
  """ Show usage information and exit
  """
  if msg is not None:
    print "Error: %s\n" % msg
  print USAGE.strip() % argv[0]
  exit(1)

#----------------------------------------------------------------------------
# XML data loading
#----------------------------------------------------------------------------

def getChildByName(node, name):
  for child in node.childNodes:
    if (child.nodeType == Node.ELEMENT_NODE) and (child.tagName == name):
      return child
  return None

def getText(node):
  node.normalize()
  text = ""
  for child in node.childNodes:
    if child.nodeType == Node.TEXT_NODE:
      text = text + child.data
  return text

def getChildrenByTagName(parent, name, recursive = False):
  """ Iterator for finding child nodes by name
  """
  for child in parent.childNodes:
    if (child.nodeType == Node.ELEMENT_NODE) and (child.tagName == name):
      yield child
      if recursive:
        for c2 in getChildrenByTagName(child, name, recursive):
          yield c2

def getChildrenByNodeType(parent, typeid, recursive = False):
  """ Iterator for finding child nodes by name
  """
  for child in parent.childNodes:
    if child.nodeType == typeid:
      yield child
      if recursive:
        for c2 in getChildrenByNodeType(child, typeid, recursive):
          yield c2

class DocItem:
  """ Represents a documentation item
  """

  def __init__(self, node):
    global ITEMS, SEQUENCE
    self.refid = node.getAttribute("refid")
    self.kind = node.getAttribute("kind")
    self.name = getText(getChildByName(node, "name"))
    self.sequence = SEQUENCE
    # Update the sequence
    SEQUENCE = SEQUENCE + 1
    # Update the global mapping and the kinds
    ITEMS[self.refid] = self
    if not KINDS.has_key(self.kind):
      KINDS[self.kind] = list()
    KINDS[self.kind].append(self)

class Compound(DocItem):
  """ Represents a compound block
  """

  def __init__(self, node):
    DocItem.__init__(self, node)
    # Add all the children
    self.children = dict()
    for child in getChildrenByTagName(node, "member"):
      item = DocItem(child)
      self.children[item.refid] = item

def updateItem(node):
  global ITEMS
  refid = node.getAttribute("id")
  if not ITEMS.has_key(refid):
    print "Warning: Could not find definition for item %s" % refid
    return
  item = ITEMS[refid]
  kind = node.getAttribute("kind")
  if item.kind <> kind:
    print "Warning: Member definition is for a different kind %s vs %s" % (kind, item.kind)
    return
  # Add attributes
  for attr in getChildrenByNodeType(node, Node.ATTRIBUTE_NODE):
    if not attr.localName in ("id", "kind"):
      item.__dict__[attr.localName] = attr.value
  # Add child elements
  for child in getChildrenByNodeType(node, Node.ELEMENT_NODE):
    item.__dict__[child.tagName] = getText(child)

def loadData(indir):
  global ITEMS
  DATASET = dict()
  print "Loading index.xml"
  top = parse(join(indir, "index.xml")).documentElement
  # Find all top level compounds
  for node in top.getElementsByTagName("compound"):
    item = Compound(node)
    if not DATASET.has_key(item.kind):
      DATASET[item.kind] = dict()
    DATASET[item.kind][item.refid] = item
  print "%d documentation items found" % len(ITEMS)
  # Now get the detail for each one
  for kind in DATASET.keys():
    for entry in DATASET[kind].keys():
      print "Loading %s.xml" % entry
      top = parse(join(indir, entry + ".xml")).documentElement
      for node in top.getElementsByTagName("memberdef"):
        updateItem(node)

#----------------------------------------------------------------------------
# Output generation
#----------------------------------------------------------------------------

def processTemplate(template, outputname, lookup, docItem = None):
  print "  %s" % outputname
  buf = StringIO()
  # Set up the context
  context = Context(buf,
    docItem = docItem,
    docItems = ITEMS,
    docItemsByKind = KINDS
    )
  template.render_context(context)
  with open(outputname, "w") as output:
    output.write(buf.getvalue())

def generateDocs(outdir):
  global ITEMS, KINDS
  # Figure our where our templates are
  templates = join(abspath(dirname(argv[0])), "doxygen")
  if not isdir(templates):
    print "Error: No template directory at '%s'" % templates
  # Create the lookup engine for includes
  lookup = TemplateLookup(directories = [ templates, join(templates, "include") ])
  # Generate the index page first
  try:
    template = lookup.get_template("index.html")
    processTemplate(template, join(outdir, "index.html"), lookup)
  except Exception, ex:
    print "Warning: Could not process 'index.html'"
  # Process each item
  for name in ITEMS.keys():
    item = ITEMS[name]
    try:
      template = lookup.get_template("%s.html" % item.kind)
      processTemplate(template, join(outdir, "%s.html" % item.refid), lookup, item)
    except:
      pass

#----------------------------------------------------------------------------
# Main program
#----------------------------------------------------------------------------

if __name__ == "__main__":
  # Check args
  if len(argv) <> 3:
    showUsage();
  # Get the input directory and make sure it exists
  indir = abspath(argv[1])
  if not isdir(indir):
    showUsage("Input directory '%s' does not exist." % indir)
  if not isfile(join(indir, "index.xml")):
    showUsage("Input directory '%s' does not contain 'index.xml'." % indir)
  # Get the output directory and make sure it's empty
  outdir = abspath(argv[2])
  if exists(outdir):
    if not isdir(outdir):
      showUsage("Output path '%s' is  not a directory." % outdir)
    rmtree(outdir, onerror = lambda x, y, z: showUsage("Cannot remove existing directory '%s'" % outdir))
  # Create the output directory
  makedirs(outdir)
  # Now, load the dataset
  loadData(indir)
  print "Documentation types:"
  for key in sorted(KINDS.keys()):
    print "%-16s: %d" % (key, len(KINDS[key]))
  # Generate the documentation
  print "Generating output files ..."
  generateDocs(outdir)

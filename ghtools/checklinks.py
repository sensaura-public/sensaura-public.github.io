#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Simple tool to check for valid links on a site
#-----------------------------------------------------------------------------
from sys import argv
from os.path import dirname
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests

# Queue of URLs to check
urls = list()
checked = list()

if __name__ == "__main__":
  if len(argv) != 2:
    print "Usage:"
    print "\t%s site-to-check" % argv[0]
    exit(1)
  # Add the first URL to the list
  urls.append((argv[1], ""))
  details = urlparse(argv[1])
  base_scheme, base_netloc = details[0], details[1]
  passed = 0
  failed = 0
  while len(urls) > 0:
    # Grab the head of the list
    url, parent = urls[0]
    del urls[0]
    # Has it already been checked?
    if url in checked:
      continue
    checked.append(url)
    # Make the request and parse the data
    try:
      request = requests.get(url, verify=False)
      if request.status_code <> 200:
        raise Exception(request.status_code)
      parser = BeautifulSoup(unicode(request.text))
      passed = passed + 1
#      print "+ %s" % url
    except Exception, ex:
      failed = failed + 1
      print "- %s" % url
      print "  From %s" % parent
      continue
    # Look for any links in the document and add local ones
    details = urlparse(url)
    base_path = dirname(details[2])
    for ref in parser.find_all("a"):
      if not ref.has_attr('href'):
        continue
      details = urlparse(ref['href'])
      if ((details[0] == base_scheme) or (details[0] == "")) and ((details[1] == base_netloc) or (details[1] == "")):
        path = details[2]
        if (path[:1] <> "/") and (path <> ""):
          path = base_path + "/" + details[2]
        child = "%s://%s%s" % (base_scheme, base_netloc, path)
        if (child not in urls) and (child not in checked):
          urls.append((child, url))
  # All done
  print "Checked %d links (%d pass/%d fail)" % (passed + failed, passed, failed)
  if failed > 0:
    print "!! Incorrect links found"
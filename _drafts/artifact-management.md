---
title: Artifact Management
category: senshub
---
Distributing packages for NuGet, PyPi and Maven.
Want local (private) repositories during development, would like to cache public repositories to speed up rebuilds.

PyPi

https://pypi.python.org/pypi/pypiserver - Handles local packages and redirects to pypi.org for packages that are not found.

http://doc.devpi.net/latest/ - an alternative to the above. Looks more complex to set up and configure though. It does support caching.

NuGet

https://github.com/themotleyfool/Klondike - very simple solution, single self-hosted server (requires Mono).

Maven

http://archiva.apache.org/index.cgi - Apache Archiva. Supports local packages as well as caching from the main repository.

See also - http://blog.kdgregory.com/2011/08/using-local-repository-server-with.html

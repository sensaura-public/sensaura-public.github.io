This directory contains data elements which can be accessed through the
'site.data.name' where 'name' is the name of the file (without extension).

This template expects at least a 'sections.csv' file - this defines the
top level sections for the site group. This should be the same across
all sites.

Project sites will also have a 'subsections.csv' file - this allows them
to split up different things like 'tutorials', 'api', etc. When this
file is present a secondary navbar is added to the site.

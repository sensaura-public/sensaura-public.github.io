#!/bin/sh
#------------------------------------------------------------------
# Start Jekyll serving pages so all machines on the network can
# preview.
#------------------------------------------------------------------
bundler exec jekyll serve --host=0.0.0.0

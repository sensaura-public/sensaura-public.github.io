#!/bin/sh
#------------------------------------------------------------------
# Start Jekyll serving pages so all machines on the network can
# preview.
#------------------------------------------------------------------

# Allow user to override port number
PORT=4000
if [ "X$1" != "X" ]; then
  PORT=$1
fi

JEKYLL_ENV=local bundler exec jekyll serve --host=0.0.0.0 --port=${PORT} --drafts

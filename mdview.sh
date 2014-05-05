#!/usr/bin/env bash

##############################################
### Usage: mdview <file>
### CLI Tool for previewing markdown files ###
##############################################

# Generate a temporary file in /tmp
MDTEMPFILE=`mktemp /tmp/mdtemp.XXXXXXX`.html || exit 1

# Convert the input file to HTML and write it to the temporary file
Markdown.pl $1 > $MDTEMPFILE

# Open the temporary file with a browser
open -a Google\ Chrome $MDTEMPFILE

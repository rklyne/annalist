#!/bin/bash
#
# This is a one-off script used to update field definitions in sitedata
# with "field_value_mode" attributes.  The file is left here as an example 
# of how to do this kind of processing with bash, find and sed.
#
# A useful and accessible reference for sed is at http://www.grymoire.com/Unix/Sed.html
#

DATE=`date "+%Y-%m-%dT%H:%M:%S"`

for F in `find . -name "field_meta.jsonld"`; do

    # for F in ./_initial_values/field_meta.jsonld; do

    echo Processing $F ...

    # Belt-and-braces: keep timed backup
    # Use 'git clean -nX' (dry run) and 'git clean -fX' to remove .bak files 
    # after updated files have been committed.

    cp $F $F.$DATE.bak

    # Use sed to apply changes

    sed '
        /annal:field_render_type/ {
            a\
            \, "annal:field_value_mode":     "Value_direct"
        } ' $F >$F.new

    # Only do this last command when the script has been debugged and tested:
    # this is the point at which the original data is overwritten.

    # mv $F.new $F

done

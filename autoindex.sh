#!/bin/bash

# source: https://github.com/rioastamal/shdir-listing

SHDIR_DEPTH="1000"

shdir_listing_html() {
    [ -z "$1" ] && {
        echo "shdir_listing_html: Missing 1st arg for directory name." >&2
        return 1
    }

    [ -z "$2" ] && {
        echo "shdir_listing_html: Missing 2nd arg for root directory." >&2
        return 1
    }

    local output_file=$1/index.html
    local doc_root=$(echo "$1" | sed "s#$2##g")
    [ -z "$doc_root" ] && doc_root="/"
    echo "$doc_root" | grep -q '/$' || doc_root="$doc_root/"

    local html="<!DOCTYPE html>
<html>
<body>
<h2>Directory Listing $doc_root</h2>
<ul>"

    for _dir in $(find $1 -maxdepth 1 | sort); do
        [ "$_dir" = "$1" ] && continue

        local _dirname=$(basename $_dir)
        [ "$_dirname" = "index.html" ] && continue

        local suffix="/"

        [ -f "$_dir" ] && suffix=""

        html="${html}\n<li><a href=\"${_dirname}${suffix}\">${_dirname}</a></li>"
    done

    html="${html}\n</ul></body></html>"
    echo -e $html
}

shdir_create_index_file() {
    [ -z "$1" ] && {
        echo "shdir_create_index_file: Missing 1st arg for directory name." >&2
        return 1
    }

    [ -z "$2" ] && {
        echo "shdir_create_index_file: Missing 2nd arg for depth." >&2
        return 1
    }

    local depth=$2
    local suffix=""
    local root_dir="$1"

    [ "$SHDIR_DRY_RUN" = "yes" ] && suffix="[DRY RUN] "

    for _dir in $(find $1 -maxdepth $depth -type d | sort -r); do
        echo -n "${suffix}Creating index.html for ${_dir}..."

        [ -f "$_dir/index.html" ] && [ "$SHDIR_SKIP_INDEX" = "yes" ] && {
            echo "SKIP."
            continue
        }

        [ "$SHDIR_DRY_RUN" = "yes" ] && {
            echo "DONE."
            continue
        }

        [ "$SHDIR_EMPTY_HTML" = "yes" ] && {
            echo >$_dir/index.html && echo "DONE."
            continue
        }

        shdir_listing_html "$_dir" "$root_dir" >$_dir/index.html
        echo "DONE."
    done
}

shdir_create_index_file "$1" $SHDIR_DEPTH

exit 0

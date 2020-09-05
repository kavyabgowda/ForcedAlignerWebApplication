#!/bin/bash

set -e

SOX=sox
EXT=wav
SOXCMD="$SOX -G "%s" -b 16 "%s" remix - rate "%d" dither -s"

# check if SoX is present or not
command -v $SOX >/dev/null 2>&1 || fail "$SOX not found."

# args verification
while getopts "s:r:w:" OPT; do
    case $OPT in
        s)
            S=$OPTARG
            ;;
        r)
            R=$OPTARG
            ;;
        w)
            W=$OPTARG
            ;;
        \?)
            fail "Invalid option."
            ;;
        :)
            fail "Option '-$OPT' requires an argument."
    esac
done

# check if directory exists if absent create
[ -n "$R" ] || fail "Source (-r) flag not set."
[ -d "$R" ] || fail `printf "Source '%s' is not a directory." "$R"`
[ -n "$W" ] || fail "Sink (-w) flag not set."
mkdir -p "$W" || fail `printf "Cannot create directory '%s'." "$W"`
[ "$R" != "$W" ] || fail "Identical source and sink directories."

# Convert speech to 16khz sample rate
for SOURCEFILE in $R/*.$EXT; do
    SINKFILE=$W/`basename $SOURCEFILE`
    `printf "$SOXCMD" "$SOURCEFILE" "$SINKFILE" "$S" `
done

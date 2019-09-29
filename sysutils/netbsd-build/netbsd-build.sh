#!/bin/sh

_bomb()
{
    echo "$@"
    exit 1
}

ROOT="/zpool"
SRC="$ROOT/src"
XSRC="$ROOT/xsrc"
OBJ="$ROOT/obj"
TOOLS="$ROOT/tools"
CMD="./build.sh -u -U -O $OBJ -T $TOOLS -x -X $XSRC -j3"
HG="/usr/pkg/bin/hg"
SUDO="/usr/pkg/bin/sudo"

for dir in $ROOT $SRC $XSRC $OBJ $TOOLS; do
    test -d "$dir" || _bomb "$dir: not found"
done

for command in $SUDO $HG; do
    test -f "$command" || _bomb "$command: command not found"
done
 
cd "$XSRC" \
    && $SUDO $HG pull \
    && $SUDO $HG update

cd "$SRC" \
    && $SUDO $HG pull \
    && $SUDO $HG update \
    && $SUDO $CMD tools \
    && $SUDO $CMD distribution \
    && $SUDO $CMD kernel=GENERIC

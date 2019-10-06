#!/bin/sh

_bomb()
{
    echo "$@"
    exit 1
}

MACHINE="$(uname -m)"

ROOT="/zpool"
SRC="$ROOT/src"
XSRC="$ROOT/xsrc"
OBJ="$ROOT/obj"
TOOLS="$ROOT/tools"
RELEASE="$ROOT/releasedir"
DEST="$ROOT/destdir/$MACHINE"
CMD="./build.sh \
     -D $DEST \
     -N0 \
     -O $OBJ \
     -R $RELEASE \
     -T $TOOLS \
     -U \
     -X $XSRC \
     -m amd64 \
     -u \
     -x \
     -j3"
HG="/usr/pkg/bin/hg"
SUDO="/usr/pkg/bin/sudo"

for dir in $ROOT $SRC $XSRC $OBJ $TOOLS $RELEASE $DEST; do
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
    && $SUDO $CMD kernel=GENERIC \
    && $SUDO $CMD modules \
    && $SUDO $CMD distribution

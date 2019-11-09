#!/bin/sh
# Copyright (c) 2019 Yuuki Enomoto
# Copyright (c) 2001-2011 The NetBSD Foundation, Inc.
# All rights reserved.

_bomb()
{
    echo "$@"
    exit 1
}

_usage()
{
    cat << EOF
$0 [-r ROOTDIR] [-huU]

 Options
    -a              Set MACHINE_ARCH to arch.
                    [Default: deduced from MACHINE]
    -m              Set MACHINE to mach.  Some mach values are
                    actually aliases that set MACHINE/MACHINE_ARCH
                    pairs.  [Default: deduced from the host system
                    if the host OS is NetBSD]
    -r              Remove contents of TOOLDIR and DESTDIR before 
                    building.
    -u              *Do not* run "make cleandir" first.
                    Without this, everything is rebuilt, including
                    the tools.
    -U              Build without requiring root privileges,
                    install from an UNPRIVED build with proper
                    file permissions.
    -h              Show this message.
EOF
    exit 0
}

ROOT="/zpool"
SRC="$ROOT/src"
XSRC="$ROOT/xsrc"
OBJ="$ROOT/obj"
TOOLS="$ROOT/tools"
RELEASE="$ROOT/releasedir"
CMD="./build.sh \
     -O $OBJ \
     -R $RELEASE \
     -T $TOOLS \
     -V MKDEBUG=yes \
     -V MKDEBUGLIB=yes \
     -V MKLINT=yes \
     -X $XSRC \
     -x \
     -j3"
HG="/usr/pkg/bin/hg"
SUDO="/usr/pkg/bin/sudo"

# Parse arguments

while getopts ruUha:m: OPT; do
    case $OPT in
    "a") MACHINE_ARCH="$OPTARG" ;;
    "m") MACHINE="$OPTARG" ;;
    "r") CMD="$CMD -r" ;;
    "u") CMD="$CMD -u" ;;
    "U") CMD="$CMD -U" ;;
    "h") _usage ;;
    *) _usage ;;
    esac
done

MACHINE=${MACHINE:=$(uname -m)}
MACHINE_ARCH=${MACHINE_ARCH:=$(uname -p)}
DEST="$ROOT/destdir/$MACHINE"

CMD="$CMD -a $MACHINE_ARCH -m $MACHINE -D $DEST"

# Initial check

for dir in $ROOT $SRC $XSRC $OBJ $TOOLS $RELEASE $DEST; do
    test -d "$dir" || _bomb "$dir: not found"
done

for command in $SUDO $HG; do
    test -f "$command" || _bomb "$command: command not found"
done

# Main

cd "$XSRC" \
    && $SUDO $HG pull \
    && $SUDO $HG update

cd "$SRC" \
    && $SUDO $HG pull \
    && $SUDO $HG update \
    && $SUDO $CMD tools \
    && $SUDO $CMD kernel=GENERIC \
    && $SUDO $CMD distribution

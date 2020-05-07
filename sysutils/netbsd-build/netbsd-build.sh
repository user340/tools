#!/bin/sh
# Copyright (c) 2020 Yuuki Enomoto
# Copyright (c) 2001-2011 The NetBSD Foundation, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE NETBSD FOUNDATION, INC. AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

_bomb()
{
    echo "$@"
    exit 1
}

_usage()
{
    cat << EOF
$0 [ruU]

 Options
    -r              Remove contents of TOOLDIR and DESTDIR before 
                    building.
    -u              *Do not* run "make cleandir" first.
                    Without this, everything is rebuilt, including
                    the tools.
    -U              Build without requiring root privileges,
                    install from an UNPRIVED build with proper
                    file permissions.
EOF
    exit 1
}

SRC="$HOME/src/cvs.NetBSD.org/src"
XSRC="$HOME/src/cvs.NetBSD.org/xsrc"

ROOT="/zshare/netbsd-build"
OBJ="$ROOT/obj"
TOOLS="$ROOT/tools"
RELEASE="$ROOT/releasedir"
DESTDIR="$ROOT/destdir"
BUILD_CMD="./build.sh"
CMD_OPT="-a x86_64 \
         -m amd64 \
         -D $DESTDIR \
         -O $OBJ \
         -R $RELEASE \
         -T $TOOLS \
         -X $XSRC \
         -x \
         -j8"
PRIV="/usr/local/bin/doas"
VCS="/usr/pkg/bin/cvs"
UPDATE_CMD="$VCS update"

for cmd in $PRIV $VCS; do
    test -x "$cmd" || _bomb "$cmd: command not found or not executable"
done

for directory in $ROOT $OBJ $TOOLS $RELEASE $DESTDIR $SRC $XSRC; do
    test -d "$directory" || _bomb "$directory: no such directory"
done

# Parse arguments

while getopts ruU OPT; do
    case $OPT in
    "r") CMD_OPT="$CMD_OPT -r" ;;
    "u") CMD_OPT="$CMD_OPT -u" ;;
    "U") CMD_OPT="$CMD_OPT -U" ;;
    *) _usage ;;
    esac
done

# Main

cd "$XSRC" && $UPDATE_CMD

cd "$SRC" \
    && $UPDATE_CMD \
    && $PRIV "$BUILD_CMD" $CMD_OPT tools \
    && $PRIV "$BUILD_CMD" $CMD_OPT kernel=GENERIC \
    && $PRIV "$BUILD_CMD" $CMD_OPT distribution \
    && $PRIV "$BUILD_CMD" $CMD_OPT sets \
    && $PRIV "$BUILD_CMD" $CMD_OPT releasekernel=GENERIC \
    && $PRIV "$BUILD_CMD" $CMD_OPT syspkgs

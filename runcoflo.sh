#! /bin/sh

# Create a subdirectory in the root of the make-3.82 source tree and run this script from it.

TOP_SRCDIR=".";

prefix=/home/dgy/Programming/VInterval
datadir=/home/dgy/Programming/VInterval
localedir=${datadir}
libdir=${prefix}

DEFAULT_INCLUDES="-I. -I${TOP_SRCDIR}"
DEFS="-DLOCALEDIR='\"'${localedir}'\"' -DLIBDIR=\"${libdir}\" -DINCLUDEDIR=\"${includedir}\" -DHAVE_CONFIG_H"

# Run CoFlo.
coflo ${DEFS} ${DEFAULT_INCLUDES} ${INCLUDES} ${TOP_SRCDIR}/main.c -O cfg_out/

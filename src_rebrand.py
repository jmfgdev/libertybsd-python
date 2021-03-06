#!/usr/bin/env python3

"""
Name: src_rebrand.py
Main: JimmyBot(jmfgdev)
Lisc: GPLV3
Desc: Rebranding OBSD base
      sources for use in
      LBSD.
"""

# Usage: src_rebrand.sh $SRC_DIR

. ./libdeblob.sh

PATCH_DIR=/tmp/src_rebrand


if [ -e $PATCH_DIR ]
then
	self_destruct_sequence $PATCH_DIR
else
	mkdir $PATCH_DIR
fi

if test -z $1
then
	SRC_DIR=/usr/src
else
	SRC_DIR=$1
fi


arch_list="amd64 i386"

rep "export OBSD=\"OpenBSD/\$ARCH \$VNAME\"" "export OBSD=\"LibertyBSD/\$ARCH \$VNAME\"" distrib/miniroot/dot.profile

#iso_list="alpha amd64 hppa i386 sgi sparc sparc64 vax"
iso_list="amd64 i386"
for arch in $(echo $iso_list)
do
	rep "OpenBSD \${OSREV} ${arch} Install CD" "LibertyBSD \${OSREV} ${arch} Install CD" distrib/$arch/iso/Makefile
	rep "Copyright (c) `date +%Y` Theo de Raadt, The OpenBSD project" "Copyright (c) `date +%Y` The *OpenBSD* and LibertyBSD projects" distrib/$arch/iso/Makefile
	rep "Theo de Raadt <deraadt@openbsd.org>" "Riley Baird <riley@openmailbox.org>" distrib/$arch/iso/Makefile
	rep "OpenBSD/\${MACHINE}   \${OSREV} Install CD" "LibertyBSD/\${MACHINE} \${OSREV} Install CD" distrib/$arch/iso/Makefile
done

#cdfs_list="alpha amd64 i386 loongson sgi sparc sparc64 vax"
cdfs_list="amd64 i386"
for arch in $(echo $cdfs_list)
do
	rep "OpenBSD \${OSREV} ${arch} bootonly CD" "LibertyBSD \${OSREV} ${arch} bootonly CD" distrib/$arch/cdfs/Makefile
	rep "Copyright (c) `date +%Y` Theo de Raadt, The OpenBSD project" "Copyright (c) `date +%Y` The *OpenBSD* and LibertyBSD projects" distrib/$arch/cdfs/Makefile
	rep "Theo de Raadt <deraadt@openbsd.org>" "Riley Baird <riley@openmailbox.org>" distrib/$arch/cdfs/Makefile
	rep "OpenBSD/${arch}   \${OSREV} boot-only CD" "LibertyBSD/${arch} \${OSREV} boot CD" distrib/$arch/cdfs/Makefile
done

# Distrib changes for all archs
for arch in $(echo $arch_list)
do
	rep "${arch}-openbsd" "${arch}-libertybsd" distrib/sets/lists/base/md.$arch
	rep "You will not be able to boot OpenBSD from \${1}." "You will not be able to boot LibertyBSD from \${1}." distrib/$arch/common/install.md
done

dir_list="lib/libiberty lib/libobjc lib/libstdc++ share usr.bin/binutils usr.bin/binutils-2.17 usr.bin/gcc usr.bin/texinfo ../usr.sbin/bind ../usr.sbin/unbound"
for dir in $dir_list
do
	rep "UNAME_SYSTEM=\`(uname -s) 2>/dev/null\`" "UNAME_SYSTEM=\`(echo OpenBSD) 2>/dev/null\`" gnu/${dir}/config.guess
done

dircp files/uname-obsd usr.bin/uname-obsd
lineadd "./usr/bin/uname" "./usr/bin/uname-obsd" distrib/sets/lists/base/mi
rep "uname " "uname" distrib/sets/lists/base/mi
rep "uname-obsd " "uname-obsd" distrib/sets/lists/base/mi
rep "uname" "uname uname-obsd" usr.bin/Makefile
lineadd "uname.1" "./usr/share/man/man1/uname-obsd.1" distrib/sets/lists/man/mi

lineadd "openbsd) osname=openbsd" "$(space 15) libertybsd) osname=libertybsd" gnu/usr.bin/perl/Configure
lineadd "openbsd) osname=openbsd" "$(space 23) ;;" gnu/usr.bin/perl/Configure
lineadd "openbsd) osname=openbsd" "$(space 23) osvers=\"\$3\"" gnu/usr.bin/perl/Configure
rep "osname=openbsd" "osname=libertybsd" gnu/usr.bin/perl/Configure
rep "interix|dragonfly|bitrig" "libertybsd|interix|dragonfly|bitrig" gnu/usr.bin/perl/Configure
rep "dragonfly\*|bitrig*" "libertybsd\*|dragonfly\*|bitrig\*" gnu/usr.bin/perl/Makefile.SH
rep "-openbsd" "-libertybsd" gnu/usr.bin/perl/Makefile.bsd-wrapper
filecp gnu/usr.bin/perl/hints/openbsd.sh gnu/usr.bin/perl/hints/libertybsd.sh


rep "#define DMESG_START \"OpenBSD \"" "#define DMESG_START \"LibertyBSD \"" usr.bin/sendbug/sendbug.c
rep "bugs@openbsd.org" "bugs@libertybsd.net" usr.bin/sendbug/sendbug.c

# Adding LBSD keys
filecp files/keys/libertybsd-61-base.pub etc/signify/libertybsd-61-base.pub
filecp files/keys/libertybsd-61-pkg.pub etc/signify/libertybsd-61-pkg.pub
filecp files/keys/libertybsd-61-syspatch.pub etc/signify/libertybsd-61-syspatch.pub
filecp files/keys/libertybsd-62-base.pub etc/signify/libertybsd-62-base.pub
filecp files/keys/libertybsd-62-pkg.pub etc/signify/libertybsd-62-pkg.pub
filecp files/keys/libertybsd-62-syspatch.pub etc/signify/libertybsd-62-syspatch.pub

rep "openbsd-" "libertybsd-" distrib/sets/lists/base/mi
rep "-59-base.pub" "-59.pub" distrib/sets/lists/base/mi
linedel "./etc/signify/openbsd-59-pkg.pub" distrib/sets/lists/base/mi
linedel "./etc/signify/openbsd-60-base.pub" distrib/sets/lists/base/mi
linedel "./etc/signify/openbsd-60-fw.pub" distrib/sets/lists/base/mi
linedel "./etc/signify/openbsd-60-pkg.pub" distrib/sets/lists/base/mi

filecp files/motd etc/motd
filecp files/root.mail etc/root/root.mail 
filecp files/install.sub distrib/miniroot/install.sub

rep "openbsd-" "libertybsd-" usr.sbin/syspatch/syspatch.sh
rep "OpenBSD" "LibertyBSD" usr.sbin/syspatch/syspatch.sh

apply

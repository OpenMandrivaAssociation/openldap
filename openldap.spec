%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define pkg_name	openldap
%define version	2.4.32
%define rel 1
%global	beta %{nil}

%{?!mklibname:%{error:You are missing macros, build will fail, see http://wiki.mandriva.com/en/Projects/BackPorts#Building_Mandriva_SRPMS_on_other_distributions}}

%{?!distsuffix:%define distsuffix mdk}
%{?!distversion:%define distversion %(echo $[%{mdkversion}/10])}
%{?!mkrel:%define mkrel(c:) %{-c:0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{distversion}%{?_with_unstable:%{1}}%{distsuffix}}}

%define release %mkrel %rel

#defaults
%define build_system 0
%define build_alternatives 0
%define build_modules 1
%define build_modpacks 0
%define build_slp 0
%define build_heimdal 0
%define build_nssov 1
%define build_smbk5pwd 1
%define build_asmmutex 0
%global build_migration 0

%{?mgaversion:%global mdkversion 201100}
%if %{?mdkversion:0}%{?!mdkversion:1}
# OK, we're not on a Mandriva box ... set this to the lowest we support
# and define a new macro we can use to know we're not in Mandriva
%define mdkversion 1000
%global notmdk 1
%endif

%if %mdkversion >= 200810
%define build_system 1
%else
%global build_migration 1
%define _with_migration 1
%endif

%{?_with_system: %global build_system 1}
%{?_without_system: %global build_system 0}
%{?_with_modules: %global build_modules 1}
%{?_without_modules: %global build_modules 0}
%{?_with_slp: %global build_slp 1}
%{?_without_slp: %global build_slp 0}
%{?_with_heimdal: %global build_heimdal 1}
%{?_without_heimdal: %global build_heimdal 0}
%{?_with_nssov: %global build_nssov 1}
%{?_without_nssov: %global build_nssov 0}
%{?_with_smbk5pwd: %global build_smbk5pwd 1}
%{?_without_smbk5pwd: %global build_smbk5pwd 0}
%{?_with_asmmutex: %global build_asmmutex 1}
%{?_without_asmmutex: %global build_asmmutex 0}

%define major 		2.4_2
%define fname ldap
%define libname %mklibname %fname %major
%define migtools_ver 	45

# we want to use the default db version for each release, so as
# to make backport binary compatibles
# excepted for very old systems, where we use bundled db
%define dbutils db4-utils
%define dbutilsprefix db_
%define bundled_db_source_ver 4.8.30
%define dbdevel db-devel
%if %mdkversion > 201020
    %global db_internal 0
    %define dbver 5.1.25
    %define dbutils db-utils
    %define dbutilsprefix db51_
%endif

%if %mdkversion <= 201020
    %global db_internal 0
    %define dbver 4.8.26
%endif

%if %mdkversion <= 201000
    %global db_internal 0
    %define dbver 4.7.25
%endif

%if %mdkversion == 200900
    %global db_internal 0
    %define dbver 4.6.21
%endif

%if %mdkversion == 200810
    %global db_internal 0
    %define dbver 4.6.21
%endif

%if %mdkversion <= 200800
    %global db_internal 1
%endif

%if %{?mgaversion:1}%{?!mgaversion:0}
%if %mgaversion > 1
	%define dbutils db51-utils
        %define dbver 5.1.25
	%define dbutilsprefix db51_
        %define dbdevel db5-devel
%else
	%define dbutils db51-utils
        %define dbver 5.1.19
	%define dbutilsprefix db51_
%endif
%endif # mgaversion

%define dbname %(a=%dbver;echo ${a%.*})
%{?_with_dbinternal: %global db_internal 1}
%{?_without_dbinternal: %global db_internal 0}
%if %db_internal
%define dbver %bundled_db_source_ver
%endif

%if %mdkversion < 200910
    %global __libtoolize /bin/true
%endif

%define ol_ver_major 2.4
%if %build_system
%define ol_major %{nil}
%define ol_suffix %nil
%else
%define ol_major 2.4
%define ol_suffix 24
%endif

%if %build_alternatives || !%build_system
%define alternative_major 2.4
%else
%define alternatives_major %{nil}
%endif

%global clientbin	ldapadd,ldapcompare,ldapdelete,ldapmodify,ldapmodrdn,ldappasswd,ldapsearch,ldapwhoami,ldapexop
%if %db_internal
%global serverbin	slapd_db_archive,slapd_db_checkpoint,slapd_db_deadlock,slapd_db_dump,slapd_db_load,slapd_db_printlog,slapd_db_recover,slapd_db_stat,slapd_db_upgrade,slapd_db_verify,slapd-addel,slapd-bind,slapd-modify,slapd-modrdn,slapd-read,slapd-search,slapd-tester,ldif-filter
%else
%global serverbin	slapd-addel,slapd-bind,slapd-modify,slapd-modrdn,slapd-read,slapd-search,slapd-tester,ldif-filter
%endif
%define serversbin	slapadd,slapcat,slapd,slapdn,slapindex,slappasswd,slaptest,slurpd,slapacl,slapauth

#localstatedir is passed directly to configure, and we want it to be /var/lib
#define _localstatedir %{_var}/run
%define	_libexecdir	%{_sbindir}

# Allow --with[out] SASL at rpm command line build
%{?_without_SASL: %{expand: %%define _without_cyrussasl --without-cyrus-sasl}}
%{?_with_SASL: %{expand: %%define _with_cyrussasl --with-cyrus-sasl}}
%{!?_with_cyrussasl: %{!?_without_cyrussasl: %global _with_cyrussasl --with-cyrus-sasl}}
%{?_with_cyrussasl: %define _with_cyrussasl --with-cyrus-sasl}
%{?_without_cyrussasl: %define _without_cyrussasl --without-cyrus-sasl}
%{?_with_gdbm: %global db_conv dbb}
%{!?_with_gdbm: %global db_conv gdbm}
%global build_sql 1
%{?_without_sql: %global build_sql 0}
%global back_perl 0

Summary: 	LDAP servers and sample clients
Name: 		%{pkg_name}%{ol_major}
Version: 	%{version}
Release: 	%{release}
License: 	Artistic
Group: 		System/Servers
URL: 		http://www.openldap.org

# Openldap source
Source0: 	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{pkg_name}-%{version}%{beta}.tgz

## To generate ths tarball, check the docs out of CVS:
# cvs -d :pserver:anonymous@cvs.OpenLDAP.org:/repo/OpenLDAP co \
# -r OPENLDAP_REL_ENG_2_4 guide
## patch the docs:
# cd guide/admin
# patch -p0 < `rpm --eval %_sourcedir`/openldap-2.4-admin-guide-add-vendor-doc.patch
# cp -p `rpm --eval %_sourcedir`/vendor*.sdf .
## build the docs
# make guide.html
## tar them up
# mkdir openldap-guide
# cp *.html *.gif *.png ../images/LDAPlogo.gif openldap-guide
# tar cjvf `rpm --eval %_sourcedir`/openldap-guide-2.4.tar.bz2 openldap-guide
## To update the README-openldap2.4.mdv as well:
# sdf -2txt_ vendor-standalone.sdf
# cp vendor-standalone.txt `rpm --eval %_sourcedir`/README-openldap2.4.mdv
## ensure your changes get back into the package:
# cvs diff | bzip2 -c > \
# `rpm --eval %_sourcedir`/openldap-2.4-admin-guide-add-vendor-doc.patch.bz2
# tar cjvf `rpm --eval %_sourcedir`/openldap-2.4-vendor-docs.tar.bz2 vendor*.sdf

Source12:	openldap-guide-2.4.tar.bz2
Source13:	README-openldap2.4.mdv

# Specific source
Source1: 	ldap.init
Source2: 	%{pkg_name}.sysconfig
Source19:	gencert.sh
Source20:	ldap.logrotate
Source21:	slapd.conf
Source22:	DB_CONFIG
Source23:	ldap.conf
Source24:	slapd.access.conf
Source25:	ldap-hot-db-backup
Source26:	ldap-reinitialise-slave
Source27:	ldap-common

# Migration tools
Source11:	http://www.padl.com/download/MigrationTools-%{migtools_ver}.tar.bz2
Source3: 	migration-tools.txt
Source4: 	migrate_automount.pl

Source30:	http://www.sleepycat.com/update/snapshot/db-%{bundled_db_source_ver}.tar.gz

# Extended Schema 
Source54: 	mull.schema

# Doc sources, used to build SOURCE12 and SOURCE13 above
Source100:	openldap-2.4-admin-guide-add-vendor-doc.patch
Source101:	vendor.sdf
Source102:	vendor-standalone.sdf

# Chris Patches
Patch0: 	%{pkg_name}-2.3.4-config.patch
Patch1:		%{pkg_name}-2.0.7-module.patch

#Fix various paths in smbk5pwd:
Patch2:		openldap-2.3-smbk5passwd-paths.patch
# For now, only build support for SMB (no krb5) changing support in smbk5passwd
# overlay:
Patch3:		openldap-2.3.4-smbk5passwd-only-smb.patch
Patch4:		openldap-2.4.25-contrib-makefiles-with-tests.patch
Patch5:     openldap-2.4.8-fix-lib-perms.patch
Patch6:		openldap-2.4.12-test001-check-slapcat.patch

# RH + PLD Patches
Patch15:	%{pkg_name}-cldap.patch

# Migration tools Patch
Patch40: 	MigrationTools-34-instdir.patch
Patch41: 	MigrationTools-36-mktemp.patch
Patch42: 	MigrationTools-27-simple.patch
Patch43: 	MigrationTools-26-suffix.patch
Patch45:	MigrationTools-45-i18n.patch
# schema patch
Patch46: 	openldap-2.0.21-schema.patch
Patch47: 	openldap-2.4.12-change-dyngroup-schema.patch
# http://qa.mandriva.com/show_bug.cgi?id=15499
Patch48:	MigrationTools-45-structural.patch

Patch200:	db-4.7.25-fix-format-errors.patch
# Upstream bdb patches

# http://www.oracle.com/technology/software/products/berkeley-db/db/
%if %db_internal
# used by s_config, which is required by above patch:
BuildRequires:	ed autoconf%{?notmdk: >= 2.5}
%else
# txn_nolog added in 4.2.52-6mdk
BuildRequires: 	%dbdevel >= %{dbver}
%endif

Patch53: %pkg_name-ntlm.patch
# preserves the temp file used to import data if an error occured
Patch54: MigrationTools-40-preserveldif.patch

#patches in CVS
# see http://www.stanford.edu/services/directory/openldap/configuration/openldap-build.html
# for other possibly interesting patches

%{?_with_cyrussasl:BuildRequires: 	%{?!notmdk:libsasl-devel}%{?notmdk:cyrus-sasl-devel}}
%{?_with_kerberos:BuildRequires:	krb5-devel}
BuildRequires:	openssl-devel, perl
%if %build_slp
BuildRequires: openslp-devel
%endif
%if %build_heimdal
BuildRequires: heimdal-devel
%endif
%if %build_sql
BuildRequires: 	unixODBC-devel
%endif
%if %back_perl
BuildRequires:	perl-devel
%endif
BuildRequires:  ncurses-devel >= 5.0
BuildRequires: tcp_wrappers%{?!notmdk:-devel} libtool%{?!notmdk:-devel}
BuildRequires:  krb5-devel
BuildRequires:	groff
# for make test:
BuildRequires:	diffutils
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Requires:	shadow-utils, setup >= 2.2.0-6mdk

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The suite includes a
stand-alone LDAP server (slapd) which is in the -servers package, libraries for
implementing the LDAP protocol (in the lib packages), and utilities, tools, and
sample clients (in the -clients package). The openldap binary package includes
only configuration files used by the libraries.

Install openldap if you need LDAP applications and tools.

%package servers
Summary: 	OpenLDAP servers and related files
Group: 		System/Servers
%if %{?notmdk:1}%{?!notmdk:0}
Requires(pre):	/usr/sbin/useradd /usr/sbin/groupadd coreutils
%else
Requires(pre):	rpm-helper >= 0.23 coreutils
BuildRequires:	rpm-helper >= 0.23
%endif
%if !%build_modpacks
Provides:	%{name}-back_dnssrv = %{version}-%{release}
Provides:	%{name}-back_ldap = %{version}-%{release}
Provides:	%{name}-back_passwd = %{version}-%{release}
Provides:	%{name}-back_sql = %{version}-%{release}
Obsoletes:	%{name}-back_dnssrv < %{version}-%{release}
Obsoletes:	%{name}-back_ldap < %{version}-%{release}
Obsoletes:	%{name}-back_passwd < %{version}-%{release}
Obsoletes:	%{name}-back_sql < %{version}-%{release}
%endif
%if !%db_internal
Requires(pre):	%dbutils
Requires(post):	%dbutils
# slapd checks at startup if the library version matches exactly what it
# was compiled against, so we cant allow newer versions, e.g.:
#bdb_back_initialize: BDB library version mismatch: expected Berkeley DB 4.8.26: (December 30, 2009), got Berkeley DB 4.8.30: (March 25, 2011)
# This might need to be changed to a library dependency, but we need to verify
# library provides on multiple distros before doing that
Requires:	%dbutils = %dbver
%endif
%if %{?_with_cyrussasl:1}%{!?_with_cyrussasl:0}
%define saslver %([ -f "%{_includedir}/sasl/sasl.h" ] && echo -e "#include <sasl/sasl.h>\\nSASL_VERSION_MAJOR SASL_VERSION_MINOR SASL_VERSION_STEP"|cpp|awk 'END {printf "%s.%s.%s",$1,$2,$3}' || echo "2.1.22")
%define sasllib %mklibname sasl 2
#Ensure we have the sasl library we compiled against available in post so
#slapadd etc works
Requires(post):	%{?!notmdk:%sasllib}%{?notmdk:cyrus-sasl} = %saslver
%endif
Requires: 	%libname = %{version}-%{release}
Conflicts:	kolab < 1.9.5-0.20050801.4mdk
Requires: 	%{pkg_name}%{ol_major}-extra-schemas >= 1.3-7
Requires(pre): 	%{pkg_name}%{ol_major}-extra-schemas >= 1.3-7

%description servers
OpenLDAP Servers

This package contains the OpenLDAP server, slapd (LDAP server), additional 
backends, configuration files, schema definitions required for operation, and 
database maintenance tools

This server package was compiled with support for the %{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}
database library.

%package clients
Summary: 	OpenLDAP clients and related files
Group: 		System/Servers
Requires: 	%libname = %{version}-%{release}

%description clients
OpenLDAP clients

This package contains command-line ldap clients (ldapsearch, ldapadd etc)

%if %build_migration
%package migration
Summary: 	Set of scripts for migration of a nis domain to a ldap directory
Group: 		System/Configuration/Other
Requires: 	%{name}-servers = %{version}
Requires: 	%{name}-clients = %{version}

%description migration
This package contains a set of scripts for migrating data from local files
(ie /etc/passwd) or a nis domain to an ldap directory.
%endif

%package -n %libname
Summary: 	OpenLDAP libraries
Group: 		System/Libraries
Provides:       lib%fname = %version-%release
# This is needed so all libldap2 applications get /etc/openldap/ldap.conf
# which was moved from openldap-clients to openldap in 2.1.25-4mdk
Requires:	%{name} >= 2.1.25-4mdk

%description -n %libname
This package includes the libraries needed by ldap applications.


%package -n %libname-devel
Summary: 	OpenLDAP development libraries and header files
Group: 		Development/C
Requires: 	%libname = %{version}-%release
Requires: 	tcp_wrappers%{?!notmdk:-devel}
Provides:       %{name}-devel = %{version}-%{release}
%if %build_system
Provides: 	lib%fname-devel = %version-%release
Provides:	openldap2-devel = %{version}-%{release}
Obsoletes: 	openldap-devel
%endif
Conflicts:	libldap1-devel
Conflicts:	%mklibname -d ldap 2
Conflicts:	%mklibname -d ldap 2.3_0

%description -n %libname-devel
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
LDAP clients.


%package -n %{libname}-static-devel
Summary: 	OpenLDAP development static libraries
Group: 		Development/C
Requires: 	%libname-devel = %{version}-%release
%if %build_system
Provides: 	lib%fname-devel-static = %version-%release
Provides: 	lib%fname-static-devel = %version-%release
Provides:	openldap-devel-static = %{version}-%{release}
Provides:	openldap-static-devel = %{version}-%{release}
Obsoletes: 	openldap-devel-static
%endif
Conflicts:	libldap1-devel


%description -n %libname-static-devel
OpenLDAP development static libraries

%if %build_modpacks
%package back_dnssrv
Summary: 	Module dnssrv for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_dnssrv
The dnssrv daabase backend module for OpenLDAP daemon

%package back_ldap
Summary: 	Module ldap for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_ldap
The ldap database backend module for OpenLDAP daemon


%package back_passwd
Summary: 	Module passwd for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%release
Requires: 	openldap-servers = %{version}-%release

%description back_passwd
The passwd database backend module for OpenLDAP daemon
%endif
%if %build_sql && %build_modpacks
%package back_sql
Summary: 	Module sql for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_sql
The sql database backend module for OpenLDAP daemon
%endif

%package doc
Summary: 	OpenLDAP documentation and administration guide
Group: 		Books/Computer books
Requires: 	openldap
Provides:	openldap-guide
Obsoletes:	openldap-guide

%description doc
OpenLDAP documentation, incuding RFCs and the adminitration guide

%package tests
Summary:	OpenLDAP Test Suite - tests and data
Group:		Development/Other
Requires:	%{name}-servers %{name}-clients %{name}-testprogs

%description tests
OpenLDAP now has a substantial test suite, which includes sample configurations
and data for a large number of scenarios and features. These are useful for
testing the installed server, and seeing examples of how to use the features.

The intention is that it should be possible to run the entire test suite on
the installed server using this package.


%package testprogs
Summary:	OpenLDAP Test Suite - simple testing client binaries
Group:		Development/Other

%description testprogs
Programs shipped with the test suite which are used by the test suite, and may
also be useful as load generators etc.

%prep
%if %db_internal
%setup -q -n %{pkg_name}-%{version}%{beta} %{?_with_migration:-a 11} -a 30 
pushd db-%{dbver} >/dev/null

%patch200 -p1
# upstream bdb patches

#(cd dist && ./s_config)
#%endif
popd >/dev/null
%else
%setup -q  -n %{pkg_name}-%{version}%{beta} %{?_with_migration:-a 11}
%endif

%patch0 -p1 -b .config
perl -pi -e 's/^(#define\s+DEFAULT_SLURPD_REPLICA_DIR.*)ldap(.*)/${1}ldap%{ol_major}${2}/' servers/slurpd/slurp.h
perl -pi -e 's/LDAP_DIRSEP "run" //g' include/ldap_defaults.h
%patch1 -p1 -b .module
%patch2 -p1 -b .smbk5paths
%if !%build_heimdal
%patch3 -p1 -b .smbonly
%endif
%patch4 -p1 -b .contribmake

%patch15 -p1 -b .cldap 


%if %build_migration
pushd MigrationTools-%{migtools_ver}
%patch40 -p1 -b .instdir
%patch41 -p1 -b .mktemp
%patch42 -p1 -b .simple
%patch43 -p1 -b .suffix
%patch45 -p2 -b .i18n
%patch48 -p2 -b .account
%patch54 -p1 -b .preserve
popd
%endif

%patch46 -p1 -b .mdk
%patch47 -p1 -b .dyngroup
#bgmilne %patch47 -p1 -b .maildropschema
# FIXME
%patch53 -p1 -b .ntlm

# patches from CVS
perl -pi -e 's/testrun/\${TESTDIR}/g' tests/scripts/test024-unique

# README:
cp %{SOURCE13} README.mdk

# test049 not ready for not writing to testdir ...
mv tests/scripts/{,broken}test049*

%patch5 -p1
%patch6 -p1
chmod a+rx tests/scripts/test054*
#aclocal
#perl -pi -e 's/^(AC_PREREQ.2.5)/${1}7/g' configure.in
#autoconf

%build
#disable icecream:
PATH=`echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g'`
%serverbuild

# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=`echo $CFLAGS|sed -e 's|-fPIE||g'`
CXXFLAGS=`echo $CXXFLAGS|sed -e 's|-fPIE||g'`

%if %db_internal
dbdir=`pwd`/db-instroot
pushd db-%{dbver}/build_unix
CONFIGURE_TOP="../dist" %configure2_5x \
        --enable-shared --disable-static \
        --with-uniquename=_openldap_slapd%{ol_suffix}_mdv \
	--program-prefix=slapd%{ol_major}_ \
%if %{build_asmmutex}
%ifarch %{ix86}
	--disable-posixmutexes --with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
	--disable-posixmutexes --with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
	--disable-posixmutexes --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
	--disable-posixmutexes --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
	--disable-posixmutexes --with-mutex=PPC/gcc-assembly
%endif
%ifarch sparc
	--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif
%else
	--with-mutex=POSIX/pthreads/library
%endif

#--with-mutex=POSIX/pthreads/library
#JMD: use --disable-posixmutexes so it works on a non-NPTL kernel, and use
#assembler mutexes since they're *way* faster and correctly implemented.

perl -pi -e 's/^(libdb_base=\s+)\w+/\1libslapd%{ol_suffix}_db/g' Makefile
#Fix soname and libname in libtool:
#perl -pi -e 's/shared_ext/shrext/g' libtool
make
rm -Rf $dbdir
mkdir -p $dbdir
make DESTDIR=$dbdir install
ln -sf ${dbdir}/%{_libdir}/libslapd%{ol_suffix}_db-%{dbname}.so ${dbdir}/%{_libdir}/libdb-%{dbname}.so
chmod u+w ${dbdir}/usr/include/db.h
grep __lock_ db_int_def.h >> ${dbdir}/usr/include/db.h
popd
export CPPFLAGS="-I${dbdir}/%{_includedir} $CPPFLAGS"
export LDFLAGS="-L${dbdir}/%{_libdir} $LDFLAGS"
export LD_LIBRARY_PATH="${dbdir}/%{_libdir}"
%endif

unset CONFIGURE_TOP

#FIXME: Some script backends should not be used with threads, mostly shell/perl

%if !%build_system
perl -pi -e 's,(progname = "\w+)",${1}%{ol_major}",g' servers/slapd/*.c
perl -pi -e 's,({"slap\w+)",${1}%{ol_major}",g' servers/slapd/main.c
%endif

# don't choose db4.3 even if it is available
export ol_cv_db_db_4_dot_3=no
# try and miss linuxthreads, so we get a threading lib on glibc2.4:
%if %mdkversion > 200600
export ol_cv_header_linux_threads=no
%endif
#rh only:
export CPPFLAGS="-I%{_prefix}/kerberos/include $CPPFLAGS"
export LDFLAGS="-L%{_prefix}/kerberos/%{_lib} $LDFLAGS"
%if %{?openldap_fd_setsize:1}%{!?openldap_fd_setsize:0}
CPPFLAGS="$CPPFLAGS -DOPENLDAP_FD_SETSIZE=%{openldap_fd_setsize}"
%endif
# FIXME glibc 2.8 breakage, this is not the correct fix, see
# http://www.openldap.org/its/index.cgi/Build?id=5464;selectid=5464
CPPFLAGS="$CPPFLAGS -D_GNU_SOURCE"
# building for systems with kernel < 2.6 requires building without epoll support
%if %{mdkversion} < 1000 || %{?_without_epoll:1}%{!?_without_epoll:0}
export ac_cv_header_sys_epoll_h=no
%endif

%configure2_5x \
	--with-subdir=%{name} \
%if !%build_system
	--program-suffix=%{ol_major} \
%endif
	--localstatedir=/var/run/ldap%{ol_major} \
	--enable-dynamic \
	--enable-syslog \
	--enable-proctitle \
	--enable-ipv6 \
	--enable-local \
	%{?_with_cyrussasl} %{?_without_cyrussasl} \
	%{?_with_kerberos} %{?_without_kerberos} \
	--with-threads \
	--with-tls \
	--enable-slapd \
	--enable-aci \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
	%{!?_with_gssapi:--without-gssapi} \
	%{?_with_kerberos:--enable-kpasswd} \
	%{?_with_cyrussasl:--enable-spasswd} \
%if %build_modules
	--enable-modules \
%endif
	--enable-rewrite \
	--enable-rlookups \
%if %build_slp
	--enable-slp \
%endif
	--enable-wrappers \
	--enable-bdb=yes \
	--enable-hdb=yes \
	--enable-ndb=no \
	--enable-backends=mod \
%if %back_perl
	--enable-perl=mod \
%else
	--enable-perl=no \
%endif
%if %build_sql
	--enable-sql=mod \
%else
	--enable-sql=no \
%endif
	--enable-overlays=mod \
	--enable-shared

%if !%build_system
perl -pi -e 's/^(ldap_subdir\s+=\s+.*)%{pkg_name}/$1%{name}/g' Makefile
perl -p -i.bak -e 's/slapd-(search|read|addel|modrdn|modify|bind)/slapd-${1}%{ol_major}/g' tests/progs/slapd-tester.c
%endif

# (oe) amd64 fix
perl -pi -e "s|^AC_CFLAGS.*|AC_CFLAGS = $CFLAGS -fPIC|g" libraries/librewrite/Makefile

make depend 

make 
export LIBTOOL=`pwd`/libtool

if [ -d /usr/kerberos/%{_lib} ]; then export LIBRARY_PATH=/usr/kerberos/%{_lib}; fi
perl -pi -e 's/radius.la//g' contrib/slapd-modules/passwd/Makefile
#acl broken
for i in addpartial allop allowed autogroup cloak denyop dsaschema dupent  \
%if %mdkversion >= 201010
    kinit \
%endif
    lastbind lastmod noopsrch nops \
%if %build_nssov
    nssov \
%endif
%if %build_smbk5pwd
    smbk5pwd \
%endif
    passwd passwd/sha2 trace
do
    make -C contrib/slapd-modules/$i libdir=%{_libdir} moduledir=%{_libdir}/%{name}
done

#proxyOld, needs some work ...
#CC=g++ make -C contrib/slapd-modules/proxyOld

#samba4, not useful yet?

# http://wiki.mandriva.com/en/2009-underlinking-overlinking
#LDFLAGS=${LDFLAGS//-Wl,--no-undefined/}
# Not shipped yet: comp_match,proxyOld


%check
%if %{!?_without_test:1}%{?_without_test:0}
%if !%{build_system}
pushd clients/tools
for OLD in {%{clientbin}}
do
    NEW=`echo ${OLD}%{alternative_major}`
    ln -sf $OLD $NEW
    #mv -f $OLD $NEW ||:
    #if [ -L $NEW ]
    #then ln -sf `readlink $NEW`%{alternative_major} $NEW
    #fi
done
popd
%endif
#disable icecream:
#PATH=`echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g'`
%if %db_internal
dbdir=`pwd`/db-instroot
export LD_LIBRARY_PATH="${dbdir}/%{_libdir}"
%endif
# meta test seems to timeout on the Mandriva cluster:
#export TEST_META=no
# Use a pseudo-random number between 9000 and 10000 as base port for slapd in tests
export SLAPD_BASEPORT=$[9000+RANDOM%1000]
make -C tests %{!?tests:test}%{?tests:%tests}
%endif

%install
#disable icecream:
#PATH=`echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g'`
export DONT_GPRINTIFY=1
export DONT_REMOVE_LIBTOOL_FILES=1
for i in acl addpartial allop allowed autogroup \
%if %mdkversion >= 201010
 kinit \
%endif
%if %build_nssov
    nssov \
%endif
%if %build_smbk5pwd
    smbk5pwd \
%endif
    passwd 
do
cp -af contrib/slapd-modules/$i/README{,.$i}
done
cp contrib/slapd-modules/passwd/sha2/README{,.sha2}
rm -Rf %{buildroot}

%if %db_internal
pushd db-%{dbver}/build_unix
%makeinstall_std STRIP="/bin/true"
for i in %{buildroot}/%{_bindir}/db_*;do mv $i ${i/db_/slapd_db_};done
popd
# For contrib tests
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
%endif

%makeinstall_std STRIP="" 

%if %build_smbk5pwd
cp -a contrib/slapd-modules/smbk5pwd/.libs/smbk5pwd.so* %{buildroot}/%{_libdir}/%{name}
%if !%{build_heimdal}
for i in %{buildroot}/%{_libdir}/%{name}/smbk5pwd*
do 
  if [ -L ${i} ]
  then
    newlink=`readlink $i|sed -e 's/k5//g'`
    rm $i
    ln -svf $newlink ${i/k5/}
  else
    mv $i ${i/k5/}
  fi
done
%endif
%endif

cp contrib/slapd-modules/allop/slapo-allop.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/cloak/slapo-cloak.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/lastbind/slapo-lastbind.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/lastmod/slapo-lastmod.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/nops/slapo-nops.5 %{buildroot}/%{_mandir}/man5

#cp contrib/slapd-modules/*/*.so %{buildroot}/%{_libdir}/%{name}

#smbk5pwd skipped, installed as smbpwd above
#dsaschema broken on 32bit
for i in addpartial allop allowed autogroup cloak denyop dupent \
%if %mdkversion >= 201010
    kinit \
%endif
    lastbind lastmod noopsrch nops \
%if %build_nssov
    nssov \
%endif
    passwd passwd/sha2 trace
do 
    if make -C contrib/slapd-modules/$i test
    then make DESTDIR=%{buildroot} mandir=%{_mandir} moduledir=%{_libdir}/%{name} schemadir=%{_sysconfdir}/%{name}/schema -C contrib/slapd-modules/$i install
    rm -f %{buildroot}/%{_libdir}/%{name}/$i.a
    else exit 1
    fi
done
rm -f %{buildroot}/%{_libdir}/%{name}/kerberos.a
rm -f %{buildroot}/%{_libdir}/%{name}/netscape.a
rm -f %{buildroot}/%{_libdir}/%{name}/sha2.a
#compat symlinks, DONT REMOVE
ln -s netscape.so %{buildroot}/%{_libdir}/%{name}/pw-netscape.so
ln -s kerberos.so %{buildroot}/%{_libdir}/%{name}/pw-kerberos.so
    
# We already had ldapns.schema in extra-schemas
rm -f %{buildroot}/%{_sysconfdir}/%{name}/schema/ldapns.schema


# try and ship the tests such that they will run properly

install -d %{buildroot}/%{_datadir}/%{name}/tests
cp -a tests/{data,scripts,Makefile,run} %{buildroot}/%{_datadir}/%{name}/tests
ln -s %{_datadir}/%{name}/schema %{buildroot}/%{_datadir}/%{name}/tests
find %{buildroot}/%{_datadir}/%{name}/tests -type f -name '*.conf' -exec perl -pi -e 's,\.\.\/servers\/slapd\/back-.*,%{_libdir}/%{name},g;s,\.\.\/servers\/slapd\/overlays,%{_libdir}/%{name},g' {} \;
perl -pi -e 's,(\`pwd\`\/)?\.\.\/servers\/(slapd|slurpd)\/(slapd|slurpd),%{_sbindir}/${2}%{ol_major},g;s,^PROGDIR=.*,PROGDIR=%{_bindir},g;s,^CLIENTDIR=.*,CLIENTDIR=%{_bindir},g;s,^TESTDIR=.*,TESTDIR=\${USER_TESTDIR-\$TMPDIR/openldap-testrun},g;s/ldap(search|add|delete|modify|whoami|compare|passwd|modrdn|exop)/ldap${1}%{ol_major}/g;s/slapd-tester$/slapd-tester%{ol_major}/g;s,\$TESTWD\/,,g;s/^(\.\*.*)\$(.*)/${1}\`pwd\`\/\$${2}/g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/defines.sh %{buildroot}/%{_datadir}/%{name}/tests/run
perl -pi -e 's/testrun/\$TESTDIR/g;s,^SHTOOL=.*,. scripts/defines.sh,g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/all
perl -p -i.bak -e 's,^olcModulePath: .*,olcModulePath: %{_libdir}/%{name},g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/test*
perl -pi -e 's/^(Makefile|SUBDIRS)/#$1/g' %{buildroot}/%{_datadir}/%{name}/tests/Makefile
echo 'SHTOOL="./scripts/shtool"' >> %{buildroot}/%{_datadir}/%{name}/tests/scripts/defines.sh
install -m755 build/shtool %{buildroot}/%{_datadir}/%{name}/tests/scripts
if [ -n "%{ol_major}" ]
then for i in addel bind modify modrdn read search tester
do ln -sf slapd-${i} tests/progs/slapd-${i}%{ol_major}
done
fi
ln -s %{_datadir}/%{name}/tests/data %{buildroot}/%{_datadir}/%{name}/tests/testdata

install -m755 tests/progs/.libs/slapd-* tests/progs/.libs/ldif-filter %{buildroot}/%{_bindir}

### some hack
perl -pi -e "s| -L../liblber/.libs||g" %{buildroot}%{_libdir}/libldap.la

perl -pi -e  "s,-L$RPM_BUILD_DIR\S+%{_libdir},,g" %{buildroot}/%{_libdir}/lib*.la
#sed -i -e "s|-L$RPM_BUILD_DIR/%{name}-%{version}/db-instroot/%{_libdir}||g" %{buildroot}/%{_libdir}/*la
#%{buildroot}/%{_libdir}/%{name}/*.la 

### Init scripts
install -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ldap%{ol_major}
perl -pi -e 's,%{_bindir}/db_,%{_bindir}/%{dbutilsprefix},g' %{buildroot}%{_initrddir}/ldap%{ol_major}

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/ldap%{ol_major}

install -m 640 %{SOURCE21} %{SOURCE23} %{SOURCE24} %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/%{_sysconfdir}/%{name}/slapd.d
#install -m640 -o ldap -g ldap -d /etc/openldap/slapd.d

### repository dir
install -d %{buildroot}%{_var}/lib/ldap%{ol_major}

### DB_CONFIG for bdb backend
install -m644 %{SOURCE22} %{buildroot}%{_var}/lib/ldap%{ol_major}

### run dir
install -d %{buildroot}%{_var}/run/ldap%{ol_major}

### Server defaults
echo "localhost" > %{buildroot}%{_sysconfdir}/%{name}/ldapserver

### we don't need the default files 
rm -f %{buildroot}/etc/%{name}/*.default 
rm -f %{buildroot}/etc/%{name}/schema/*.default 


### Standard schemas should not be changed by users
install -d %{buildroot}%{_datadir}/%{name}/schema
mv -f %{buildroot}%{_sysconfdir}/%{name}/schema/* %{buildroot}%{_datadir}/%{name}/schema/

### install additional schemas
install -m 644 %{SOURCE54} %{buildroot}%{_datadir}/%{name}/schema/

install -d %{buildroot}/%{_datadir}/%{name}/scripts
install -m 755 %{SOURCE25} %{SOURCE26} %{SOURCE27} %{buildroot}/%{_datadir}/%{name}/scripts/
for i in hourly daily weekly monthly yearly
do
	install -d %{buildroot}/%{_sysconfdir}/cron.${i}
	ln -s %{_datadir}/%{name}/scripts/ldap-hot-db-backup %{buildroot}/%{_sysconfdir}/cron.${i}/ldap-hot-db-backup%{ol_major}
done
perl -pi -e 's,%{_bindir}/db_,%{_bindir}/%{dbutilsprefix},g' %{buildroot}/%{_datadir}/%{name}/scripts/ldap-common

### create local.schema
echo "# This is a good place to put your schema definitions " > %{buildroot}%{_sysconfdir}/%{name}/schema/local.schema
chmod 644 %{buildroot}%{_sysconfdir}/%{name}/schema/local.schema

### deal with the migration tools
%if %build_migration
install -d %{buildroot}%{_datadir}/%{name}/migration
install -m 755 MigrationTools-%{migtools_ver}/{*.pl,*.sh,*.txt,*.ph} %{buildroot}%{_datadir}/%{name}/migration
install -m 644 MigrationTools-%{migtools_ver}/README %{SOURCE3} %{buildroot}%{_datadir}/%{name}/migration
install -m 755 %{SOURCE4} %{buildroot}%{_datadir}/%{name}/migration

cp MigrationTools-%{migtools_ver}/README README.migration
cp %{SOURCE3} TOOLS.migration
%endif

### Guide
mkdir -p %{buildroot}/%{_docdir}/
tar xvjf %{SOURCE12} -C %{buildroot}/%{_docdir}/
mv %{buildroot}/%{_docdir}/{%{pkg_name},%{name}}-guide ||:

### gencert.sh
install -m 755 %{SOURCE19} %{buildroot}/%{_datadir}/%{name}

### log repository
install -m 700 -d %{buildroot}/var/log/ldap%{ol_major}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/logrotate.d/ldap%{ol_major}


# get the buildroot out of the man pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

#mkdir -p %{buildroot}%{_sysconfdir}/ssl/%{name}

#rename binaries
%if !%{build_system} || %build_alternatives
for OLD in %{buildroot}/%{_bindir}/{%{clientbin}}
do
    NEW=`echo ${OLD}%{alternative_major}`
    mv -f $OLD $NEW ||:
    if [ -L $NEW ]
    then ln -sf `readlink $NEW`%{alternative_major} $NEW
    fi
done
for OLD in %{buildroot}/%{_mandir}/man?/{%{clientbin},ldap.conf,ldif}*
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
        EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
        NEW=`echo ${BASE}%{alternative_major}${EXT}`
        mv $OLD $NEW
    fi
done
%endif
%if !%build_system
for OLD in %{buildroot}/%{_bindir}/{%{serverbin}} %{buildroot}/%{_sbindir}/{%{serversbin}}
do
    NEW=`echo ${OLD}%{ol_major}`
    mv $OLD $NEW -f ||:
    if [ -L $NEW ]
        then ln -sf `readlink $NEW`%{ol_major} $NEW
    fi
done
# And the man pages too:
%if %db_internal
for OLD in %{buildroot}/%{_mandir}/man?/{%{serverbin},%{serversbin},slapo}*
%else
for OLD in %{buildroot}/%{_mandir}/man?/{%{serversbin},slapo}*
%endif
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
#        BASE=`perl -e '$name="'${OLD}'"; print "",($name =~ /(.*?)\.[0-9]/), "\n";'`
	EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
	NEW=`echo ${BASE}%{ol_major}${EXT}`
	mv $OLD $NEW
    fi
done
%endif

#Fix binary names and config paths in scripts/configs
perl -pi -e 's,/%{pkg_name}/,/%{name}/,g;s,(/ldap\w?)\b,${1}%{ol_major},g;s,(%{_bindir}/slapd_db_\w+),${1}%{ol_major},g;s,(%{_sbindir}/sl(apd|urpd|aptest))\b,${1}%{ol_major},g;s/ldap%{ol_major}-common/ldap-common/g;s,ldap%{ol_major}.pem,ldap.pem,g;s,/usr/lib,%{_libdir},g' %{buildroot}/{%{_sysconfdir}/%{name}/slapd.conf,%{_initrddir}/ldap%{ol_major},%{_datadir}/%{name}/scripts/*}
perl -pi -e 's/ldap/ldap%{ol_major}/' %{buildroot}/%{_sysconfdir}/logrotate.d/ldap%{ol_major}

mv %{buildroot}/var/run/ldap%{ol_major}/openldap-data/DB_CONFIG.example %{buildroot}/%{_var}/lib/ldap%{ol_major}/
 
# install private headers so as to build additional overlays later
install -d -m 755 %{buildroot}%{_includedir}/%{name}/{include,slapd}
install -m 644 include/*.h  %{buildroot}%{_includedir}/%{name}/include
install -d -m 755 %{buildroot}%{_includedir}/%{name}/include/ac
install -m 644 include/ac/*.h  %{buildroot}%{_includedir}/%{name}/include/ac
install -m 644 servers/slapd/*.h  %{buildroot}%{_includedir}/%{name}/slapd
install -d -m 755 %{buildroot}%{_includedir}/%{name}/libraries/liblunicode/ucdata
install -m 644 libraries/liblunicode/ucdata/*.h %{buildroot}%{_includedir}/%{name}/libraries/liblunicode/ucdata

# Dont drop all  .la files, as OpenLDAP uses them for loading plugins
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/%{name}/*.a

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
#rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%pre servers
%_pre_useradd ldap %{_var}/lib/ldap /bin/false
%_pre_groupadd ldap ldap
# allowing slapd to read hosts.allow and hosts.deny
%{_bindir}/gpasswd -a ldap adm 1>&2 > /dev/null || :

if [ "$1" -ne '1' ]
then
SLAPD_STATUS=`LANG=C LC_ALL=C NOLOCALE=1 service ldap%{ol_major} status 2>/dev/null|grep -q stopped;echo $?`
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} stop
service ldap%{ol_major} recover

%if build_system
LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}

#decide whether we need to migrate at all:
MIGRATE=`%{_sbindir}/slapd%{ol_major} -VV 2>&1|while read a b c d e;do case $d in (2.4.*) echo nomigrate;;(2.*) echo migrate;;esac;done`

if [ "$1" -ne 1 -a -e "$SLAPDCONF" -a "$MIGRATE" != "nomigrate" ]
then 
#`awk '/^[:space:]*directory[:space:]*\w*/ {print $2}' /etc/%{name}/slapd.conf`
dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm"||db=="hdb")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm"||db="hdb")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
for db in $dbs
do
	dbdir=${db/:*/}
	dbsuffix=${db/*:/}
	[ -e /etc/sysconfig/ldap%{ol_major} ] && . /etc/sysconfig/ldap%{ol_major}
# data migration between incompatible versions
# openldap >= 2.2.x have slapcat as a link to slapd, older releases do not
	if [ "${AUTOMIGRATE:-yes}" == "yes" -a -f %{_sbindir}/slapcat ]
	then
		ldiffile="rpm-migrate-to-%{ol_ver_major}.ldif"
		# dont do backups more than onc
		if [ ! -e "${dbdir}/${ldiffile}-imported" -a ! -e "${dbdir}/${ldiffile}-import-failed" ];then
		echo "Migrating pre-OpenLDAP-%{ol_ver_major} data"
		echo "Making a backup of $dbsuffix to ldif file ${dbdir}/$ldiffile"
		# For some reason, slapcat works in the shell when slapd is
		# running but not via rpm ...
		slapcat -b "$dbsuffix" -l ${dbdir}/${ldiffile} ||:
		fi
	fi
done
fi
%endif
# We want post to start the service, but we dont want to start
# it now to create a new database environment in case of db library upgrade
touch /var/lock/subsys/slapd%{ol_major}
fi

%post servers
%if %mdkversion < 200900
/sbin/ldconfig
%endif
SLAPD_STATUS=`LANG=C LC_ALL=C NOLOCALE=1 service ldap%{ol_major} status 2>/dev/null|grep -q stopped;echo $?`
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} stop
# bgmilne: part 2 of gdbm->dbb conversion for data created with 
# original package for 9.1:
dbnum=1
LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}
if [ -e "$SLAPDCONF" ] 
then
dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
for db in $dbs
do	
	dbdir=${db/:*/}
	dbsuffix=${db/*:/}
	ldiffile="rpm-migrate-to-%{ol_ver_major}.ldif"
	if [ -e "${dbdir}/${ldiffile}" ]
	then
		echo -e "\n\nImporting $dbsuffix"
		if [ -e ${dbdir}/ldap-rpm-backup ]
		then 
			echo "Warning: Old ldap backup data in ${dbdir}/ldap-rpm-backup"
			echo "These files will be removed"
			rm -f ${dbdir}/ldap-rpm-backup/*
		fi
	
		echo "Moving the database files fom ${dbdir} to ${dbdir}/ldap-rpm-backup"
		mkdir -p ${dbdir}/ldap-rpm-backup
		mv -f ${dbdir}/{*.bdb,*.gdbm,*.dbb,log.*,__db*} ${dbdir}/ldap-rpm-backup 2>/dev/null
		echo "Importing $dbsuffix from ${dbdir}/${ldiffile}"
		if slapadd%{ol_major} -q -cv -b "$dbsuffix" -l ${dbdir}/${ldiffile} > \
		${dbdir}/rpm-ldif-import.log 2>&1
		then
			mv -f ${dbdir}/${ldiffile} ${dbdir}/${ldiffile}-imported
			echo "Import complete, see log ${dbdir}/rpm-ldif-import.log"
			echo "If any entries were not migrated, see ${dbdir}/${ldiffile}-imported"
		else
			mv -f ${dbdir}/${ldiffile} ${dbdir}/${ldiffile}-import-failed
			echo "Import failed on ${dbdir}/${ldifffile}, see ${dbdir}/rpm-ldif-import.log"
			echo "An ldif dump of $dbsuffix has been saved as ${dbdir}/${ldiffile}-import-failed"
			echo -e "\nYou can import it manually by running (as root):"
			echo "# service ldap%{ol_major} stop"
			echo "# slapadd%{ol_major} -c -l ${dbdir}/${ldiffile}-import-failed"
			echo "# chown $LDAPUSER:$LDAPGROUP ${dbdir}/*"
			echo "# service ldap%{ol_major} start"
		fi
	fi

	chown ${LDAPUSER}:${LDAPGROUP} -R ${dbdir}
	# openldap-2.0.x->2.1.x on ldbm/dbb backend seems to need reindex regardless:
	#slapindex -n $dbnum
	#dbnum=$[dbnum+1]
done
fi
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} start

# Setup log facility for OpenLDAP on new install
%if %{?_post_syslogadd:1}%{!?_post_syslogadd:0}
%_post_syslogadd /var/log/ldap%{ol_major}/ldap.log local4
perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"local4\"|" \
    %{_sysconfdir}/sysconfig/ldap%{ol_major}
%else
if [ -f %{_sysconfdir}/syslog.conf -a $1 -eq 1 ]
then
	# clean syslog
	perl -pi -e "s|^.*ldap%{ol_major}.*\n||g" %{_sysconfdir}/syslog.conf 

	# probe free local-users
	cntlog=""
	for log in 7 6 5 3 2 1 0 4
	do 
		grep -vE "local${log}[^;]*\.none" %{_sysconfdir}/syslog.conf|grep -q local${log} || cntlog="${log}"
	done

	if [ "${cntlog}" != "" ];then
		echo "# added by %{name}-%{version} rpm $(date)" >> %{_sysconfdir}/syslog.conf
#   modified by Oden Eriksson
#		echo "local${cntlog}.*       /var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf
		echo -e "local${cntlog}.*\t\t\t\t\t\t\t-/var/log/ldap%{ol_major}/ldap.log" >> %{_sysconfdir}/syslog.conf

		# reset syslog daemon
		if [ -f /var/lock/subsys/syslog ]; then
        		service syslog restart  > /dev/null 2>/dev/null || : 
		elif [ -f /var/lock/subsys/rsyslog ]; then
			service rsyslog restart > /dev/null 2>/dev/null || :
		fi
	else
		echo "I can't set syslog local-user!"
	fi
		
	# set syslog local-user in /etc/sysconfig/ldap
	perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"LOCAL${cntlog}\"|g" %{_sysconfdir}/sysconfig/ldap%{ol_major}

fi
%endif

# Handle switch from %{_sysconfdir}/ssl/%{name}/ldap.pem to %{_sysconfdir}/pki/tls/private/ldap.pem
if [ -e %{_sysconfdir}/ssl/%{name}/ldap.pem -a ! -e %{_sysconfdir}/pki/tls/private/ldap.pem ]
then
  mv %{_sysconfdir}/ssl/%{name}/ldap.pem %{_sysconfdir}/pki/tls/private/ldap.pem
  ln -s %{_sysconfdir}/pki/tls/private/ldap.pem %{_sysconfdir}/ssl/%{name}/ldap.pem
fi
# generate the ldap.pem cert here instead of the initscript
%if %{?_create_ssl_certificate:1}%{!?_create_ssl_certificate:0}
%_create_ssl_certificate -g ldap ldap
%else
if [ ! -e %{_sysconfdir}/pki/tls/private/ldap.pem ]
then
  if [ -x %{_datadir}/%{name}/gencert.sh ] ; then
    echo "Generating self-signed certificate..."
    pushd %{_sysconfdir}/pki/tls/private > /dev/null
    yes ""|%{_datadir}/%{name}/gencert.sh >/dev/null 2>&1
    chmod 640 ldap.pem
    chown root:ldap ldap.pem
    popd > /dev/null
  fi
  echo "To generate a self-signed certificate, you can use the utility"
  echo "%{_datadir}/%{name}/gencert.sh..."
fi
%endif

pushd %{_sysconfdir}/%{name}/ > /dev/null
for i in slapd.conf slapd.access.conf ; do
	if [ -f $i ]; then
		chmod 0640 $i
		chown root:ldap $i
	fi
done
popd > /dev/null


%_post_service ldap%{ol_major}

# nscd reset
if [ -f /var/lock/subsys/nscd ]; then
        service nscd restart  > /dev/null 2>/dev/null || : 
fi


%preun servers
%_preun_service ldap%{ol_major}


%postun servers
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%if %{?_preun_syslogdel:1}%{?!_preun_syslogdel:0}
%_preun_syslogdel
%else
if [ $1 = 0 ]; then 
	# remove ldap entry 
	perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf 

	# reset syslog daemon
	if [ -f /var/lock/subsys/syslog ]; then
	        service syslog restart  > /dev/null 2>/dev/null || : 
	elif [ -f /var/lock/subsys/rsyslog ]; then
		service rsyslog restart > /dev/null 2>/dev/null || :
	fi
fi
%endif
%_postun_userdel ldap
%_postun_groupdel ldap


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%triggerpostun -- openldap-clients < 2.1.25-5mdk
# We may have openldap client configuration in /etc/ldap.conf
# which now needs to be in /etc/openldap/ldap.conf
if [ -f /etc/ldap.conf ] 
then
	mv -f /etc/%{name}/ldap.conf /etc/%{name}/ldap.conf.rpmfix
	cp -af /etc/ldap.conf /etc/%{name}/ldap.conf
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/ldapserver
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ldap.conf
%{_mandir}/man5/ldap.conf%{ol_major}.5*
%{_mandir}/man5/ldif%{ol_major}.5*
%doc README.mdk


%files doc
%defattr(-,root,root)
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README 
%if %build_migration
%doc README.migration TOOLS.migration
%endif
%doc doc/rfc doc/drafts
#%config(noreplace) %{_sysconfdir}/%{name}/ldapfilter.conf
#%config(noreplace) %{_sysconfdir}/%{name}/ldapsearchprefs.conf
#%config(noreplace) %{_sysconfdir}/%{name}/ldaptemplates.conf
#%{_datadir}/%{name}/ldapfriendly
#%{_mandir}/man5/ldapfilter.conf.5*
#%{_mandir}/man5/ldapfriendly.5*
#%{_mandir}/man5/ldapsearchprefs.conf.5*
#%{_mandir}/man5/ldaptemplates.conf.5*
%doc %{_docdir}/%{name}-guide

%if %build_migration
%files migration
%defattr(-,root,root)
%{_datadir}/%{name}/migration
%endif


%files servers
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/schema
#%dir %{_sysconfdir}/%{name}/slapd.d
#%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/ssl/openldap/ldap.pem
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/%{name}/slapd.conf
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/%{name}/slapd.ldif
%dir %attr(750,ldap,ldap) %{_sysconfdir}/%{name}/slapd.d
%attr(640,root,ldap) %{_sysconfdir}/%{name}/DB_CONFIG.example
%attr(640,root,ldap) %config %{_sysconfdir}/%{name}/slapd.access.conf

#dir %{_sysconfdir}/ssl/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/schema/*.schema
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/schema
%{_datadir}/%{name}/schema/*.schema
%{_datadir}/%{name}/schema/*.ldif
%{_datadir}/%{name}/schema/README
#%dir %{_datadir}/%{name}/ucdata
#%{_datadir}/%{name}/ucdata/*.dat
%{_datadir}/%{name}/scripts
%{_sysconfdir}/cron.hourly/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.daily/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.weekly/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.monthly/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.yearly/ldap-hot-db-backup%{ol_major}

%config(noreplace) %{_sysconfdir}/sysconfig/ldap%{ol_major}
%config(noreplace) %{_initrddir}/ldap%{ol_major}
%attr(750,ldap,ldap) %dir %{_var}/lib/ldap%{ol_major}
%config(noreplace) %{_var}/lib/ldap%{ol_major}/DB_CONFIG
%{_var}/lib/ldap%{ol_major}/DB_CONFIG.example
%attr(755,ldap,ldap) %dir /var/run/ldap%{ol_major}
#%{_datadir}/openldap/*.help
%{_datadir}/%{name}/gencert.sh
%{_sbindir}/*


%dir %{_libdir}/%{name}
%if %build_modules && !%build_modpacks
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.so*
#%exclude %{_libdir}/%{name}/*.a
%endif

%{_mandir}/man5/slap*.5*
%{_mandir}/man8/*

%attr(750,ldap,ldap) %dir /var/log/ldap%{ol_major}
%config(noreplace) %{_sysconfdir}/logrotate.d/ldap%{ol_major}

%if %db_internal
#internal version of db
%{_libdir}/libslapd%{ol_suffix}_db*
%attr(755,root,root)%{_bindir}/slapd_db*
%exclude %{_prefix}/docs
%exclude %{_includedir}/db*.h
%endif

%doc contrib/slapd-modules/acl/README.acl
%doc contrib/slapd-modules/addpartial/README.addpartial
%doc contrib/slapd-modules/allop/README.allop
%doc contrib/slapd-modules/allowed/README.allowed
%doc contrib/slapd-modules/autogroup/README.autogroup
#doc contrib/slapd-modules/dsaschema/README.dsaschema
%if %mdkversion >= 201010
%doc contrib/slapd-modules/kinit/README.kinit
%endif
%doc contrib/slapd-modules/passwd/README.passwd
%doc contrib/slapd-modules/passwd/sha2/README.sha2
%if %build_smbk5pwd
%doc contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%endif
%if %build_nssov
%doc contrib/slapd-modules/nssov/README.nssov
%endif

%files clients
%defattr(-,root,root)
%{_bindir}/ldap*
%{_mandir}/man1/*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/lib*.so.*


%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/libl*.so
%{_includedir}/l*.h
%{_includedir}/s*.h
%{_includedir}/%{name}
%{_mandir}/man3/*

%files -n %libname-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%if %build_modpacks
%files back_dnssrv
%defattr(-,root,root)
%{_libdir}/%{name}/back_dnssrv.la
%{_libdir}/%{name}/back_dnssrv*.so.*
%{_libdir}/%{name}/back_dnssrv*.so

%files back_ldap
%defattr(-,root,root)
%{_libdir}/%{name}/back_ldap.la
%{_libdir}/%{name}/back_ldap*.so.*
%{_libdir}/%{name}/back_ldap*.so

%files back_passwd
%defattr(-,root,root)
%{_libdir}/%{name}/back_passwd.la
%{_libdir}/%{name}/back_passwd*.so.*
%{_libdir}/%{name}/back_passwd*.so
%endif #build_modpacks

%if %build_sql && %build_modpacks
%files back_sql
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/back_sql.la
%{_libdir}/%{name}/back_sql*.so.*
%{_libdir}/%{name}/back_sql*.so
%endif

%files tests
%defattr(-,root,root)
%{_datadir}/%{name}/tests

%files testprogs
%defattr(-,root,root)
%{_bindir}/slapd-*
%{_bindir}/ldif-filter%{ol_major}
#
# Todo:
# - add cron-job to remove transaction logs (bdb)

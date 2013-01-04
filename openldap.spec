%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define pkg_name openldap
%global beta %{nil}

#defaults
%define build_system 1
%define build_alternatives 0
%define build_modules 1
%define build_modpacks 0
%define build_slp 0
%define build_heimdal 0
%define build_nssov 1
%define build_smbk5pwd 1
%define build_asmmutex 0
%global build_migration 0

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

%define major 2.4_2
%define fname ldap
%define libname %mklibname %{fname} %{major}
%define migtools_ver 45

# we want to use the default db version for each release, so as
# to make backport binary compatibles
# excepted for very old systems, where we use bundled db
%define bundled_db_source_ver 4.8.30
%define dbdevel db-devel
%global db_internal 0
%define dbver 5.2.0
%define dbutils db-utils
%define dbutilsprefix db52_

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
%global serverbin	slapd-addel,slapd-bind,slapd-modify,slapd-modrdn,slapd-read,slapd-search,slapd-tester,ldif-filter
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

Summary:	LDAP servers and sample clients
Name:		%{pkg_name}%{ol_major}
Version:	2.4.33
Release:	2
License:	Artistic
Group:		System/Servers
URL:		http://www.openldap.org

# Openldap source
Source0:	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{pkg_name}-%{version}%{beta}.tgz

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

# Extended Schema 
Source54:	mull.schema

# Doc sources, used to build SOURCE12 and SOURCE13 above
Source100:	openldap-2.4-admin-guide-add-vendor-doc.patch
Source101:	vendor.sdf
Source102:	vendor-standalone.sdf

# Chris Patches
Patch0:		%{pkg_name}-2.3.4-config.patch
Patch1:		%{pkg_name}-2.0.7-module.patch

#Fix various paths in smbk5pwd:
Patch2:		openldap-2.3-smbk5passwd-paths.patch
# For now, only build support for SMB (no krb5) changing support in smbk5passwd
# overlay:
Patch3:		openldap-2.3.4-smbk5passwd-only-smb.patch
Patch4:		openldap-2.4.25-contrib-makefiles-with-tests.patch
Patch5:		openldap-2.4.8-fix-lib-perms.patch
Patch6:		openldap-2.4.12-test001-check-slapcat.patch

# RH + PLD Patches
Patch15:	%{pkg_name}-cldap.patch

# schema patch
Patch46:	openldap-2.0.21-schema.patch
Patch47:	openldap-2.4.12-change-dyngroup-schema.patch

Patch53:	%pkg_name-ntlm.patch

#patches in CVS
# see http://www.stanford.edu/services/directory/openldap/configuration/openldap-build.html
# for other possibly interesting patches

%{?_with_cyrussasl:BuildRequires:	libsasl-devel}
%{?_with_kerberos:BuildRequires:	krb5-devel}
BuildRequires:	openssl-devel, perl
%if %build_slp
BuildRequires:	openslp-devel
%endif
%if %build_heimdal
BuildRequires:	heimdal-devel
%endif
%if %build_sql
BuildRequires:	unixODBC-devel
%endif
%if %back_perl
BuildRequires:	perl-devel
%endif
BuildRequires:	%{dbdevel} >= %{dbver}
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libltdl-devel
BuildRequires:	krb5-devel
BuildRequires:	groff
# for make test:
BuildRequires:	diffutils
Requires:	shadow-utils, setup

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The suite includes a
stand-alone LDAP server (slapd) which is in the -servers package, libraries for
implementing the LDAP protocol (in the lib packages), and utilities, tools, and
sample clients (in the -clients package). The openldap binary package includes
only configuration files used by the libraries.

Install openldap if you need LDAP applications and tools.

%package servers
Summary:	OpenLDAP servers and related files
Group:		System/Servers
Requires(pre):	rpm-helper >= 0.23 coreutils shadow-utils
BuildRequires:	rpm-helper >= 0.23
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
Requires(pre):	%{dbutils}
Requires(post):	%{dbutils}
# slapd checks at startup if the library version matches exactly what it
# was compiled against, so we cant allow newer versions, e.g.:
#bdb_back_initialize: BDB library version mismatch: expected Berkeley DB 4.8.26: (December 30, 2009), got Berkeley DB 4.8.30: (March 25, 2011)
# This might need to be changed to a library dependency, but we need to verify
# library provides on multiple distros before doing that
Requires:	%{dbutils} >= %{dbver}

%if %{?_with_cyrussasl:1}%{!?_with_cyrussasl:0}
%define saslver %([ -f "%{_includedir}/sasl/sasl.h" ] && echo -e "#include <sasl/sasl.h>\\nSASL_VERSION_MAJOR SASL_VERSION_MINOR SASL_VERSION_STEP"|cpp|awk 'END {printf "%s.%s.%s",$1,$2,$3}' || echo "2.1.22")
%define sasllib %mklibname sasl 2
#Ensure we have the sasl library we compiled against available in post so
#slapadd etc works
Requires(post):	%{sasllib} = %{saslver}
%endif

Requires:	%{libname} = %{version}-%{release}
Requires:	%{pkg_name}%{ol_major}-extra-schemas >= 1.3-7
Requires(pre):	%{pkg_name}%{ol_major}-extra-schemas >= 1.3-7

%description servers
OpenLDAP Servers

This package contains the OpenLDAP server, slapd (LDAP server), additional 
backends, configuration files, schema definitions required for operation, and 
database maintenance tools

This server package was compiled with support for the %{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}
database library.

%package clients
Summary:	OpenLDAP clients and related files
Group:		System/Servers
Requires:	%{libname} = %{version}-%{release}

%description clients
OpenLDAP clients

This package contains command-line ldap clients (ldapsearch, ldapadd etc)

%package -n %{libname}
Summary:	OpenLDAP libraries
Group:		System/Libraries
Provides:	lib%{fname} = %{version}-%{release}
Requires:	%{name}

%description -n %{libname}
This package includes the libraries needed by ldap applications.

%package -n %{libname}-devel
Summary:	OpenLDAP development libraries and header files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	tcp_wrappers-devel
Provides:	%{name}-devel = %{version}-%{release}
%if %build_system
Provides: 	lib%{fname}-devel = %{version}-%{release}
Provides:	openldap2-devel = %{version}-%{release}
Obsoletes: 	openldap-devel < %{version}-%{release}
%endif
Conflicts:	libldap1-devel
Conflicts:	%mklibname -d ldap 2
Conflicts:	%mklibname -d ldap 2.3_0

%description -n %{libname}-devel
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
LDAP clients.

%package -n %{libname}-static-devel
Summary: 	OpenLDAP development static libraries
Group: 		Development/C
Requires: 	%{libname}-devel = %{version}-%{release}
%if %build_system
Provides: 	lib%{fname}-devel-static = %{version}-%{release}
Provides: 	lib%{fname}-static-devel = %{version}-%{release}
Provides:	openldap-devel-static = %{version}-%{release}
Provides:	openldap-static-devel = %{version}-%{release}
Obsoletes: 	openldap-devel-static < %{version}-%{release}
%endif
Conflicts:	libldap1-devel

%description -n %{libname}-static-devel
OpenLDAP development static libraries

%if %build_modpacks
%package back_dnssrv
Summary:	Module dnssrv for OpenLDAP
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	openldap-servers = %{version}-%{release}

%description back_dnssrv
The dnssrv daabase backend module for OpenLDAP daemon

%package back_ldap
Summary:	Module ldap for OpenLDAP
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	openldap-servers = %{version}-%{release}

%description back_ldap
The ldap database backend module for OpenLDAP daemon

%package back_passwd
Summary:	Module passwd for OpenLDAP
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	openldap-servers = %{version}-%{release}

%description back_passwd
The passwd database backend module for OpenLDAP daemon
%endif

%if %build_sql && %build_modpacks
%package back_sql
Summary:	Module sql for OpenLDAP
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	openldap-servers = %{version}-%{release}

%description back_sql
The sql database backend module for OpenLDAP daemon
%endif

%package doc
Summary:	OpenLDAP documentation and administration guide
Group:		Books/Computer books
Requires:	openldap
Provides:	openldap-guide

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
%setup -q  -n %{pkg_name}-%{version}%{beta}

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

%patch46 -p1 -b .mdk
%patch47 -p1 -b .dyngroup
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

unset CONFIGURE_TOP

#FIXME: Some script backends should not be used with threads, mostly shell/perl

%if !%build_system
perl -pi -e 's,(progname = "\w+)",${1}%{ol_major}",g' servers/slapd/*.c
perl -pi -e 's,({"slap\w+)",${1}%{ol_major}",g' servers/slapd/main.c
%endif

# don't choose db4.3 even if it is available
export ol_cv_db_db_4_dot_3=no
# try and miss linuxthreads, so we get a threading lib on glibc2.4:
export ol_cv_header_linux_threads=no
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
    kinit \
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
 kinit \
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
    kinit \
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
%if !%{build_system} || %{build_alternatives}
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
for OLD in %{buildroot}/%{_mandir}/man?/{%{serversbin},slapo}*
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
dbs=`awk 'BEGIN {OFS=":"} /[[:space:]]*^database[[:space:]]*\w*/ {db=$2;suf="";dir=""}; /^[[:space:]]*suffix[[:space:]]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm"||db=="hdb")&&(suf!=""&&dir!="")) print dir,suf};/^[[:space:]]*directory[[:space:]]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm"||db="hdb")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
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
dbs=`awk 'BEGIN {OFS=":"} /[[:space:]]*^database[[:space:]]*\w*/ {db=$2;suf="";dir=""}; /^[[:space:]]*suffix[[:space:]]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};/^[[:space:]]*directory[[:space:]]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
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

%triggerpostun -- openldap-clients < 2.1.25-5mdk
# We may have openldap client configuration in /etc/ldap.conf
# which now needs to be in /etc/openldap/ldap.conf
if [ -f /etc/ldap.conf ] 
then
	mv -f /etc/%{name}/ldap.conf /etc/%{name}/ldap.conf.rpmfix
	cp -af /etc/ldap.conf /etc/%{name}/ldap.conf
fi

%files
%config(noreplace) %{_sysconfdir}/%{name}/ldapserver
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ldap.conf
%{_mandir}/man5/ldap.conf%{ol_major}.5*
%{_mandir}/man5/ldif%{ol_major}.5*
%doc README.mdk


%files doc
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README 
%doc doc/rfc doc/drafts
%doc %{_docdir}/%{name}-guide

%files servers
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/schema
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/%{name}/slapd.conf
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/%{name}/slapd.ldif
%dir %attr(750,ldap,ldap) %{_sysconfdir}/%{name}/slapd.d
%attr(640,root,ldap) %{_sysconfdir}/%{name}/DB_CONFIG.example
%attr(640,root,ldap) %config %{_sysconfdir}/%{name}/slapd.access.conf
%config(noreplace) %{_sysconfdir}/%{name}/schema/*.schema
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/schema
%{_datadir}/%{name}/schema/*.schema
%{_datadir}/%{name}/schema/*.ldif
%{_datadir}/%{name}/schema/README
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
%{_datadir}/%{name}/gencert.sh
%{_sbindir}/*

%dir %{_libdir}/%{name}
%if %build_modules && !%build_modpacks
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.so*
%endif

%{_mandir}/man5/slap*.5*
%{_mandir}/man8/*

%attr(750,ldap,ldap) %dir /var/log/ldap%{ol_major}
%config(noreplace) %{_sysconfdir}/logrotate.d/ldap%{ol_major}

%doc contrib/slapd-modules/acl/README.acl
%doc contrib/slapd-modules/addpartial/README.addpartial
%doc contrib/slapd-modules/allop/README.allop
%doc contrib/slapd-modules/allowed/README.allowed
%doc contrib/slapd-modules/autogroup/README.autogroup
#doc contrib/slapd-modules/dsaschema/README.dsaschema
%doc contrib/slapd-modules/kinit/README.kinit
%doc contrib/slapd-modules/passwd/README.passwd
%doc contrib/slapd-modules/passwd/sha2/README.sha2
%if %build_smbk5pwd
%doc contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%endif
%if %build_nssov
%doc contrib/slapd-modules/nssov/README.nssov
%endif

%files clients
%{_bindir}/ldap*
%{_mandir}/man1/*

%files -n %libname
%{_libdir}/lib*.so.*

%files -n %libname-devel
%{_libdir}/libl*.so
%{_includedir}/l*.h
%{_includedir}/s*.h
%{_includedir}/%{name}
%{_mandir}/man3/*

%files -n %libname-static-devel
%{_libdir}/lib*.a

%if %build_modpacks
%files back_dnssrv
%{_libdir}/%{name}/back_dnssrv.la
%{_libdir}/%{name}/back_dnssrv*.so.*
%{_libdir}/%{name}/back_dnssrv*.so

%files back_ldap
%{_libdir}/%{name}/back_ldap.la
%{_libdir}/%{name}/back_ldap*.so.*
%{_libdir}/%{name}/back_ldap*.so

%files back_passwd
%{_libdir}/%{name}/back_passwd.la
%{_libdir}/%{name}/back_passwd*.so.*
%{_libdir}/%{name}/back_passwd*.so
%endif #build_modpacks

%if %build_sql && %build_modpacks
%files back_sql
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/back_sql.la
%{_libdir}/%{name}/back_sql*.so.*
%{_libdir}/%{name}/back_sql*.so
%endif

%files tests
%{_datadir}/%{name}/tests

%files testprogs
%{_bindir}/slapd-*
%{_bindir}/ldif-filter%{ol_major}
#
# Todo:
# - add cron-job to remove transaction logs (bdb)


%changelog
* Fri Jan  4 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.4.33-2
- remove outdated autofs schema
- fix awk scriptlet

* Tue May 01 2012 Oden Eriksson <oeriksson@mandriva.com> 2.4.31-1mdv2012.0
+ Revision: 794733
- avoid nuking the *.la files (needed by openldap per design)
- 2.4.31
- disable rpmlint
- sync with openldap-2.4.29-2.mga2.src.rpm

* Wed Dec 28 2011 Buchan Milne <bgmilne@mandriva.org> 2.4.28-1
+ Revision: 745869
- Sync with Mageia:
 - Drop shared library libtool files, but keep plugin libtool files
 - Fix errors from 'service ldap recover' etc. due to versioned binaries in db51-utils
- revert addition of pam-devel BR
- revert additional macro for disabling tests, --without-test can be used

  + Oden Eriksson <oeriksson@mandriva.com>
    - 2.4.28
    - rediffed P4
    - make it possible to skip the tests

* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.26-4
+ Revision: 739200
- try to fix the build
- rebuilt for new unixODBC (second try)
- rebuilt for new unixODBC

* Sun Oct 16 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.26-2
+ Revision: 704845
- fix deps (pam-devel)
- rebuild

  + Buchan Milne <bgmilne@mandriva.org>
    - Revert r675900, 'make openldap less restrictibe requiring db', it can break upgrades
    - Add a description of why we have an exact version dependency
    - Sync with Mageia

* Thu Jul 07 2011 Buchan Milne <bgmilne@mandriva.org> 2.4.26-1
+ Revision: 689053
- New version 2.4.26
- Allow build-time overrides for some contrib overlays which dont build on older
  toolchains

* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.25-5
+ Revision: 686320
- avoid pulling 32 bit libraries on 64 bit arch

  + Luis Daniel Lucio Quiroz <dlucio@mandriva.org>
    - fixes to let compile under 2010.2

* Tue May 17 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 2.4.25-3
+ Revision: 675900
- make openldap less restrictibe requiring db

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.25-2
+ Revision: 666954
- mass rebuild

* Thu Mar 31 2011 Buchan Milne <bgmilne@mandriva.org> 2.4.25-1
+ Revision: 649407
- Fix contrib test/install with internal berkeley db
- Dont build kinit overlay on releases without krb5 1.8.x (requires Fast negotiation)
- Disable test/install of dsaschema, it is broken on 32bit
- Relax db buildrequire to allow newer releases
- Fix nssov linking without openldap development libraries installed
- New version 2.4.25
-Put all work regarding contrib overlays in a single patch intended for upstream
 that makes make targets consistent, and adds a sanity-check 'test' target
- Reload syslog instead of restart, and take care of rsyslog as well
- Add patch adding install targets to overlays with makefiles but no install target
- Fix backports to systems with db4
- Re-order building of contrib overlays
- Enable nssov

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - build against berkeley db 5.1.25

* Thu Feb 17 2011 Buchan Milne <bgmilne@mandriva.org> 2.4.24-1
+ Revision: 638083
- New version 2.4.24
- Rename %%sql to %%build_sql, to prevent crashing rpm
- Speed up database host backup (Richard Soderberg)

* Thu Dec 02 2010 Buchan Milne <bgmilne@mandriva.org> 2.4.23-4mdv2011.0
+ Revision: 604757
- Fix dependencies for db-5.x (s/db4/db/g)

* Thu Nov 25 2010 Buchan Milne <bgmilne@mandriva.org> 2.4.23-3mdv2011.0
+ Revision: 601162
- Allow db5.1

* Thu Nov 25 2010 Buchan Milne <bgmilne@mandriva.org> 2.4.23-2mdv2011.0
+ Revision: 601144
- Improve default client SSL settings
  Bundle the correct Berkeley DB copy, but build against 4.8.26 for 2010.1
  Try and correct some nssov issues, but disabled for now as it is still broken

  + Funda Wang <fwang@mandriva.org>
    - update dbver

  + Oden Eriksson <oeriksson@mandriva.com>
    - 2.4.23
    - drop P7, it's added upstream

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.4.22-2mdv2010.1
+ Revision: 540359
- rebuild so that shared libraries are properly stripped again

* Tue Apr 27 2010 Buchan Milne <bgmilne@mandriva.org> 2.4.22-1mdv2010.1
+ Revision: 539539
- Add patch from head fixing proxy control propagation (r1.259 in back-ldap/bind.c)
- clean some rpm-helper deps
- New version 2.4.22
- Re-enable nssov by default without any nss-ldapd hacks
- Tighten schema requires to avoid errors in pre
- Ensure group is added even if private groups are not enabled (Eugeni)

* Tue Apr 06 2010 Funda Wang <fwang@mandriva.org> 2.4.21-5mdv2010.1
+ Revision: 531957
- rebuild for new openssl

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against openssl-0.9.8m

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - adapt to new %%_post_syslogadd behaviour

* Wed Dec 30 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.21-2mdv2010.1
+ Revision: 483941
- Update to db-4.8.26

* Tue Dec 29 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.21-1mdv2010.1
+ Revision: 483295
- New version 2.4.21
- init script fixes for SSL with back-config (Leo Bergolth)
- Try harder to use db4.8 by default

* Sun Nov 29 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.20-1mdv2010.1
+ Revision: 471347
- New version 2.4.20
- Switch to db4.8
- Use syslog helper macro if available
- Use SSL cert helper macro if available
- Move SSL certs from /etc/ssl/openldap to /etc/pki/tls/private

* Tue Nov 24 2009 Frederik Himpe <fhimpe@mandriva.org> 2.4.19-3mdv2010.1
+ Revision: 469777
- Add support for rsyslog

* Mon Oct 12 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.19-2mdv2010.0
+ Revision: 456810
- Use a pseudo-random base port for tests
- Use a newer killproc options (delay, pid file) if available, and fall back to an
 internal version that is new enough if not

* Tue Oct 06 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.19-1mdv2010.0
+ Revision: 454919
- New version 2.4.19

* Mon Sep 07 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.18-1mdv2010.0
+ Revision: 432771
- New version 2.4.18
- rediff patches for fuzz
- Require new enough openldap-mandriva-dit to avoid missing schema that were in
 openldap-servers before
- Run tests on all backends available, not just bdb
- Update to db 4.7.25.4 (for build with internal copy)

* Sun Jul 19 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.17-2mdv2010.0
+ Revision: 397917
- Migrate the rest of the non-core schema out

* Sun Jul 19 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.17-1mdv2010.0
+ Revision: 397474
- New version 2.4.17
- Remove schema files that are shipped in openldap-extra-schemas
- Require openldap-extra-schemas

* Wed Jun 24 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.16-2mdv2010.0
+ Revision: 388877
- Always run recovery on upgrade, to smoothly handle database library upgrades

* Mon Apr 06 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.16-1mdv2009.1
+ Revision: 364349
- New version 2.4.16

* Tue Feb 24 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.15-1mdv2009.1
+ Revision: 344541
- update to new version 2.4.15

* Mon Feb 16 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.14-1mdv2009.1
+ Revision: 340709
- Fix fuzz
- New version 2.4.14
- Drop patches for ITS 5768,5809,5849
- Add some contrib overlays

* Tue Feb 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.13-5mdv2009.1
+ Revision: 337186
- keep bash completion in its own package

* Thu Jan 29 2009 Funda Wang <fwang@mandriva.org> 2.4.13-4mdv2009.1
+ Revision: 335107
- rebuild for new libtool

* Thu Jan 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.13-3mdv2009.1
+ Revision: 329910
- use bdb 4.6 on 2008.1 too

* Fri Jan 02 2009 Buchan Milne <bgmilne@mandriva.org> 2.4.13-2mdv2009.1
+ Revision: 323305
- Disable direct gssapi support for now (though we need to find a way to enable it
  again (should fix bug #46573)
- Build against db4.6 by default on 2009.0 (but still ship 4.7 source)
- Tighten up db4-util requires

* Sat Dec 13 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.13-1mdv2009.1
+ Revision: 313955
- New version 2.4.13
- Switch to db4.7
- Drop ITS patches upstreamed
- ITS #5768 Fixed libldap_r deref building
- ITS #5809 Fixed slapd syncrepl rename handling
- ITS #5849 Fixed libldap peer cert memory leak

* Wed Nov 05 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.12-5mdv2009.1
+ Revision: 300112
- Fix for ITS #5745 slapcat fails and doesn't return correct error status for bdb fatal error
- Fix for ITS #5709 slapd sync provider skips some objects
- Fix for ITS #5698 slapd crashes after trying to add an invalid database entry
- Fix for ITS #5766 smbkrb5 overlay doesn't honour kerberos principal expiration
- Include current db4.6 patches for build against internal copy

* Fri Oct 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.12-4mdv2009.1
+ Revision: 294614
- modify dyngroup.schema so as to use autogroup overlay

* Tue Oct 14 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.12-3mdv2009.1
+ Revision: 293664
- New version 2.4.12

* Mon Sep 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.11-3mdv2009.0
+ Revision: 284964
- devel packages requires libwrap-devel

* Wed Jul 23 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.11-2mdv2009.0
+ Revision: 242559
- patch5: ensure libs are installed with executable bit set, so as to have debug symbols included indebug package

* Fri Jul 18 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.11-1mdv2009.0
+ Revision: 238145
- New version 2.4.11

* Wed Jul 16 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.10-3mdv2009.0
+ Revision: 236365
- Initial support for back-config configurations in init script

* Tue Jul 15 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.10-2mdv2009.0
+ Revision: 236103
- ITS #5580 (CVS-2008-2952 / MDVSA-2008:144)
- Alternative fix for ITS #5569
- Bump release
- Add patch for ITS #5569 (smbk5pwd interferes with ppolicy)

* Wed Jun 11 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.10-1mdv2009.0
+ Revision: 218095
- New version 2.4.10
  Fix smbpwd overlay symlinks
  Avoid stripping binaries at install time to get usable debug packages

* Mon Jun 09 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.9-2mdv2009.0
+ Revision: 217233
- Workaround struct ucred glibc 2.8 issue
  Fix overlinking/underliking for contrib overlays
- Maintain backportability

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 08 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.9-1mdv2009.0
+ Revision: 204515
- 2.4.9
- added P200 (db46-update-4.6.21.1.diff) from the db46 package for completeness

* Sun Mar 23 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.8-2mdv2008.1
+ Revision: 189682
- Ship slapd headers in devel package to allow out-of-tree module compilation
 (Guillaume Rousse)
- Ship addpartial and autogroup overlays
- Ship smbk5pwd overlay without heimdal support as smbpwd to not conflict
  with heimdal-enabled smbk5pwd overlay from openldap-smbk5pwd package
- Drop explicit perl-MIME-Base64 dependency in migration subpackage
- Ship the allop overlay from contrib/ (Guillaume Rousse)
  Avoid conflicting with other openldap packages, and make bash completion work
  for non-system case

* Mon Feb 25 2008 Buchan Milne <bgmilne@mandriva.org> 2.4.8-1mdv2008.1
+ Revision: 174893
- Drop patches which are no longer required
- rediff ntlm patch
- Always ship db4 source, so srpm rebuilds more easily on older distros
- New version 2.4.8
- Rework backend options (so new backends will be enabled as modules by default)

  + Thierry Vignaud <tv@mandriva.org>
    - fix description-line-too-long

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - fix bash completion

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.7-4mdv2008.1
+ Revision: 136101
- fix krb5-devel <-> openldap-devel cross linkage (take one)

* Fri Dec 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.7-3mdv2008.1
+ Revision: 136062
- really build system (silly bs bug...)
- added db-4.6.21.tar.gz
- 2.4.7

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 09 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.39-5mdv2008.1
+ Revision: 116780
- use correct source file for bash completion

* Sat Dec 08 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.39-4mdv2008.1
+ Revision: 116519
- bash completion

* Wed Dec 05 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.39-3mdv2008.1
+ Revision: 115711
- Add fix for slapadd hang when not using quick mode (-q)

* Wed Nov 07 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.39-2mdv2008.1
+ Revision: 106742
- rebuild

* Mon Oct 29 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.39-1mdv2008.1
+ Revision: 103016
- New version 2.3.39
- Drop ITS4873 patch, applied upstream
- Optional support (--with heimdal) for changing Heimdal passwords in smbk5pwd

* Tue Sep 18 2007 Anssi Hannula <anssi@mandriva.org> 2.3.38-3mdv2008.0
+ Revision: 89723
- rebuild due to package loss

  + Andreas Hasenack <andreas@mandriva.com>
    - fix indentation error in sudo.schema

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 2.3.38-2mdv2008.0
+ Revision: 69740
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Wed Aug 22 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.38-1mdv2008.0
+ Revision: 69115
- New version 2.3.38
- Fix program names in test scripts in non-system case

* Thu Aug 16 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.37-1mdv2008.0
+ Revision: 64124
- Double the size of the SRPM by always shipping db4 source (to avoid build system
  problems)
- New version 2.3.37
-Update URLs for Berkeley DB
-Add 4.2.52.5 patch from upstream
-Add Howards cache memory leak fix
-Fix building with internal db4 (and activate it for anything without the above
 patches)

  + Andreas Hasenack <andreas@mandriva.com>
    - updated dhcp schema from version 3.0.5 of the dhcp patch

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 2.3.36-1mdv2008.0
+ Revision: 43205
- use better rpm group for test packages

  + Buchan Milne <bgmilne@mandriva.org>
    - New version 2.3.36

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3.35-2mdv2008.0
+ Revision: 33634
- rebuilt due to fixed initscript
- make sure slurpd is shut down

* Sun Apr 22 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.35-1mdv2008.0
+ Revision: 17103
- New version 2.3.35
- Patches from CVS:
  - Fixed slapd-bdb no-op crasher (ITS#4925)
  - Fixed libldap response code handling on rebind (ITS#4924)


* Fri Mar 23 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.34-5mdv2007.1
+ Revision: 148682
- Fix syslog facility selection with new default syslog.conf (Bug #29687)

* Fri Mar 16 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.34-4mdv2007.1
+ Revision: 144974
- Last fixes for test suite

* Thu Mar 15 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.34-3mdv2007.1
+ Revision: 144262
- ITS #4873 - user contributed fix for ACL set memory leak
- fix up syslog configuration in postinstall a bit

* Tue Mar 13 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.34-2mdv2007.1
+ Revision: 143193
- Fix some missing system vs non-system issues
- Apply patch derived from my changes to HEAD for tests not writing to the test
  dir
- ITS #4854 - Fixed str2anlist handling of undefined attrs/OCs (segfault)
- ITS #4851 - Fixed slapd-bdb/hdb startup with missing shm env
- ITS #4853 - Fixed slapo-refint config message
- ITS #4855 - Fixed libldap_r tpool reset
- Ship the test suite in a working condition

* Sat Feb 17 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.34-1mdv2007.1
+ Revision: 122184
- New version 2.3.34
- Drop link-ltdl-before-odbc patch (applied upstream)
- reenable meta-concurrency test as it doesnt chase referrals anymore
  (according to hyc)
- New version 2.3.33
- Fix issue with back-meta not working (by linking to ltdl before odbc)

* Fri Jan 05 2007 Buchan Milne <bgmilne@mandriva.org> 2.3.32-1mdv2007.1
+ Revision: 104331
-New version 2.3.32
-Post-2.3.31 fixes:
- ACL set memory leak(#4780)
- syncrepl shutdown hang (#4790)
- values return filter control leak(ITS#4794)
- Debug typo (ITS#4784)
-Add additional password modules from contrib (pw-netscape tested and working)
-Add acl-posixgroup from contrib (not tested yet)

* Wed Dec 20 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.31-1mdv2007.1
+ Revision: 100520
-New version 2.3.31
-ACL set memory leak patch from HEAD (ITS#4780)
- revert unnecessary libification of unixODBC-devel buildrequire

* Tue Nov 14 2006 Andreas Hasenack <andreas@mandriva.com> 2.3.30-1mdv2007.1
+ Revision: 84112
- fixed odbc buildrequires
- updated to verison 2.3.30

* Sat Nov 11 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.29-1mdv2007.0
+ Revision: 81603
- new version 2.3.29

  + Andreas Hasenack <andreas@mandriva.com>
    - we don't necessarily have libsasl-devel installed on the host that
      builds the .src.rpm or parses it (-q --specfile ...)
    - updated to version 2.3.28

* Thu Aug 24 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.27-1mdv2007.0
+ Revision: 57726
- New version 2.3.27
- Import openldap

* Wed Aug 16 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.25-1mdv2007.0
- 2.3.25
- init script: use subsys file named after process (fixes status), 
  fix status check in recover

* Thu Jul 13 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.24-3mdv2007.0
- include patch for ITS4589
- dont use wildcards in files list (some old versions of rpm dont like that)

* Wed Jul 12 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.24-2mdv2007.0
- apply file size limits during start (set in /etc/sysconfig/ldap)
- fix modulepath in slapd.conf on biarch platforms (#23400)
- put the ldapi socket in a more sensible place, /var/run/ldap/ldapi (#22420)
- use slapd -VV, not slapd -V (which starts slapd too) for version check,
  fixes #19245.
- allow setting the maximum file descriptor limit in slapd at compile time,
  use --define 'openldap_fd_setsize 8192' or similar.
- update samba.schema

* Wed Jun 07 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.24-1mdv2007.0
- New release 2.3.24
- only disable linuxthreads check on cooker
- update ldap-hot-db-backup to remove old archived transaction logs (after
  7 days by default)
- install cron symlinks for ldap-hot-db-backup, and adjust it for this
- fix ppolicy issues (ITS4576)

* Fri May 19 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.23-1mdk
- New release 2.3.23

* Wed May 03 2006 Buchan Milne <bgmilne@mandriva.org> 3.2.21-2mdk
- add patches for ITSs 4499, 4500, 4503, 4504, 4512, 4513, and a slurpd 
  potential overflow from Quanahs page

* Fri Apr 28 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.21-1mdk
- New release 2.3.21
- merge fixes from CS4 branch:
  - added patch to fix password policy control value
  - enabled spasswd (fixes #21753)
  - added indexes for syncprov replication
  - updated samba schema file with what is provided in samba 3.0.21c
  - added sample index line for when using syncprov
  - fixed #21066 (limits must be in database section)
- fix ldap-common to only consider bdb and hdb (not ldbm)

* Mon Feb 20 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.20-1mdk
- New release 2.3.20

* Thu Jan 26 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.19-1mdk
- New release 2.3.19

* Wed Jan 18 2006 Buchan Milne <bgmilne@mandriva.org> 2.3.18-1mdk
- New release 2.3.18

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 2.3.13-3mdk
- convert parallel init to LSB

* Mon Jan 02 2006 Olivier Blin <oblin@mandriva.com> 2.3.13-2mdk
- parallel init support

* Thu Dec 01 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.13-1mdk
- 2.3.13
- run recovery by default again
- disable meta-concurrency test for now

* Tue Nov 22 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.12-1mdk
- 2.3.12
- no-transaction patch no longer necessary, drop db-4.2.52-6mdk requirement
- drop patches from cvs
- fix quoting of urls in init script (#19911)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.3.11-7mdk
- rebuilt against openssl-0.9.8a

* Wed Nov 02 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.11-6mdk
- ITS 4108 -  thread crash, fix from CVS

* Sat Oct 29 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.11-5mdk
- fix logrotate (including for non-system case)

* Thu Oct 27 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.11-4mdk
- fix init script

* Thu Oct 27 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.11-3mdk
- fix slaptest modification in initscript in non-system case

* Thu Oct 27 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.11-2mdk
- fixes to scripts (put all backups under one place, handle empty suffix)
- check configuration file in init script before restarting, and add
  check option (and force-restart if you really want to kill your slapd)

* Sat Oct 15 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.11-1mdk
- 2.3.11
- provide means to build without epoll (--without epoll)
- drop p100

* Wed Oct 12 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.9-2mdk
- disable epoll when building for distributions with a 2.4 kernel
- fix lib require for non-system case

* Tue Oct 11 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.9-1mdk
- 2.3.9
- test041 is disabled upstream
- ITS 4035 - rootdn incorrect in cn=config backend/database (Andreas)

* Fri Oct 07 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.3.8-1mdk
- New release 2.3.8
- drop upstream patches (p100-102)
- openldap (since 2.3.7) includes up-to-date libtool, ensure we keep it on
  older distros (and no longer patch it in etc)
- only run tests for bdb backend by default (--define 'tests all' to run all)
- test041 seems broken

* Wed Sep 28 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.7-1mdk
- ITS 3989 fix ID used for syncprov_findbase (p100)
- fix rwm-2.3.so.0: undefined symbol: rewrite_info_init (p101)
- ITS 4020 slapd dies with empty uniqueMember attributes (p102)
- fix database dir for build on RH

* Tue Sep 20 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.6-4mdk
- rework init script so permissions checking (which was only called during 
  recovery) is done by default again (#16518), and add "recover" option to handle
  recovery sanely

* Sat Sep 17 2005 Buchan Milne <bgmilne@mandriva.org> 2.3.6-3mdk
- check slapd version to avoid unnecessary export/import
- fix typo in previous change to init script
- add acl for sambaDomain to slapd.access.conf
- add some more slapd.conf examples (load overlays, limits for syncrepl)

* Thu Sep 15 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.3.6-2mdk
- hacks for clean building on other/older distros (mdk10.0, fc1->rhel4)
- fix test for db4_internal case
- return correct exit codes in init script

* Tue Aug 30 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.3.6-1mdk
- conflict with kolab with broken template slapd.conf

- Sun Aug 28 2005 Oden Eriksson <oeriksson@mandriva.com>
  - fixed one %%lib/%%{_lib} error
  - make the devel sub package conflict with libldap2.2_7-devel
- Mon Aug 22 2005 Buchan Milne <bgmilne@linux-mandrake.com>
  - 2.3.6
  - drop p3 (sent upstream)
  - use BerkelyDB4.2 patch from source distribution
  - update docs from CVS, and add Mandriva section (re-used for README.mdk)
  - test and update migration from previous versions with db migration

* Tue Aug 09 2005 Buchan Milne <bgmilnelinux-mandrake.com> 2.3.4-4mdk
- fixes from Christiaan Welvaart <cjw@daneel.dyndns.org> allowing building
  with openldap-devel installed:
  - use new libtool and autotools
  - disable parallel make (make depend fails with icecream)

* Wed Aug 03 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.3.4-3mdk
- fix build with db4.3 run-time library present
- build with system db4.2 on 2006 and later

* Thu Jul 21 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.3.4-2mdk
- dont run db_recover in scriptlets or init script, not only is it
  unnecessary, it can prevent startup
- update/sync configure options
- update built-in db4.2 for the db4_internal case (and default to it for now)
- ship overlays from contrib too (smbk5pwd)

* Wed Jun 22 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.3.4-1mdk
- 2.3.4
- drop patches included upstream (p20, p21)

* Wed Jun 22 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.27-2mdk
- init script fixes
  - fix ownership of database directories (#16518)
  - ease translations (inspired by #16491)
  - factorise use of user to run slurpd and db tools (also in rpm scriptlets)
  - enable SSL if SLAPDURLLIST is not set and we have certs
- fixes in preparation for openldap2.3
  - macro-ize more hardcoded versions

* Sat Jun 18 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.27-1mdk
- New release 2.2.27
- drop migration subpackage (which will be packaged seperately)
- move 'make test' to %%check

* Fri Jun 10 2005 Andreas Hasenack <andreas@mandriva.com> 2.2.24-4mdk
- added account objectclass to migration tools when EXTENDED_SCHEMA is not
  being used (#15499)
- added preserve patch for migrationtools so that the temporary ldif file used
  during the import is not removed in the event of an error

* Thu Jun 02 2005 Andreas Hasenack <andreas@mandriva.com> 2.2.24-3mdk
- restart in %%pre and %%post has to deal with locales other than english
- rebuilt with newer sasl (2.1.22)

* Fri Apr 22 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.2.24-2mdk
- fix smbk5pwd build:
  - fix Patch20: use libtool archives in build dir for libldap_r and liblber
  - build openldap first so these archives are available

* Tue Apr 19 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.24-1mdk
- 2.2.24
- update qmail schema (Tibor Pittich)
- buildconflicts with libdb4.3

* Thu Apr 07 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.2.23-5mdk
- add -fPIC to cflags for librewrite to fix build on amd64
- fix deps

* Sat Apr 02 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.23-4mdk
- add conflict for devel package to allow upgrade (#14536)
- require the version of sasl we built against in post (#15056)
- dont use attributes in slapd.access.conf that were not available in
  default schemas before to not break upgrade (#15056)
- build with modules, but not in seperate packages (fixes upgrade with 
  module packages installed)
- handle databases defined in included files (fix upgrade for Kolab)
- allow disabling of database recovery at startup
- ship smbk5passwd module from cvs (p20), and make it work right (p21)
- disable parallel build (breaks building with modules)
- build against system db4.2 again
- only backup to ldif once for upgrade

* Mon Feb 07 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.23-3mdk
- sync slapd.access.conf with version from openldap2.2 package
- unmark slapd.access.conf as noreplace, and warn the user to this fact

* Fri Feb 04 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.23-2mdk
- fix typo in migration
- migrate data only once, even if the first failed
- fix libtool file fix
- provide backends when built without module support

* Wed Jan 26 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.23-1mdk
- 2.2.23
- fix changelog (from bad merge)
- version the guide source
- run make test once
- fix migration (should migrate all ldbm or bdb database defined in slapd.conf)

* Fri Jan 21 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.20-3mdk
- buildconflicts with older openldap-devel, so we don't link to parts
  of it in the devel package
- be able to disable tests (via --without test)
- fix typo in Contacts ACL
- add changelog for distro-specific release

* Wed Jan 05 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.20-2mdk
- run make test in build
- build against system db4.2 on 10.1

* Tue Jan 04 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.20-1mdk
- 2.2.20
- fix default slurpd replica path when not system ldap (#12745)
- stop slurpd if it is running, even if we couldn't stop slapd (#12760)
- allow overriding of replica detection in the init script when starting
  slurpd, via STARTSLURPD in the sysconfig file (#11552)
- fix rpmlint summary-ended-with-dot
- fix requires for -migration
- build against internal db4.2, otherwise we segfault? (#12759)

* Thu Dec 23 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.19-3mdk
- really revert to db-4.2 (and enforce it now)
- fix conflict with system openldap (man pages)
- don't use attributes/objectclasses from obsolete samba2 schema in 
  slapd.access.conf

* Wed Dec 15 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.19-2mdk
- use mkrel (conditionally define it) for distribution specific release tag
- revert to db-4.2 until Sleepycat bug #11505 is fixed
- update ntlm patch (p53), and apply it now
- fix calls to slapd_db* when not system ldap
- allow build-time setting of system (--with-system)
- macro-ise db4 libname
- update docs (finally) and document how to do it

* Mon Nov 29 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.19-1mdk
- 2.2.19
- only do hostname-based release maths on i586 for now (and fix it too)
- drop p55 (final fix in upstream) and p54 (merged upstream)
- build against system db-4.3 on 10.2 and later

* Tue Nov 16 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.18-3mdk
- better db4.3 patch (Quanah's)
- memleak fixes from HEAD (Quanah's)
- use original samba.schema, samba2 schema is now obsolete (samba2 retired)
- rename -devel-static to -static-devel
- don't provide unversioned -develprovides when not system

* Wed Nov 10 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.18-2mdk
- build with internal db4.3
- ship db4 patches even if we don't build with internal db4

* Tue Oct 26 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.18-1mdk
- 2.2.18
- drop buildconflicts
- fix last few "parallel install" issues (also fixes #12199)
- fix build without system db4
- add distribution-specific release number

* Sat Oct 09 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.17-1mdk
- 2.2.17
- allow building as non-system, provision to alternativise (taken from samba)
  (syslog/logrotate config still needs fixing)

* Mon Aug 23 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.15-1mdk
- 2.2.15

* Mon Aug 02 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.29-6mdk
- slapd.init - only run recovery in start (don't destroy memory cache)
- rewrite of backup and reinitialise scripts
- slapd.conf, slapd.access.conf - better default ACLs
- add ldapns.schema, for migrating host attributes from "account" objectclass

* Fri Jun 18 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.1.29-5mdk
- change ldap.conf permissions to 644 so anyone can read the file. It's
  needed so Evolution and others can work.
- add autoconf2.5 and ed to buildrequires
- disable posix mutexes, this breaks setups with non-NPTL kernels,
  low-end processors (VIA, K6, P1), and User-Mode Linux
- use assembler mutexes whenever possible, since they're the fastest on
  Linux.

* Wed May 19 2004 Florin <florin@mandrakesoft.com> 2.1.29-4mdk
- fix the awk lines in the scripts

* Wed May 19 2004 Florin <florin@mandrakesoft.com> 2.1.29-3mdk
- add the ntlm.patch (required by fcrozat)

* Sat Apr 24 2004 Florin <florin@mandrakesoft.com> 2.1.29-2mdk
- add the forgotten dhcp.schema

* Sat Apr 03 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.29-1mdk
- 2.1.29 marked as stable
- drop patch 3
- add some example scripts for hot database backups / removal of old
  transaction logs.
- add schema for evolution, dnszone, sudo, dhcp, drop dns, cron (not valid,
  and never implemented)
- update ACLs to allow users to add contacts (ie via Evo).

* Thu Mar 25 2004 Florin <florin@mandrakesoft.com> 2.1.25-6mdk
- comment out the TLS_CACERT      /etc/ssl/cacert.pem line in ldap.conf
 the file doesn't exist anyway and it breaks the non TLS behaviour

* Wed Mar 24 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.25-5mdk
- db4.2.52.2
- fix replica uri support (patch from CVS/2.1.26/2.1.27)
- revert to using /etc/openldap/ldap.conf instead of /etc/ldap.conf (#4462)
- don't ship /var/run/ldap/openldap-slurpd
- merge fixes from amd64 branch (thanks Gwenole)
- set TMPDIR in init script to keep kerberos binds working after restart
  (Denis Havlik)
- better default slapd.access.conf and ldap.conf (don't require CA-signed certs)


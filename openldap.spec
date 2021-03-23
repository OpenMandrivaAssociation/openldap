# wine uses openldap
%ifarch %{x86_64}
%bcond_without compat32
%endif

#defaults
%define build_modules 1
%define build_nssov 1
%define build_smbk5pwd 1
%bcond_with check
%global build_sql 1
%global back_perl 0

%{?_with_modules: %global build_modules 1}
%{?_without_modules: %global build_modules 0}
%{?_with_nssov: %global build_nssov 1}
%{?_without_nssov: %global build_nssov 0}
%{?_with_smbk5pwd: %global build_smbk5pwd 1}
%{?_without_smbk5pwd: %global build_smbk5pwd 0}
%{?_without_SASL: %{expand: %%define _without_cyrussasl --without-cyrus-sasl}}
%{?_with_SASL: %{expand: %%define _with_cyrussasl --with-cyrus-sasl}}
%{!?_with_cyrussasl: %{!?_without_cyrussasl: %global _with_cyrussasl --with-cyrus-sasl}}
%{?_with_cyrussasl: %define _with_cyrussasl --with-cyrus-sasl}
%{?_without_cyrussasl: %define _without_cyrussasl --without-cyrus-sasl}
%{?_with_gdbm: %global db_conv dbb}
%{!?_with_gdbm: %global db_conv gdbm}
%{?_without_sql: %global build_sql 0}

%define api 2.4
%define major 2
%define fname ldap
%define libname %mklibname %{fname} %{api} %{major}
%define devname %mklibname %{fname} %{api} -d
%define lib32name %mklib32name %{fname} %{api} %{major}
%define dev32name %mklib32name %{fname} %{api} -d

# we want to use the default db version for each release, so as
# to make backport binary compatibles
# excepted for very old systems, where we use bundled db
%define dbver 5.2.0
%define dbutils db52-utils
%define dbutilsprefix db52_

%global clientbin ldapadd,ldapcompare,ldapdelete,ldapmodify,ldapmodrdn,ldappasswd,ldapsearch,ldapwhoami,ldapexop
%global serverbin slapd-addel,slapd-bind,slapd-modify,slapd-modrdn,slapd-read,slapd-search,slapd-tester,ldif-filter
%define serversbin slapadd,slapcat,slapd,slapdn,slapindex,slappasswd,slaptest,slurpd,slapacl,slapauth

#localstatedir is passed directly to configure, and we want it to be /var/lib
#define _localstatedir %{_var}/run
%define _libexecdir %{_sbindir}

Summary:	LDAP servers and sample clients
Name:		openldap
Version:	2.4.58
Release:	1
License:	Artistic
Group:		System/Servers
Url:		http://www.openldap.org
Source0:	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
Source12:	openldap-guide-2.4.tar.bz2
Source13:	README-openldap2.4.mdv
Source14:	ldap.service
Source15:	openldap.sysconfig
Source19:	gencert.sh
Source20:	ldap.logrotate
Source21:	slapd.conf
Source22:	DB_CONFIG
Source23:	ldap.conf
Source24:	slapd.access.conf
Source25:	ldap-hot-db-backup
Source26:	ldap-reinitialise-slave
Source27:	ldap-common
Source28:	coreschemas.conf
Source29:	extraschemas.conf
# Extended Schema
Source50:	printer.schema
Source51:	evoldap.schema
Source53:	sudo.schema
Source54:	mull.schema
Source55:	evolutionperson.schema
Source56:	dnszone.schema
Source57:	calendar.schema
Source100:	openldap-2.4-admin-guide-add-vendor-doc.patch
Source101:	vendor.sdf
Source102:	vendor-standalone.sdf
Source500:	ldap.tmpfiles.d
Source502:	ldap.sysusers.d


Patch0:		openldap-2.3.4-config.patch
Patch1:		openldap-2.0.7-module.patch
Patch2:		openldap-2.3-smbk5passwd-paths.patch
Patch3:		openldap-2.3.4-smbk5passwd-only-smb.patch
#Patch4:	openldap-2.4.25-contrib-makefiles-with-tests.patch
Patch5:		openldap-2.4.8-fix-lib-perms.patch
Patch6:		openldap-2.4.12-test001-check-slapcat.patch
# RH + PLD Patches
Patch15:	openldap-cldap.patch
# schema patch
Patch46:	openldap-2.0.21-schema.patch
Patch47:	openldap-2.4.12-change-dyngroup-schema.patch
Patch53:	openldap-ntlm.patch
#patches in CVS
# see http://www.stanford.edu/services/directory/openldap/configuration/openldap-build.html
# for other possibly interesting patches

# http://git.yoctoproject.org/cgit/cgit.cgi/meta-cloud-services/tree/recipes-support/openldap/openldap-2.4.39/libldap-symbol-versions.patch?h=master
# https://github.com/ValveSoftware/csgo-osx-linux/issues/1925
Patch54:	libldap-symbol-versions.patch

# for make test:
BuildRequires:	diffutils
BuildRequires:	groff
BuildRequires:	rpm-helper
BuildRequires:	perl
BuildRequires:	db52-devel >= %{dbver}
BuildRequires:	krb5-devel
%{?_with_cyrussasl:BuildRequires:	sasl-devel}
BuildRequires:	libltdl-devel
%if %build_sql
BuildRequires:	unixODBC-devel
%endif
%if %back_perl
BuildRequires:	perl-devel
%endif
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(com_err)
Requires:	setup
%if %{with compat32}
BuildRequires:	devel(libkrb5)
BuildRequires:	devel(libncurses)
BuildRequires:	devel(libssl)
BuildRequires:	devel(libcom_err)
BuildRequires:	devel(libltdl)
BuildRequires:	libcrypt-devel
%endif

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The suite includes a
stand-alone LDAP server (slapd) which is in the -servers package, libraries for
implementing the LDAP protocol (in the lib packages), and utilities, tools, and
sample clients (in the -clients package). The openldap binary package includes
only configuration files used by the libraries.

Install openldap if you need LDAP applications and tools.


%package config
Summary:	OpenLDAP confdir
Group:		Databases

%description config
OpenLDAP confdir
This package prepares directory structure for server configuration files and
for openldap-schema-* packages, the OpenLDAP schema file collection.
# --------------------------------------------------------------------------- #

%package schemas
Summary:	OpenLDAP schema files
Group:		Databases
Requires(pre): %{name}-config
Recommends:	openldap-schemas-heimdal
Recommends:	openldap-schemas-krb5
Recommends:	openldap-schemas-samba
Recommends:	openldap-schemas-dhcp
Recommends:	openldap-schemas-freeradius
Recommends:	openldap-schemas-nfs
Recommends:	openldap-schemas-webmin
Recommends:	openldap-schemas-pureftpd
Recommends:	openldap-schemas-quota
Recommends:	openldap-schemas-sendmail
Recommends:	openldap-schemas-evoldap
Recommends:	openldap-schemas-extra

%description schemas
OpenLDAP schema files
This package contains standard set of OpenLDAP schema files. Supplementary
schema definitions (Heimdal, krb5, etc.) may be added up to this collection,
see 'dnf search openldap-schemas' for full list.
# --------------------------------------------------------------------------- #
%package schemas-extra
# A successor to "openldap-extra-schemas" package which was not updated for a
# number of years. This one should be kept as thin as possible as it can only be
# updated manually. Use of openldap-schemas-%{name} packages is preferrable.
# IMPORTANT: it should not obsolete and trigger removal of "openldap-extra-schemas"
# at list till 2016 as removal of "openldap-extra-schemas" could ruin someones's
# production environment.
Summary:	OpenLDAP extra schema files
Group:		Databases
Requires(pre): %{name}-config

%description schemas-extra
OpenLDAP extra schema files
A set of extra OpenLDAP schema files,
see 'urpmq -aS openldap-schemas' for full list.
# --------------------------------------------------------------------------- #

%package servers
Summary:	OpenLDAP servers and related files
Group:		System/Servers
Requires(pre,post,preun):	rpm-helper >= 0.23
Requires(pre,post,preun):	%{dbutils}
# slapd checks at startup if the library version matches exactly what it
# was compiled against, so we cant allow newer versions, e.g.:
#bdb_back_initialize: BDB library version mismatch: expected Berkeley DB 4.8.26: (December 30, 2009), got Berkeley DB 4.8.30: (March 25, 2011)
# This might need to be changed to a library dependency, but we need to verify
# library provides on multiple distros before doing that
Requires:	%{dbutils} >= %{dbver}
Requires:	%{name}-extra-schemas >= 1.3-7
Requires(pre):	%{name}-extra-schemas >= 1.3-7
Requires(post):	openssl

%description servers
OpenLDAP Servers.

This package contains the OpenLDAP server, slapd (LDAP server), additional
backends, configuration files, schema definitions required for operation, and
database maintenance tools

This server package was compiled with support for the following database
library: %{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}


%package clients
Summary:	OpenLDAP clients and related files
Group:		System/Servers

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

%package -n %{devname}
Summary:	OpenLDAP development libraries and header files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}ldap2.4_2-devel
Obsoletes:	%{_lib}ldap2.4_2-static-devel

%description -n %{devname}
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
LDAP clients.

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	OpenLDAP libraries (32-bit)
Group:		System/Libraries
Requires:	%{name}

%description -n %{lib32name}
This package includes the libraries needed by ldap applications.

%package -n %{dev32name}
Summary:	OpenLDAP development libraries and header files (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
LDAP clients.
%endif

%prep
%autosetup -p1

for f in config.guess config.sub ; do
    test -f /usr/share/libtool/config/$f || continue
    find . -type f -name $f -exec cp /usr/share/libtool/config/$f \{\} \;
done

perl -pi -e 's/^(#define\s+DEFAULT_SLURPD_REPLICA_DIR.*)ldap(.*)/${1}ldap${2}/' servers/slurpd/slurp.h
perl -pi -e 's/LDAP_DIRSEP "run" //g' include/ldap_defaults.h

# patches from CVS
perl -pi -e 's/testrun/\${TESTDIR}/g' tests/scripts/test024-unique

# README:
cp %{SOURCE13} README.mdk

# test048 has timing issues
mv tests/scripts/{,broken}test048*
# test049 not ready for not writing to testdir ...
mv tests/scripts/{,broken}test049*

chmod a+rx tests/scripts/test054*
libtoolize
aclocal --force --install -I m4
autoconf -f
autoheader -f

%build
PATH=$(echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g')
%serverbuild

# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=$(echo $CFLAGS|sed -e 's|-fPIE||g')
CXXFLAGS=$(echo $CXXFLAGS|sed -e 's|-fPIE||g')

# don't choose db4.3 even if it is available
export ol_cv_db_db_4_dot_3=no

#rh only:
export CPPFLAGS="-I%{_prefix}/kerberos/include $CPPFLAGS"
export LDFLAGS="-L%{_prefix}/kerberos/%{_lib} $LDFLAGS"
%if %{?openldap_fd_setsize:1}%{!?openldap_fd_setsize:0}
CPPFLAGS="$CPPFLAGS -DOPENLDAP_FD_SETSIZE=%{openldap_fd_setsize}"
%endif

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--with-subdir=%{name} \
	--localstatedir=/var/run/ldap \
	--enable-dynamic \
	--enable-syslog \
	--enable-proctitle \
	--enable-ipv6 \
	--enable-local \
	--with-threads \
	--with-tls \
	--disable-slapd \
	--enable-aci \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
%if %build_modules
	--enable-modules \
%endif
	--enable-rewrite \
	--enable-rlookups \
	--disable-wrappers \
	--enable-bdb=no \
	--enable-hdb=yes \
	--enable-lmdb=yes \
	--enable-ndb=no \
	--enable-backends=mod \
	--disable-perl \
%if %build_sql
	--enable-sql=mod \
%else
	--enable-sql=no \
%endif
	--enable-overlays=mod \
	--enable-shared
%make_build
cd ..
%endif

# FIXME glibc 2.8 breakage, this is not the correct fix, see
# http://www.openldap.org/its/index.cgi/Build?id=5464;selectid=5464
CPPFLAGS="$CPPFLAGS -D_GNU_SOURCE"

%configure \
	--disable-static \
	--with-subdir=%{name} \
	--localstatedir=/var/run/ldap \
	--enable-dynamic \
	--enable-syslog \
	--enable-proctitle \
	--enable-ipv6 \
	--enable-local \
	%{?_with_cyrussasl} %{?_without_cyrussasl} \
	--with-threads \
	--with-tls \
	--enable-slapd \
	--enable-aci \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
	%{!?_with_gssapi:--without-gssapi} \
	%{?_with_cyrussasl:--enable-spasswd} \
%if %build_modules
	--enable-modules \
%endif
	--enable-rewrite \
	--enable-rlookups \
	--disable-wrappers \
	--enable-bdb=no \
	--enable-hdb=yes \
	--enable-lmdb=yes \
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

# (oe) amd64 fix
perl -pi -e "s|^AC_CFLAGS.*|AC_CFLAGS = $CFLAGS -fPIC|g" libraries/librewrite/Makefile

%make_build depend
%make_build
export LIBTOOL=$(pwd)/libtool

if [ -d /usr/kerberos/%{_lib} ]; then export LIBRARY_PATH=/usr/kerberos/%{_lib}; fi
sed -i -e 's/pw-radius.la//g' contrib/slapd-modules/passwd/Makefile

#acl broken
for i in addpartial allop allowed autogroup cloak denyop dsaschema dupent  \
	kinit \
	lastbind lastmod noopsrch nops \
%if %{build_nssov}
	nssov \
%endif
%if %{build_smbk5pwd}
	smbk5pwd \
%endif
	passwd passwd/sha2 trace
do
	make -C contrib/slapd-modules/$i libdir=%{_libdir} moduledir=%{_libdir}/%{name}
done

%check
%if %{with check}
# Use a pseudo-random number between 9000 and 10000 as base port for slapd in tests
export SLAPD_BASEPORT=$[9000+RANDOM%1000]
make -C tests %{!?tests:test}%{?tests:%tests}
%endif

%install
export DONT_GPRINTIFY=1
export DONT_REMOVE_LIBTOOL_FILES=1
for i in acl addpartial allop allowed autogroup \
 kinit \
%if %{build_nssov}
	nssov \
%endif
%if %{build_smbk5pwd}
	smbk5pwd \
%endif
	passwd
do
[ -e contrib/slapd-modules/$i/README ] && cp -af contrib/slapd-modules/$i/README{,.$i}
done
cp contrib/slapd-modules/passwd/sha2/README{,.sha2}
rm -Rf %{buildroot}

%if %{with compat32}
%make_install -C build32 STRIP=""
%endif

%make_install STRIP=""

%if %{build_smbk5pwd}
cp -a contrib/slapd-modules/smbk5pwd/.libs/smbk5pwd.so* %{buildroot}/%{_libdir}/%{name}
for i in %{buildroot}/%{_libdir}/%{name}/smbk5pwd*
do
  if [ -L ${i} ]
  then
	newlink=$(readlink $i|sed -e 's/k5//g')
	rm $i
	ln -svf $newlink ${i/k5/}
  else
	mv $i ${i/k5/}
  fi
done
%endif

cp contrib/slapd-modules/allop/slapo-allop.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/cloak/slapo-cloak.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/lastbind/slapo-lastbind.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/lastmod/slapo-lastmod.5 %{buildroot}/%{_mandir}/man5
cp contrib/slapd-modules/nops/slapo-nops.5 %{buildroot}/%{_mandir}/man5

#smbk5pwd skipped, installed as smbpwd above
#dsaschema broken on 32bit
for i in addpartial allop allowed autogroup cloak denyop dupent \
	kinit \
	lastbind lastmod noopsrch nops \
%if %{build_nssov}
	nssov \
%endif
	passwd passwd/sha2 trace
do
	if grep -qE '^test:' contrib/slapd-modules/$i/Makefile; then
		if make -C contrib/slapd-modules/$i test; then
			make DESTDIR=%{buildroot} mandir=%{_mandir} moduledir=%{_libdir}/%{name} schemadir=%{_sysconfdir}/%{name}/schema -C contrib/slapd-modules/$i install
			rm -f %{buildroot}/%{_libdir}/%{name}/$i.a
		else
			exit 1
		fi
	fi
done
rm -f %{buildroot}/%{_libdir}/%{name}/kerberos.a
rm -f %{buildroot}/%{_libdir}/%{name}/netscape.a
rm -f %{buildroot}/%{_libdir}/%{name}/sha2.a

#compat symlinks, DONT REMOVE
ln -s netscape.so %{buildroot}/%{_libdir}/%{name}/pw-netscape.so
ln -s kerberos.so %{buildroot}/%{_libdir}/%{name}/pw-kerberos.so

# try and ship the tests such that they will run properly
install -d %{buildroot}/%{_datadir}/%{name}/tests
cp -a tests/{data,scripts,Makefile,run} %{buildroot}/%{_datadir}/%{name}/tests
ln -s %{_datadir}/%{name}/schema %{buildroot}/%{_datadir}/%{name}/tests
find %{buildroot}/%{_datadir}/%{name}/tests -type f -name '*.conf' -exec perl -pi -e 's,\.\.\/servers\/slapd\/back-.*,%{_libdir}/%{name},g;s,\.\.\/servers\/slapd\/overlays,%{_libdir}/%{name},g' {} \;
perl -pi -e 's,(\`pwd\`\/)?\.\.\/servers\/(slapd|slurpd)\/(slapd|slurpd),%{_sbindir}/${2},g;s,^PROGDIR=.*,PROGDIR=%{_bindir},g;s,^CLIENTDIR=.*,CLIENTDIR=%{_bindir},g;s,^TESTDIR=.*,TESTDIR=\${USER_TESTDIR-\$TMPDIR/openldap-testrun},g;s/ldap(search|add|delete|modify|whoami|compare|passwd|modrdn|exop)/ldap${1}/g;s/slapd-tester$/slapd-tester/g;s,\$TESTWD\/,,g;s/^(\.\*.*)\$(.*)/${1}\`pwd\`\/\$${2}/g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/defines.sh %{buildroot}/%{_datadir}/%{name}/tests/run
perl -pi -e 's/testrun/\$TESTDIR/g;s,^SHTOOL=.*,. scripts/defines.sh,g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/all
perl -p -i.bak -e 's,^olcModulePath: .*,olcModulePath: %{_libdir}/%{name},g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/test*
perl -pi -e 's/^(Makefile|SUBDIRS)/#$1/g' %{buildroot}/%{_datadir}/%{name}/tests/Makefile
echo 'SHTOOL="./scripts/shtool"' >> %{buildroot}/%{_datadir}/%{name}/tests/scripts/defines.sh
install -m755 build/shtool %{buildroot}/%{_datadir}/%{name}/tests/scripts
if [ -n "" ]
then for i in addel bind modify modrdn read search tester
do ln -sf slapd-${i} tests/progs/slapd-${i}
done
fi
ln -s %{_datadir}/%{name}/tests/data %{buildroot}/%{_datadir}/%{name}/tests/testdata

install -m755 tests/progs/.libs/slapd-* tests/progs/.libs/ldif-filter %{buildroot}/%{_bindir}

### some hack
perl -pi -e "s| -L../liblber/.libs||g" %{buildroot}%{_libdir}/libldap.la

perl -pi -e  "s,-L$RPM_BUILD_DIR\S+%{_libdir},,g" %{buildroot}/%{_libdir}/lib*.la

### Init scripts
install -d %{buildroot}%{_unitdir}
install -m644 %{SOURCE14} %{buildroot}%{_unitdir}/ldap.service

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE15} %{buildroot}%{_sysconfdir}/sysconfig/ldap

install -m 640 %{SOURCE21} %{SOURCE23} %{SOURCE24} %{buildroot}%{_sysconfdir}/%{name}

install -d %{buildroot}/%{_sysconfdir}/%{name}/slapd.d
install -m 640 %{SOURCE28} %{buildroot}%{_sysconfdir}/%{name}/slapd.d/coreschemas.conf
install -m 640 %{SOURCE29} %{buildroot}%{_sysconfdir}/%{name}/slapd.d/extraschemas.conf

### repository dir
install -d %{buildroot}%{_var}/lib/ldap

### DB_CONFIG for bdb backend
install -m644 %{SOURCE22} %{buildroot}%{_var}/lib/ldap

### run dir
install -d %{buildroot}%{_var}/run/ldap

### Server defaults
echo "localhost" > %{buildroot}%{_sysconfdir}/%{name}/ldapserver

### we don't need the default files
rm -f %{buildroot}/etc/%{name}/*.default 
rm -f %{buildroot}/etc/%{name}/*.example 
rm -f %{buildroot}/etc/%{name}/schema/*.default 
rm -f %{buildroot}/etc/%{name}/slapd.ldif

### Previous versions of this package held core schema files in {_datadir}/{name}/schema/. We have to keep
### these files in place at least till 2016 so that upgrades do not break existing installations.
install -d %{buildroot}%{_datadir}/%{name}/schema
cp %{buildroot}%{_sysconfdir}/%{name}/schema/*.{schema,ldif} %{buildroot}%{_datadir}/%{name}/schema/
# This one is an exception as it conflicts with 'openldap-extra-schemas'
mv %{buildroot}%{_sysconfdir}/%{name}/schema/README %{buildroot}%{_sysconfdir}/%{name}/schema/README.coreschemas

### install additional schemas

install -m 644 %{SOURCE54} %{buildroot}%{_datadir}/%{name}/schema/
install -m 644 %{SOURCE50} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE51} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE52} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE53} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE54} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE55} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE56} %{buildroot}%{_sysconfdir}/%{name}/schema/
install -m 644 %{SOURCE57} %{buildroot}%{_sysconfdir}/%{name}/schema/

### install additional schemas
install -m 644 %{SOURCE54} %{buildroot}%{_datadir}/%{name}/schema/

install -d %{buildroot}/%{_datadir}/%{name}/scripts
install -m 755 %{SOURCE25} %{SOURCE26} %{SOURCE27} %{buildroot}/%{_datadir}/%{name}/scripts/
for i in hourly daily weekly monthly yearly
do
	install -d %{buildroot}/%{_sysconfdir}/cron.${i}
	ln -s %{_datadir}/%{name}/scripts/ldap-hot-db-backup %{buildroot}/%{_sysconfdir}/cron.${i}/ldap-hot-db-backup
done
perl -pi -e 's,%{_bindir}/db_,%{_bindir}/%{dbutilsprefix},g' %{buildroot}/%{_datadir}/%{name}/scripts/ldap-common

### create local.schema
# echo "# This is a good place to put your schema definitions " > %{buildroot}%{_sysconfdir}/%{name}/schema/local.schema
# chmod 644 %{buildroot}%{_sysconfdir}/%{name}/schema/local.schema

### Guide
mkdir -p %{buildroot}/%{_docdir}/
tar xvjf %{SOURCE12} -C %{buildroot}/%{_docdir}/
mv %{buildroot}/%{_docdir}/{%{name},%{name}}-guide ||:

### gencert.sh
install -m 755 %{SOURCE19} %{buildroot}/%{_datadir}/%{name}

### log repository
install -m 700 -d %{buildroot}/var/log/ldap
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/logrotate.d/ldap

# get the buildroot out of the man pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

#Fix binary names and config paths in scripts/configs
perl -pi -e 's,/%{name}/,/%{name}/,g;s,(/ldap\w?)\b,${1},g;s,(%{_bindir}/slapd_db_\w+),${1},g;s,(%{_sbindir}/sl(apd|urpd|aptest))\b,${1},g;s/ldap-common/ldap-common/g;s,ldap.pem,ldap.pem,g;s,/usr/lib,%{_libdir},g' %{buildroot}/{%{_sysconfdir}/%{name}/slapd.conf,%{_initrddir}/ldap,%{_datadir}/%{name}/scripts/*}

perl -pi -e 's/ldap/ldap/' %{buildroot}/%{_sysconfdir}/logrotate.d/ldap

mv %{buildroot}/var/run/ldap/openldap-data/DB_CONFIG.example %{buildroot}/%{_var}/lib/ldap/

# install private headers so as to build additional overlays later
install -d -m 755 %{buildroot}%{_includedir}/%{name}/{include,slapd}
install -m 644 include/*.h  %{buildroot}%{_includedir}/%{name}/include
install -d -m 755 %{buildroot}%{_includedir}/%{name}/include/ac
install -m 644 include/ac/*.h  %{buildroot}%{_includedir}/%{name}/include/ac
install -m 644 servers/slapd/*.h  %{buildroot}%{_includedir}/%{name}/slapd
install -d -m 755 %{buildroot}%{_includedir}/%{name}/libraries/liblunicode/ucdata
install -m 644 libraries/liblunicode/ucdata/*.h %{buildroot}%{_includedir}/%{name}/libraries/liblunicode/ucdata

%if %{with compat32}
# Deal with headers that differ between 32-bit and 64-bit builds
cd build32/include
for i in *.h; do
	mv %{buildroot}%{_includedir}/openldap/include/$i %{buildroot}%{_includedir}/openldap/include/${i/.h/-64.h}
	cp $i %{buildroot}%{_includedir}/openldap/include/${i/.h/-32.h}
	cat >%{buildroot}%{_includedir}/openldap/include/$i <<EOF
#ifdef __i386__
#include "${i/.h/-32.h}"
#else
#include "${i/.h/-64.h}"
#endif
EOF
done
cd ../..
%endif


rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/%{name}/*.la
%if %{with compat32}
rm -f %{buildroot}/%{_prefix}/lib/*.la
rm -f %{buildroot}%{_prefix}/lib/%{name}/*.la
%endif

# tmpfiles
install -m 0644 %{SOURCE500} -D %{buildroot}%{_tmpfilesdir}/ldap.conf
# sysusers.d
install -m 0644 %{SOURCE502} -D %{buildroot}%{_sysusersdir}/ldap.conf

%pre servers
%_pre_useradd ldap %{_var}/lib/ldap /bin/false
%_pre_groupadd ldap ldap
# allowing slapd to read hosts.allow and hosts.deny
%{_bindir}/gpasswd -a ldap adm 1>&2 > /dev/null || :

if [ "$1" -ne '1' ]
then
SLAPD_STATUS=$(LANG=C LC_ALL=C NOLOCALE=1 service ldap status 2>/dev/null|grep -q stopped;echo $?)
[ $SLAPD_STATUS -eq 1 ] && service ldap stop
service ldap recover

LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}

#decide whether we need to migrate at all:
MIGRATE=$(%{_sbindir}/slapd -VV 2>&1|while read a b c d e;do case $d in (2.4.*) echo nomigrate;;(2.*) echo migrate;;esac;done)

if [ "$1" -ne 1 -a -e "$SLAPDCONF" -a "$MIGRATE" != "nomigrate" ]
then
#`awk '/^[:space:]*directory[:space:]*\w*/ {print $2}' /etc/%{name}/slapd.conf`
dbs=$(awk 'BEGIN {OFS=":"} /[[:space:]]*^database[[:space:]]*\w*/ {db=$2;suf="";dir=""}; /^[[:space:]]*suffix[[:space:]]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm"||db=="hdb")&&(suf!=""&&dir!="")) print dir,suf};/^[[:space:]]*directory[[:space:]]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm"||db="hdb")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g')
for db in $dbs
do
	dbdir=${db/:*/}
	dbsuffix=${db/*:/}
	[ -e /etc/sysconfig/ldap ] && . /etc/sysconfig/ldap
# data migration between incompatible versions
# openldap >= 2.2.x have slapcat as a link to slapd, older releases do not
	if [ "${AUTOMIGRATE:-yes}" == "yes" -a -f %{_sbindir}/slapcat ]
	then
		ldiffile="rpm-migrate-to-%{api}.ldif"
		# dont do backups more than onc
		if [ ! -e "${dbdir}/${ldiffile}-imported" -a ! -e "${dbdir}/${ldiffile}-import-failed" ];then
		echo "Migrating pre-OpenLDAP-%{api} data"
		echo "Making a backup of $dbsuffix to ldif file ${dbdir}/$ldiffile"
		# For some reason, slapcat works in the shell when slapd is
		# running but not via rpm ...
		slapcat -b "$dbsuffix" -l ${dbdir}/${ldiffile} ||:
		fi
	fi
done
fi

# We want post to start the service, but we dont want to start
# it now to create a new database environment in case of db library upgrade
touch /var/lock/subsys/slapd
fi



%pre config
%sysusers_create_package ldap %{SOURCE502}

%post config
%tmpfiles_create ldap.conf

%post servers
SLAPD_STATUS=$(LANG=C LC_ALL=C NOLOCALE=1 service ldap status 2>/dev/null|grep -q stopped;echo $?)
[ $SLAPD_STATUS -eq 1 ] && service ldap stop
# bgmilne: part 2 of gdbm->dbb conversion for data created with
# original package for 9.1:
dbnum=1
LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}
if [ -e "$SLAPDCONF" ]
then
dbs=$(awk 'BEGIN {OFS=":"} /[[:space:]]*^database[[:space:]]*\w*/ {db=$2;suf="";dir=""}; /^[[:space:]]*suffix[[:space:]]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};/^[[:space:]]*directory[[:space:]]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g')
for db in $dbs
do
	dbdir=${db/:*/}
	dbsuffix=${db/*:/}
	ldiffile="rpm-migrate-to-%{api}.ldif"
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
		if slapadd -q -cv -b "$dbsuffix" -l ${dbdir}/${ldiffile} > \
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
			echo "# service ldap stop"
			echo "# slapadd -c -l ${dbdir}/${ldiffile}-import-failed"
			echo "# chown $LDAPUSER:$LDAPGROUP ${dbdir}/*"
			echo "# service ldap start"
		fi
	fi

	chown ${LDAPUSER}:${LDAPGROUP} -R ${dbdir}
	# openldap-2.0.x->2.1.x on ldbm/dbb backend seems to need reindex regardless:
	#slapindex -n $dbnum
	#dbnum=$[dbnum+1]
done
fi
[ $SLAPD_STATUS -eq 1 ] && service ldap start

# Setup log facility for OpenLDAP on new install
%if %{?_post_syslogadd:1}%{!?_post_syslogadd:0}
%_post_syslogadd /var/log/ldap/ldap.log local4
perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"local4\"|" \
	%{_sysconfdir}/sysconfig/ldap
%else
if [ -f %{_sysconfdir}/syslog.conf -a $1 -eq 1 ]
then
	# clean syslog
	perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf

	# probe free local-users
	cntlog=""
	for log in 7 6 5 3 2 1 0 4
	do
		grep -vE "local${log}[^;]*\.none" %{_sysconfdir}/syslog.conf|grep -q local${log} || cntlog="${log}"
	done

	if [ "${cntlog}" != "" ];then
		echo "# added by %{name}-%{version} rpm $(date)" >> %{_sysconfdir}/syslog.conf
#   modified by Oden Eriksson
#		echo "local${cntlog}.*	   /var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf
		echo -e "local${cntlog}.*\t\t\t\t\t\t\t-/var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf

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
	perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"LOCAL${cntlog}\"|g" %{_sysconfdir}/sysconfig/ldap

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

%_post_service ldap

# nscd reset
if [ -f /var/lock/subsys/nscd ]; then
	service nscd restart  > /dev/null 2>/dev/null || :
fi


%preun servers
%_preun_service ldap

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
%{_mandir}/man5/ldap.conf.5*
%{_mandir}/man5/ldif.5*
%doc README.mdk

%files doc
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README
%doc doc/rfc doc/drafts
%doc %{_docdir}/%{name}-guide

%files config
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/schema
%dir %attr(750,ldap,ldap) %{_sysconfdir}/%{name}/slapd.d
%{_sysusersdir}/ldap.conf
%{_tmpfilesdir}/ldap.conf

%files schemas
%config(noreplace) %{_sysconfdir}/%{name}/schema/README.coreschemas
%config(noreplace) %attr(750,ldap,ldap) %{_sysconfdir}/%{name}/slapd.d/coreschemas.conf
%config(noreplace) %{_sysconfdir}/%{name}/schema/collective.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/collective.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/corba.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/corba.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/core.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/core.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/cosine.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/cosine.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/duaconf.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/duaconf.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/dyngroup.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/dyngroup.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/inetorgperson.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/inetorgperson.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/java.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/java.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/misc.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/misc.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/mull.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/nis.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/nis.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/openldap.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/openldap.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/pmi.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/pmi.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/ppolicy.ldif
%config(noreplace) %{_sysconfdir}/%{name}/schema/ppolicy.schema
%{_datadir}/%{name}/schema/collective.ldif
%{_datadir}/%{name}/schema/collective.schema
%{_datadir}/%{name}/schema/corba.ldif
%{_datadir}/%{name}/schema/corba.schema
%{_datadir}/%{name}/schema/core.ldif
%{_datadir}/%{name}/schema/core.schema
%{_datadir}/%{name}/schema/cosine.ldif
%{_datadir}/%{name}/schema/cosine.schema
%{_datadir}/%{name}/schema/duaconf.ldif
%{_datadir}/%{name}/schema/duaconf.schema
%{_datadir}/%{name}/schema/dyngroup.ldif
%{_datadir}/%{name}/schema/dyngroup.schema
%{_datadir}/%{name}/schema/inetorgperson.ldif
%{_datadir}/%{name}/schema/inetorgperson.schema
%{_datadir}/%{name}/schema/java.ldif
%{_datadir}/%{name}/schema/java.schema
%{_datadir}/%{name}/schema/misc.ldif
%{_datadir}/%{name}/schema/misc.schema
%{_datadir}/%{name}/schema/mull.schema
%{_datadir}/%{name}/schema/nis.ldif
%{_datadir}/%{name}/schema/nis.schema
%{_datadir}/%{name}/schema/openldap.ldif
%{_datadir}/%{name}/schema/openldap.schema
%{_datadir}/%{name}/schema/pmi.ldif
%{_datadir}/%{name}/schema/pmi.schema
%{_datadir}/%{name}/schema/ppolicy.ldif
%{_datadir}/%{name}/schema/ppolicy.schema

%files schemas-extra
%config(noreplace) %attr(750,ldap,ldap) %{_sysconfdir}/%{name}/slapd.d/extraschemas.conf
%config(noreplace) %{_sysconfdir}/%{name}/schema/printer.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/evoldap.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/calendar.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/dnszone.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/evolutionperson.schema
%config(noreplace) %{_sysconfdir}/%{name}/schema/sudo.schema


%files servers
%doc contrib/slapd-modules/acl/README.gssacl
%doc contrib/slapd-modules/addpartial/README.addpartial
%doc contrib/slapd-modules/allop/README.allop
%doc contrib/slapd-modules/allowed/README.allowed
%doc contrib/slapd-modules/autogroup/README.autogroup
%doc contrib/slapd-modules/kinit/README.kinit
%doc contrib/slapd-modules/passwd/README.passwd
%doc contrib/slapd-modules/passwd/sha2/README.sha2
%if %{build_smbk5pwd}
%doc contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%endif
%if %{build_nssov}
%doc contrib/slapd-modules/nssov/README.nssov
%endif
%dir %{_sysconfdir}/%{name}
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/%{name}/slapd.conf
%dir %attr(750,ldap,ldap) %{_sysconfdir}/%{name}/slapd.d
%attr(640,root,ldap) %config %{_sysconfdir}/%{name}/slapd.access.conf
%{_sysconfdir}/cron.hourly/ldap-hot-db-backup
%{_sysconfdir}/cron.daily/ldap-hot-db-backup
%{_sysconfdir}/cron.weekly/ldap-hot-db-backup
%{_sysconfdir}/cron.monthly/ldap-hot-db-backup
%{_sysconfdir}/cron.yearly/ldap-hot-db-backup
%config(noreplace) %{_sysconfdir}/logrotate.d/ldap
%config(noreplace) %{_sysconfdir}/sysconfig/ldap
%{_unitdir}/ldap.service
%{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so*
%{_datadir}/%{name}/gencert.sh
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/schema
%{_datadir}/%{name}/schema/*.schema
%{_datadir}/%{name}/schema/*.ldif
%{_datadir}/%{name}/scripts
%{_mandir}/man5/slap*.5*
%{_mandir}/man8/*
%attr(750,ldap,ldap) %dir /var/log/ldap
%attr(750,ldap,ldap) %dir %{_var}/lib/ldap
%config(noreplace) %{_var}/lib/ldap/DB_CONFIG
%{_var}/lib/ldap/DB_CONFIG.example
%attr(755,ldap,ldap) %dir /var/run/ldap

%files clients
%{_bindir}/ldap*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/lib*.so.*

%files -n %{devname}
%{_libdir}/libl*.so
%{_includedir}/l*.h
%{_includedir}/openldap.h
%{_includedir}/s*.h
%{_includedir}/%{name}
%{_mandir}/man3/*

%files tests
%{_datadir}/%{name}/tests

%files testprogs
%{_bindir}/slapd-*
%{_bindir}/ldif-filter

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/lib*.so.*

%files -n %{dev32name}
%{_prefix}/lib/libl*.so
%endif

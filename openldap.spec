# wine uses openldap
%ifarch %{x86_64}
%bcond_without compat32
%endif

%global _hardened_build 1
%define _disable_ld_no_undefined 1
%define _disable_lto 1

%global systemctl_bin /usr/bin/systemctl
%global check_password_version 1.1

%global so_ver 2
%global so_ver_compat 2

# When you change "Version: " to the new major version, remember to change this value too
%global major_version 2.6

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

%if %{cross_compiling}
# Workaround for libtool brokenness being unable to handle spaces
# in $CC (such as "clang -target whatever")
%define prefer_gcc 1
%endif

%define libname %mklibname ldap
%define lberlibname %mklibname lber
%define slapilibname %mklibname slapi
%define devname %mklibname -d ldap
%define compatname %mklibname ldap2.4
%define lib32name %mklib32name ldap
%define dev32name %mklib32name -d ldap

%bcond_without perl

Name: openldap
Version: 2.6.6
Release: 2
Summary: LDAP support libraries
License: OpenLDAP
URL: http://www.openldap.org/

Source0: https://openldap.org/software/download/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: slapd.service
Source2: slapd.tmpfiles
Source3: slapd.ldif
Source4: ldap.conf
Source5: UPGRADE_INSTRUCTIONS
Source10: https://github.com/ltb-project/openldap-ppolicy-check-password/archive/v%{check_password_version}/openldap-ppolicy-check-password-%{check_password_version}.tar.gz
Source50: libexec-functions
Source52: libexec-check-config.sh

# Patches for 2.6
Patch0: openldap-manpages.patch
Patch1: openldap-reentrant-gethostby.patch

Patch3: openldap-smbk5pwd-overlay.patch
Patch4: openldap-ai-addrconfig.patch
Patch5: openldap-allop-overlay.patch

# fix back_perl problems with lt_dlopen()
# might cause crashes because of symbol collisions
# the proper fix is to link all perl modules against libperl
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=327585
Patch6: openldap-switch-to-lt_dlopenadvise-to-get-RTLD_GLOBAL-set.patch

# System-wide default for CA certs
Patch7: openldap-openssl-manpage-defaultCA.patch
Patch8: openldap-add-export-symbols-LDAP_CONNECTIONLESS.patch

# check-password module specific patches
Patch90: check-password-makefile.patch
Patch91: check-password.patch

Patch200: openldap-2.6.6-clang16.patch
Patch201: openldap-2.6.6-compat-2.4.patch
# memcmp works on all OM targets, but detection
# doesn't work reliably when crosscompiling, so
# disable it
Patch202: openldap-2.6-cross.patch

BuildRequires: pkgconfig(libsasl2)
BuildRequires: locales-extra-charsets
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libltdl-devel
BuildRequires: pkgconfig(libevent)
BuildRequires: make
BuildRequires: pkgconfig(libcrypto)
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: unixODBC-devel

Requires: %{libname} = %{EVRD}
Requires: %{lberlibname} = %{EVRD}
Requires: %{slapilibname} = %{EVRD}

%if %{with compat32}
BuildRequires: devel(libkrb5)
BuildRequires: devel(libncurses)
BuildRequires: devel(libssl)
BuildRequires: devel(libcom_err)
BuildRequires: devel(libltdl)
BuildRequires: libcrypt-devel
%endif

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package -n %{libname}
Summary: Libraries for the OpenLDAP LDAP environment
Group: System/Libraries

%description -n %{libname}
Libraries for the OpenLDAP LDAP environment

%package -n %{lberlibname}
Summary: LBER libraries for the OpenLDAP LDAP environment
Group: System/Libraries

%description -n %{lberlibname}
LBER libraries for the OpenLDAP LDAP environment

%package -n %{slapilibname}
Summary: SLAPI libraries for the OpenLDAP LDAP environment
Group: System/Libraries

%description -n %{slapilibname}
SLAPI libraries for the OpenLDAP LDAP environment

%package -n %{devname}
Summary: LDAP development libraries and header files
Requires: openldap%{?_isa} = %{EVRD}
Requires: %{libname}%{?_isa} = %{EVRD}
Requires: %{lberlibname}%{?_isa} = %{EVRD}
Requires: %{slapilibname}%{?_isa} = %{EVRD}
Requires: pkgconfig(libsasl2)
%rename %mklibname -d ldap 2.4

%description -n %{devname}
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package -n %{compatname}
Summary: Package providing legacy non-threaded libldap
Requires: %{libname}%{?_isa} = %{EVRD}
Requires: %{lberlibname}%{?_isa} = %{EVRD}
Requires: %{slapilibname}%{?_isa} = %{EVRD}
%rename %mklibname ldap2.4 %{so_ver_compat}
# since libldap is manually linked from libldap_r, the provides is not generated automatically
%if "%_lib" == "lib"
Provides: libldap-2.4.so.%{so_ver_compat}
Provides: libldap_r-2.4.so.%{so_ver_compat}
Provides: liblber-2.4.so.%{so_ver_compat}
Provides: libslapi-2.4.so.%{so_ver_compat}
%else
Provides: libldap-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
Provides: libldap_r-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
Provides: liblber-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
Provides: libslapi-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
Provides: libldap-2.4.so.%{so_ver_compat}(OPENLDAP_2.4_2)(%{__isa_bits}bit)
Provides: libldap_r-2.4.so.%{so_ver_compat}(OPENLDAP_2.4_2)(%{__isa_bits}bit)
Provides: liblber-2.4.so.%{so_ver_compat}(OPENLDAP_2.4_2)(%{__isa_bits}bit)
%endif

%description -n %{compatname}
The %{compatname} package contains shared libraries named as libldap-2.4.so,
libldap_r-2.4.so, liblber-2.4.so and libslapi-2.4.so.
The libraries are just links to the current version shared libraries,
and are available for compatibility reasons.

%package servers
Summary: LDAP server
License: OpenLDAP
Requires: openldap%{?_isa} = %{EVRD}
Requires(pre): shadow-utils
BuildRequires: systemd
BuildRequires: cracklib-devel
# migrationtools (slapadd functionality):
Provides: ldif2ldbm
%{?systemd_requires}

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd server and related files.

%package clients
Summary: LDAP client utilities
Requires: openldap%{?_isa} = %{EVRD}

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

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
32-bit LDAP clients.
%endif

%prep
%autosetup -p1 -a 10
autoconf

# build smbk5pwd with other overlays
ln -s ../../../contrib/slapd-modules/smbk5pwd/smbk5pwd.c servers/slapd/overlays
mv contrib/slapd-modules/smbk5pwd/README contrib/slapd-modules/smbk5pwd/README.smbk5pwd
# build allop with other overlays
ln -s ../../../contrib/slapd-modules/allop/allop.c servers/slapd/overlays
mv contrib/slapd-modules/allop/README contrib/slapd-modules/allop/README.allop
mv contrib/slapd-modules/allop/slapo-allop.5 doc/man/man5/slapo-allop.5

mv servers/slapd/back-perl/README{,.back_perl}

# fix documentation encoding
for filename in doc/drafts/draft-ietf-ldapext-acl-model-xx.txt; do
  iconv -f iso-8859-1 -t utf-8 "$filename" > "$filename.utf8"
  mv "$filename.utf8" "$filename"
done

%build

%set_build_flags
# enable experimental support for LDAP over UDP (LDAP_CONNECTIONLESS)
export CFLAGS="${CFLAGS} ${LDFLAGS} -Wl,--as-needed -DLDAP_CONNECTIONLESS"

# FIXME in the cross_compiling case, we assume we're crosscompiling
# to something with a yielding select -- this assumption may not
# always be true -- some ifos/ifarch switches may be necessary

%configure \
	--enable-debug \
	--enable-dynamic \
	--enable-versioning \
	\
	--enable-dynacl \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
	--enable-spasswd \
	--enable-modules \
%if %{with perl}
	--enable-perl \
%else
	--disable-perl \
%endif
	--enable-rewrite \
	--enable-rlookups \
	--enable-slapi \
	--disable-slp \
	\
	--enable-backends=mod \
	--enable-bdb=yes \
	--enable-hdb=yes \
	--enable-mdb=yes \
	--enable-monitor=yes \
	--disable-ndb \
	--disable-sql \
	--disable-wt \
	\
	--enable-overlays=mod \
	\
	--disable-static \
	\
	--enable-balancer=mod \
        \
	--with-cyrus-sasl \
	--without-fetch \
	--with-threads \
	--with-pic \
	--with-gnu-ld \
	\
%if %{cross_compiling}
	--with-yielding_select=yes \
%endif
	\
	--libexecdir=%{_libdir}

%make_build

pushd openldap-ppolicy-check-password-%{check_password_version}
%make_build CC="%{__cc}" LDAP_INC="-I../include \
 -I../servers/slapd \
 -I../build-servers/include"
popd

%if %{with compat32}
CONFIGURE_TOP="$(pwd)"
mkdir build32
cd build32
%configure32 \
	--with-subdir=%{name} \
	--localstatedir=/var/run/ldap \
	--enable-dynamic \
	--enable-syslog \
	--enable-ipv6 \
	--enable-local \
	--with-threads \
	--with-tls \
	--disable-slapd \
	--enable-aci \
	--enable-versioning \
	\
	--enable-dynacl \
	--enable-cleartext \
	--enable-crypt \
	--enable-spasswd \
	--enable-modules \
	--enable-perl \
	--enable-rlookups \
	--disable-wrappers \
	--enable-slapi \
	--disable-slp \
	--enable-backends=mod \
	--disable-perl \
	--disable-sql \
	--disable-wt \
	\
	--enable-overlays=mod \
	--enable-shared
make depend
%make_build PROGRAMS=""
cd ..
%endif


%install

mkdir -p %{buildroot}%{_libdir}/

%if %{with compat32}
# Install 32-bit cruft first so the normal install can overwrite it
%make_install -C build32 STRIP="" PROGRAMS=""
%endif

%make_install STRIP_OPTS=""

# install check_password module
pushd openldap-ppolicy-check-password-%{check_password_version}
mv check_password.so check_password.so.%{check_password_version}
ln -s check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/check_password.so
install -m 755 check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/
# install -m 644 README %{buildroot}%{_libdir}/openldap
install -d -m 755 %{buildroot}%{_sysconfdir}/openldap
cat > %{buildroot}%{_sysconfdir}/openldap/check_password.conf <<EOF
# OpenLDAP pwdChecker library configuration

#useCracklib 1
#minPoints 3
#minUpper 0
#minLower 0
#minDigit 0
#minPunct 0
EOF
mv README{,.check_pwd}
popd

# setup directories for TLS certificates
mkdir -p %{buildroot}%{_sysconfdir}/openldap/certs

# setup data and runtime directories
mkdir -p %{buildroot}%{_sharedstatedir}
mkdir -p %{buildroot}%{_localstatedir}
install -m 0700 -d %{buildroot}%{_sharedstatedir}/ldap
install -m 0755 -d %{buildroot}%{_localstatedir}/run/openldap

# setup autocreation of runtime directories on tmpfs
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE2 %{buildroot}%{_tmpfilesdir}/slapd.conf

# install default ldap.conf (customized)
rm %{buildroot}%{_sysconfdir}/openldap/ldap.conf
install -m 0644 %SOURCE4 %{buildroot}%{_sysconfdir}/openldap/ldap.conf

# setup maintainance scripts
mkdir -p %{buildroot}%{_libexecdir}
install -m 0755 -d %{buildroot}%{_libexecdir}/openldap
install -m 0644 %SOURCE50 %{buildroot}%{_libexecdir}/openldap/functions
install -m 0755 %SOURCE52 %{buildroot}%{_libexecdir}/openldap/check-config.sh

# remove build root from config files and manual pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_sysconfdir}/openldap/*.conf
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# we don't need the default files -- RPM handles changes
rm %{buildroot}%{_sysconfdir}/openldap/*.default

# install an init script for the servers
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/slapd.service

# move slapd out of _libdir
mv %{buildroot}%{_libdir}/slapd %{buildroot}%{_sbindir}/

# setup tools as symlinks to slapd
for X in acl add auth cat dn index modify passwd test schema ; do
  rm %{buildroot}%{_sbindir}/slap$X
  ln -s slapd %{buildroot}%{_sbindir}/slap$X
done

%if %{with compat32}
# Deal with headers that differ between 32-bit and 64-bit builds
cd build32/include
for i in *.h; do
	[ -e %{buildroot}%{_includedir}/$i ] || continue
	cmp $i %{buildroot}%{_includedir}/$i && continue
	mv %{buildroot}%{_includedir}/$i %{buildroot}%{_includedir}/${i/.h/-64.h}
	cp $i %{buildroot}%{_includedir}/${i/.h/-32.h}
	cat >%{buildroot}%{_includedir}/$i <<EOF
#ifdef __i386__
#include "${i/.h/-32.h}"
#else
#include "${i/.h/-64.h}"
#endif
EOF
done
cd -
%endif

# re-symlink unversioned libraries, so ldconfig is not confused
pushd %{buildroot}%{_libdir}
v=%{version}
version=$(echo ${v%.[0-9]*})
for lib in liblber libldap libslapi; do
        rm -f ${lib}.so
        ln -s ${lib}.so.%{so_ver} ${lib}.so
done

for lib in $(ls | grep libldap); do
    IFS='.'
    read -r -a libsplit <<< "$lib"
    if [[ -z "${libsplit[3]}" && -n "${libsplit[2]}" ]]
    then
        so_ver_short_2_4="%{so_ver_compat}"
    elif [ -n "${libsplit[3]}" ]
    then
        so_ver_full_2_4="%{so_ver_compat}.${libsplit[3]}.${libsplit[4]}"
    fi
    unset IFS
done

# Provide only libldap and copy it to libldap_r for both 2.4 and 2.6+ versions, make a versioned lib link
# We increase it by 2 because libldap-2.4 has the 'so.2' major version on 2.4.59 (one of the last versions which is EOF)
%__cc -shared -o "%{buildroot}%{_libdir}/libldap-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,libldap-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -lldap
%__cc -shared -o "%{buildroot}%{_libdir}/libldap_r-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,libldap_r-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -lldap
%__cc -shared -o "%{buildroot}%{_libdir}/liblber-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,liblber-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -llber
%__cc -shared -o "%{buildroot}%{_libdir}/libslapi-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,libslapi-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -lslapi
ln -s libldap-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}
ln -s libldap_r-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}
ln -s liblber-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}
ln -s libslapi-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}

popd

# tweak permissions on the libraries to make sure they're correct
chmod 0755 %{buildroot}%{_libdir}/lib*.so*
chmod 0644 %{buildroot}%{_libdir}/lib*.*a
chmod 0644 %{buildroot}%{_libdir}/openldap/*.la

# slapd.conf(5) is obsoleted since 2.3, see slapd-config(5)
mkdir -p %{buildroot}%{_datadir}
install -m 0755 -d %{buildroot}%{_datadir}/openldap-servers
install -m 0644 %SOURCE3 %{buildroot}%{_datadir}/openldap-servers/slapd.ldif
install -m 0644 %SOURCE5 %{buildroot}%{_datadir}/openldap-servers/UPGRADE_INSTRUCTIONS
install -m 0700 -d %{buildroot}%{_sysconfdir}/openldap/slapd.d
rm %{buildroot}%{_sysconfdir}/openldap/slapd.conf
rm %{buildroot}%{_sysconfdir}/openldap/slapd.ldif

# move doc files out of _sysconfdir
mv %{buildroot}%{_sysconfdir}/openldap/schema/README README.schema

# remove files which we don't want packaged
rm %{buildroot}%{_libdir}/*.la  # because we do not want files in %{_libdir}/openldap/ removed, yet

%pre servers
# create ldap user and group
getent group ldap &>/dev/null || groupadd -r -g 55 ldap
getent passwd ldap &>/dev/null || \
	useradd -r -g ldap -u 55 -d %{_sharedstatedir}/ldap -s /sbin/nologin -c "OpenLDAP server" ldap
exit 0

%post servers
%systemd_post slapd.service

# If it's not upgrade - we remove the UPGRADE_INSTRUCTIONS
if [ $1 -lt 2 ] ; then
    rm %{_datadir}/openldap-servers/UPGRADE_INSTRUCTIONS
fi
# generate configuration if necessary
if [[ ! -f %{_sysconfdir}/openldap/slapd.d/cn=config.ldif && \
      ! -f %{_sysconfdir}/openldap/slapd.conf
   ]]; then
      # if there is no configuration available, generate one from the defaults
      mkdir -p %{_sysconfdir}/openldap/slapd.d/ &>/dev/null || :
      /usr/sbin/slapadd -F %{_sysconfdir}/openldap/slapd.d/ -n0 -l %{_datadir}/openldap-servers/slapd.ldif
      chown -R ldap:ldap %{_sysconfdir}/openldap/slapd.d/
      %{systemctl_bin} try-restart slapd.service &>/dev/null
fi

# restart after upgrade
if [ $1 -ge 1 ]; then
    %{systemctl_bin} condrestart slapd.service &>/dev/null || :
fi

exit 0

%preun servers
%systemd_preun slapd.service

%postun servers
%systemd_postun_with_restart slapd.service

%files
%doc ANNOUNCEMENT
%doc CHANGES
%license COPYRIGHT
%license LICENSE
%doc README
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/certs
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%dir %{_libexecdir}/openldap/
%{_mandir}/man5/ldif.5*
%{_mandir}/man5/ldap.conf.5*

%files -n %{libname}
%{_libdir}/libldap.so.*

%files -n %{lberlibname}
%{_libdir}/liblber.so.*

%files -n %{slapilibname}
%{_libdir}/libslapi.so.*

%files servers
%doc contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%doc doc/guide/admin/*.html
%doc doc/guide/admin/*.png
%doc servers/slapd/back-perl/SampleLDAP.pm
%doc servers/slapd/back-perl/README.back_perl
%doc openldap-ppolicy-check-password-%{check_password_version}/README.check_pwd
%doc README.schema
%config(noreplace) %dir %attr(0750,ldap,ldap) %{_sysconfdir}/openldap/slapd.d
%config(noreplace) %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/check_password.conf
%{_tmpfilesdir}/slapd.conf
%dir %attr(0700,ldap,ldap) %{_sharedstatedir}/ldap
%dir %attr(-,ldap,ldap) %{_localstatedir}/run/openldap
%{_unitdir}/slapd.service
%{_datadir}/openldap-servers/
%{_libdir}/openldap/accesslog*
%{_libdir}/openldap/allop*
%{_libdir}/openldap/auditlog*
%{_libdir}/openldap/autoca*
%{_libdir}/openldap/back_asyncmeta*
%{_libdir}/openldap/back_dnssrv*
%{_libdir}/openldap/back_ldap*
%{_libdir}/openldap/back_meta*
%{_libdir}/openldap/back_null*
%{_libdir}/openldap/back_passwd*
%{_libdir}/openldap/back_relay*
%{_libdir}/openldap/back_sock*
%{_libdir}/openldap/check_password*
%{_libdir}/openldap/collect*
%{_libdir}/openldap/constraint*
%{_libdir}/openldap/dds*
%{_libdir}/openldap/deref*
%{_libdir}/openldap/dyngroup*
%{_libdir}/openldap/dynlist*
%{_libdir}/openldap/home*
%{_libdir}/openldap/lloadd*
%{_libdir}/openldap/memberof*
%{_libdir}/openldap/otp*
%{_libdir}/openldap/pcache*
%{_libdir}/openldap/ppolicy*
%{_libdir}/openldap/refint*
%{_libdir}/openldap/remoteauth*
%{_libdir}/openldap/retcode*
%{_libdir}/openldap/rwm*
%{_libdir}/openldap/seqmod*
%{_libdir}/openldap/smbk5pwd*
%{_libdir}/openldap/sssvlv*
%{_libdir}/openldap/syncprov*
%{_libdir}/openldap/translucent*
%{_libdir}/openldap/unique*
%{_libdir}/openldap/valsort*
%{_libexecdir}/openldap/functions
%{_libexecdir}/openldap/check-config.sh
%{_sbindir}/sl*
%{_mandir}/man8/*
%{_mandir}/man5/lloadd.conf.5*
%{_mandir}/man5/slapd*.5*
%{_mandir}/man5/slapo-*.5*
%{_mandir}/man5/slappw-argon2.5*
# obsolete configuration
%ghost %config(noreplace,missingok) %attr(0640,ldap,ldap) %{_sysconfdir}/openldap/slapd.conf

%files clients
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{devname}
%doc doc/drafts doc/rfc
%{_libdir}/liblber.so
%{_libdir}/libldap.so
%{_libdir}/libslapi.so
%{_includedir}/*
%{_libdir}/pkgconfig/lber.pc
%{_libdir}/pkgconfig/ldap.pc
%{_mandir}/man3/*

%files -n %{compatname}
%{_libdir}/libldap-2.4*.so.*
%{_libdir}/libldap_r-2.4*.so.*
%{_libdir}/liblber-2.4*.so.*
%{_libdir}/libslapi-2.4*.so.*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/lib*.so.*

%files -n %{dev32name}
%{_prefix}/lib/libl*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif

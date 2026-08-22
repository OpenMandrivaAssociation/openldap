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
%global major_version 2.7

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

Name: openldap
Version: 2.7.0
Release: 2
Summary: LDAP support libraries
License: OpenLDAP
URL: https://www.openldap.org/

Source0: https://openldap.org/software/download/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: slapd.service
Source2: slapd.tmpfiles
Source3: slapd.ldif
Source4: ldap.conf
Source10: https://github.com/ltb-project/openldap-ppolicy-check-password/archive/v%{check_password_version}/openldap-ppolicy-check-password-%{check_password_version}.tar.gz
Source50: libexec-functions
Source52: libexec-check-config.sh

# Extra schemas -- RFC2307bis is the successor to NIS
Source100: https://github.com/jtyr/rfc2307bis/raw/refs/heads/master/rfc2307bis.schema
# Same thing converted to LDIF format
Source101: https://github.com/palw3ey/rfc2307bis/raw/refs/heads/main/rfc2307bis.ldif

# Patches for 2.7
Patch0: openldap-manpages.patch
Patch1: openldap-reentrant-gethostby.patch

Patch3: openldap-smbk5pwd-overlay.patch
Patch4: openldap-ai-addrconfig.patch
Patch5: openldap-allop-overlay.patch

# System-wide default for CA certs
Patch7: openldap-openssl-manpage-defaultCA.patch
Patch9: https://git.openldap.org/openldap/openldap/-/merge_requests/303.patch

# check-password module specific patches
Patch90: check-password-makefile.patch
Patch91: check-password.patch

#Patch200: openldap-2.6.6-clang16.patch
Patch201: openldap-2.6.6-compat-2.4.patch
# memcmp works on all OM targets, but detection
# doesn't work reliably when crosscompiling, so
# disable it
Patch202: openldap-2.6-cross.patch
Patch203: openldap-sltdl.patch
Patch204: openldap-fix-Makefiles.patch

BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	pkgconfig(sltdl)
BuildRequires: autoconf
BuildRequires: pkgconfig(libsasl2)
BuildRequires: locales-extra-charsets
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: pkgconfig(libevent)
BuildRequires: make
BuildRequires: pkgconfig(libcrypto)
BuildRequires: perl-interpreter

Requires: %{libname} = %{EVRD}
Requires: %{lberlibname} = %{EVRD}
Requires: %{slapilibname} = %{EVRD}

%if %{with compat32}
BuildRequires: devel(libkrb5)
BuildRequires: devel(libncurses)
BuildRequires: devel(libssl)
BuildRequires: devel(libcom_err)
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
autoreconf

# build smbk5pwd with other overlays
ln -s ../../../contrib/slapd-modules/smbk5pwd/smbk5pwd.c servers/slapd/overlays
mv contrib/slapd-modules/smbk5pwd/README contrib/slapd-modules/smbk5pwd/README.smbk5pwd
# build allop with other overlays
ln -s ../../../contrib/slapd-modules/allop/allop.c servers/slapd/overlays
mv contrib/slapd-modules/allop/README contrib/slapd-modules/allop/README.allop
mv contrib/slapd-modules/allop/slapo-allop.5 doc/man/man5/slapo-allop.5

# fix documentation encoding
for filename in doc/drafts/draft-ietf-ldapext-acl-model-xx.txt; do
  iconv -f iso-8859-1 -t utf-8 "$filename" > "$filename.utf8"
  mv "$filename.utf8" "$filename"
done

%build

%set_build_flags
# -DLDAP_CONNECTIONLESS: enable experimental support for LDAP over
# UDP (LDAP_CONNECTIONLESS)
# -Wl,--export-dynamic: Make sure symbols like
# slap_anlist_no_attrs (from slapd) are visible to plugins like memberof
export CFLAGS="${CFLAGS} ${LDFLAGS} -Wl,--as-needed -Wl,--export-dynamic -DLDAP_CONNECTIONLESS"

# FIXME in the cross_compiling case, we assume we're crosscompiling
# to something with a yielding select -- this assumption may not
# always be true -- some ifos/ifarch switches may be necessary

LIBTOOL=slibtool-shared \
%configure \
	--enable-debug \
	--enable-dynamic \
	--enable-versioning \
	\
	--sharedstatedir=/srv/ldap \
	--enable-dynacl \
	--enable-cleartext \
	--enable-crypt \
	--enable-spasswd \
	--enable-modules \
	--enable-rlookups \
	--enable-slapi \
	--disable-slp \
	\
	--enable-backends=mod \
	--enable-mdb=yes \
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

%make_build LIBTOOL=slibtool-shared

pushd openldap-ppolicy-check-password-%{check_password_version}
%make_build CC="%{__cc}" LIBTOOL=slibtool-shared LDAP_INC="-I../include \
 -I../servers/slapd \
 -I../build-servers/include"
popd #" <-- workaround for a vim syntax highlighting bug, ignore

%if %{with compat32}
CONFIGURE_TOP="$(pwd)"
mkdir build32
cd build32
%configure32 \
	--with-subdir=%{name} \
	--localstatedir=/var/run/ldap \
	--sharedstatedir=/srv/ldap \
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
	--enable-rlookups \
	--disable-wrappers \
	--enable-slapi \
	--disable-slp \
	--enable-backends=mod \
	--disable-wt \
	\
	--enable-overlays=mod \
	--enable-shared
make depend LIBTOOL=slibtool-shared
%make_build PROGRAMS="" LIBTOOL=slibtool-shared
cd ..
%endif


%install
mkdir -p %{buildroot}%{_libdir}/

%if %{with compat32}
# Install 32-bit cruft first so the normal install can overwrite it
%make_install -C build32 STRIP="" PROGRAMS="" LIBTOOL=slibtool-shared
%endif

%make_install STRIP_OPTS="" LIBTOOL=slibtool-shared

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
mkdir -p %{buildroot}/srv
mkdir -p %{buildroot}%{_localstatedir}
install -m 0700 -d %{buildroot}/srv/ldap
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

# Provide only libldap and copy it to libldap_r for both 2.4 and current versions, make a versioned lib link
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

# slapd.conf(5) is obsoleted since 2.3, see slapd-config(5)
mkdir -p %{buildroot}%{_datadir}
install -m 0755 -d %{buildroot}%{_datadir}/openldap-servers
install -m 0644 %SOURCE3 %{buildroot}%{_datadir}/openldap-servers/slapd.ldif
install -m 0700 -d %{buildroot}%{_sysconfdir}/openldap/slapd.d
rm %{buildroot}%{_sysconfdir}/openldap/slapd.conf
rm %{buildroot}%{_sysconfdir}/openldap/slapd.ldif

# move doc files out of _sysconfdir
mv %{buildroot}%{_sysconfdir}/openldap/schema/README README.schema

# Create the ldap user and group
mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/ldap.conf <<'EOF'
g ldap 55 - -
u ldap 55:55 "OpenLDAP server" /srv/ldap /sbin/nologin
EOF

# Extra schemas
install -c -m 644 %{S:100} %{buildroot}%{_sysconfdir}/openldap/schema/
install -c -m 644 %{S:101} %{buildroot}%{_sysconfdir}/openldap/schema/

# Move from /var/lib/ldap to /srv/ldap
# Old name prior to 2.6.12-1, after 6.0, 2026-02-17
# Also dump MDB databases with the old slapcat before unpacking 2.7 (LMDB 1.0).
%pretrans servers -p <lua>
-- arg[2] is $1: 1 on initial install, >=2 on upgrade.
-- Fresh install: nothing to migrate or dump, and omv.lua is not
-- in an empty --root yet (%pretrans runs before any files unpack).
local ninst = tonumber(arg[2]) or 0
if ninst < 2 then
	return
end

omv = require("omv")
omv.dir2Symlink("/var/lib/ldap", "/srv/ldap")

-- Automatic LMDB 0.9 -> 1.0 dump for upgrades from OpenLDAP < 2.7.
-- Must run in %%pretrans so the still-installed < 2.7 slapcat is used.
local UPGRADE_DIR = "/var/lib/openldap-upgrade"
local STATE = UPGRADE_DIR .. "/state"
local MANIFEST = UPGRADE_DIR .. "/manifest"
local LOG = UPGRADE_DIR .. "/upgrade.log"

local function exists(p)
	return posix.stat(p) ~= nil
end

local function log(msg)
	print("openldap: " .. msg)
	omv.mkdir_p(UPGRADE_DIR)
	local f = io.open(LOG, "a")
	if f then
		f:write(os.date("%%Y-%%m-%%d %%H:%%M:%%S ") .. msg .. "\n")
		f:close()
	end
end

local function find_cmd(cands)
	for _, n in ipairs(cands) do
		if posix.access(n, "x") then
			return n
		end
	end
	return nil
end

local function readfile(p)
	local f = io.open(p, "r")
	if not f then return "" end
	local t = f:read("*a")
	f:close()
	return t
end

local function writefile(p, data)
	local f = io.open(p, "w")
	if not f then return false end
	f:write(data)
	f:close()
	return true
end

local function trim(s)
	if not s then return s end
	return (s:gsub("^%%s+", ""):gsub("%%s+$", ""))
end

local function unfold_ldif(text)
	return (text:gsub("\n ", ""))
end

local function parse_mdb_from_ldif(text)
	text = unfold_ldif(text)
	local dbs, cur = {}, {}
	local function flush()
		if cur.dir and cur.suffix then
			cur.dir = trim(cur.dir)
			cur.suffix = trim(cur.suffix)
			if exists(cur.dir .. "/data.mdb") then
				table.insert(dbs, {suffix = cur.suffix, dir = cur.dir})
			end
		end
		cur = {}
	end
	for line in text:gmatch("[^\n]+") do
		if line:match("^dn:") then
			flush()
		elseif line:match("^olcSuffix:: ") then
			cur.suffix = rpm.b64decode(line:match("^olcSuffix::%%s*(%%S+)"))
		elseif line:match("^olcSuffix: ") then
			cur.suffix = line:match("^olcSuffix:%%s*(.+)$")
		elseif line:match("^olcDbDirectory:: ") then
			cur.dir = rpm.b64decode(line:match("^olcDbDirectory::%%s*(%%S+)"))
		elseif line:match("^olcDbDirectory: ") then
			cur.dir = line:match("^olcDbDirectory:%%s*(.+)$")
		end
	end
	flush()
	return dbs
end

local function parse_mdb_from_slapd_conf(path)
	local f = io.open(path, "r")
	if not f then return {} end
	local dbs = {}
	local suf, dir, ismdb
	local function flush()
		if ismdb and dir and suf and exists(dir .. "/data.mdb") then
			table.insert(dbs, {suffix = trim(suf), dir = trim(dir)})
		end
		suf, dir, ismdb = nil, nil, nil
	end
	for line in f:lines() do
		local db = line:match("^%%s*[Dd][Aa][Tt][Aa][Bb][Aa][Ss][Ee]%%s+(%%S+)")
		if db then
			flush()
			db = db:lower():gsub('"', "")
			ismdb = (db == "mdb" or db == "hdb" or db == "bdb")
		else
			local s = line:match("^%%s*[Ss][Uu][Ff][Ff][Ii][Xx]%%s+(.+)$")
			if s then suf = s:gsub('"', "") end
			local d = line:match("^%%s*[Dd][Ii][Rr][Ee][Cc][Tt][Oo][Rr][Yy]%%s+(%%S+)")
			if d then dir = d:gsub('"', "") end
		end
	end
	flush()
	f:close()
	return dbs
end

if exists(STATE) then
	local st = trim(readfile(STATE))
	if st == "dumped" or st == "reloaded" then
		return
	end
end

local slapd = find_cmd({"/usr/sbin/slapd", "/usr/bin/slapd"})
if not slapd then
	return
end

omv.mkdir_p(UPGRADE_DIR)
posix.chmod(UPGRADE_DIR, "0700")

local tmp_ver = UPGRADE_DIR .. "/.slapd-vv"
rpm.spawn({slapd, "-VV"}, {stdout = tmp_ver, stderr = tmp_ver})
local vout = readfile(tmp_ver)
posix.unlink(tmp_ver)
local ver = vout:match("slapd%%s+([0-9]+%%.[0-9]+%%.[0-9]+)") or vout:match("slapd%%s+([0-9]+%%.[0-9]+)")
if not ver then
	local tmp_q = UPGRADE_DIR .. "/.rpmq"
	rpm.spawn({"/usr/bin/rpm", "-q", "--qf", "%%{VERSION}", "openldap-servers"},
		{stdout = tmp_q, stderr = "/dev/null"})
	ver = trim(readfile(tmp_q))
	posix.unlink(tmp_q)
	if ver and ver:match("not installed") then
		ver = nil
	end
end
if not ver or rpm.vercmp(ver, "2.7.0") >= 0 then
	return
end

local slapcat = find_cmd({"/usr/sbin/slapcat", "/usr/bin/slapcat"})
if not slapcat then
	log("OpenLDAP " .. ver .. " is installed but slapcat is missing; cannot dump MDB for 2.7")
	error("openldap: slapcat not found; cannot dump MDB databases for the 2.7 LMDB 1.0 upgrade")
end

local cfg_args
if exists("/etc/openldap/slapd.d/cn=config.ldif") then
	cfg_args = {"-F", "/etc/openldap/slapd.d"}
elseif exists("/etc/openldap/slapd.conf") then
	cfg_args = {"-f", "/etc/openldap/slapd.conf"}
else
	if exists("/srv/ldap/data.mdb") or exists("/var/lib/ldap/data.mdb") then
		error("openldap: MDB data exists but no slapd configuration was found; dump with 2.6 slapcat before upgrading")
	end
	return
end

local systemctl = find_cmd({"/usr/bin/systemctl", "/bin/systemctl"})
if systemctl then
	rpm.spawn({systemctl, "stop", "slapd.service"}, {stdout = "/dev/null", stderr = "/dev/null"})
end

local dbs = {}
if cfg_args[1] == "-F" then
	local cfg_ldif = UPGRADE_DIR .. "/cn-config.ldif"
	local cmd = {slapcat}
	for _, a in ipairs(cfg_args) do table.insert(cmd, a) end
	table.insert(cmd, "-b")
	table.insert(cmd, "cn=config")
	table.insert(cmd, "-l")
	table.insert(cmd, cfg_ldif)
	rpm.spawn(cmd, {stderr = UPGRADE_DIR .. "/slapcat-config.err"})
	if exists(cfg_ldif) then
		dbs = parse_mdb_from_ldif(readfile(cfg_ldif))
	end
	if #dbs == 0 then
		local confdir = "/etc/openldap/slapd.d/cn=config"
		local acc = ""
		if exists(confdir) then
			for _, name in ipairs(posix.dir(confdir)) do
				if name:match("^olcDatabase=") and name:match("%%.ldif$") then
					acc = acc .. readfile(confdir .. "/" .. name) .. "\n"
				end
			end
		end
		if acc ~= "" then
			dbs = parse_mdb_from_ldif(acc)
		end
	end
else
	dbs = parse_mdb_from_slapd_conf("/etc/openldap/slapd.conf")
end

if #dbs == 0 then
	local fallback = nil
	if exists("/srv/ldap/data.mdb") then
		fallback = "/srv/ldap"
	elseif exists("/var/lib/ldap/data.mdb") then
		fallback = "/var/lib/ldap"
	end
	if fallback then
		dbs = {{dir = fallback, dbnum = 1}}
	else
		log("OpenLDAP " .. ver .. ": no MDB databases to convert")
		return
	end
end

log("dumping " .. #dbs .. " MDB database(s) from OpenLDAP " .. ver .. " for LMDB 1.0 reload")

local mf = io.open(MANIFEST, "w")
if not mf then
	error("openldap: cannot write " .. MANIFEST)
end

for i, db in ipairs(dbs) do
	local ldif = UPGRADE_DIR .. "/db-" .. i .. ".ldif"
	local cmd = {slapcat}
	for _, a in ipairs(cfg_args) do table.insert(cmd, a) end
	local seltype, selector
	if db.suffix then
		seltype, selector = "b", db.suffix
		table.insert(cmd, "-b")
		table.insert(cmd, db.suffix)
	else
		seltype, selector = "n", tostring(db.dbnum or 1)
		table.insert(cmd, "-n")
		table.insert(cmd, selector)
	end
	table.insert(cmd, "-l")
	table.insert(cmd, ldif)
	local errf = UPGRADE_DIR .. "/slapcat-" .. i .. ".err"
	local rc = rpm.spawn(cmd, {stderr = errf})
	if rc ~= 0 or not exists(ldif) then
		mf:close()
		local detail = trim(readfile(errf))
		log("slapcat failed for " .. selector .. ": " .. detail)
		error("openldap: slapcat failed for '" .. selector ..
			"'. Staying on OpenLDAP " .. ver ..
			" so you can dump the MDB database manually. See " .. UPGRADE_DIR)
	end
	mf:write(seltype .. "\t" .. selector .. "\t" .. db.dir .. "\t" .. ldif .. "\n")
	log("dumped " .. selector .. " (" .. db.dir .. ") -> " .. ldif)
end
mf:close()

writefile(STATE, "dumped\n")
writefile(UPGRADE_DIR .. "/README", [[
OpenLDAP automatic MDB reload (LMDB 0.9 -> 1.0)
================================================

OpenLDAP 2.7 uses LMDB 1.0, which cannot open 2.6 (LMDB 0.9) data.mdb files.
This directory holds slapcat dumps taken with the old slapd before the upgrade.

After a successful upgrade:
  - reloaded databases live in their original olcDbDirectory
  - the original MDB files are saved as <directory>/pre-2.7-backup/
  - LDIF dumps remain here

Once you have confirmed slapd is healthy you may remove:
  rm -rf /var/lib/openldap-upgrade
  rm -rf <directory>/pre-2.7-backup

If reload failed, slapd is intentionally not started. Fix the error in
upgrade.log / slapcat-*.err, then either:
  - reinstall/upgrade openldap-servers to retry slapadd, or
  - slapadd the db-*.ldif files by hand with OpenLDAP 2.7
]])
log("MDB dump complete; slapadd will run from %%post")

%post servers
# Reload MDB dumps taken in %%pretrans (LMDB 0.9 -> 1.0)
UPGRADE_DIR=/var/lib/openldap-upgrade
STATE=$UPGRADE_DIR/state
MANIFEST=$UPGRADE_DIR/manifest
if [ -f "$STATE" ]; then
	st=$(tr -d '\n' < "$STATE" 2>/dev/null)
	if [ "$st" = "dumped" ] || [ "$st" = "failed" ]; then
		echo "openldap: reloading MDB databases into LMDB 1.0 format"
		%{systemctl_bin} stop slapd.service &>/dev/null || :
		SLAPADD=%{_sbindir}/slapadd
		[ -x "$SLAPADD" ] || SLAPADD=/usr/bin/slapadd
		if [ -f %{_sysconfdir}/openldap/slapd.d/cn=config.ldif ]; then
			SLAPADD_CFG="-F %{_sysconfdir}/openldap/slapd.d"
		elif [ -f %{_sysconfdir}/openldap/slapd.conf ]; then
			SLAPADD_CFG="-f %{_sysconfdir}/openldap/slapd.conf"
		else
			SLAPADD_CFG=""
		fi
		failed=0
		if [ ! -f "$MANIFEST" ]; then
			echo "openldap: $MANIFEST missing; cannot reload MDB dumps"
			echo failed > "$STATE"
			exit 1
		fi
		while IFS="$(printf '\t')" read -r seltype selector dir ldif; do
			[ -n "$seltype" ] || continue
			if [ ! -f "$ldif" ]; then
				echo "openldap: missing dump $ldif"
				failed=1
				continue
			fi
			mkdir -p "$dir/pre-2.7-backup"
			for f in "$dir"/data.mdb "$dir"/lock.mdb "$dir"/alock; do
				if [ -e "$f" ]; then
					mv -f "$f" "$dir/pre-2.7-backup/"
				fi
			done
			for f in "$dir"/*.mdb; do
				[ -e "$f" ] || continue
				mv -f "$f" "$dir/pre-2.7-backup/"
			done
			if [ "$seltype" = "b" ]; then
				addrc=0
				"$SLAPADD" $SLAPADD_CFG -b "$selector" -l "$ldif" -q -w >>"$UPGRADE_DIR/upgrade.log" 2>&1 || addrc=$?
			else
				addrc=0
				"$SLAPADD" $SLAPADD_CFG -n "$selector" -l "$ldif" -q -w >>"$UPGRADE_DIR/upgrade.log" 2>&1 || addrc=$?
			fi
			if [ "$addrc" -ne 0 ]; then
				echo "openldap: slapadd failed for $selector (exit $addrc); restoring pre-2.7 MDB backup"
				mv -f "$dir/pre-2.7-backup/"* "$dir/" 2>/dev/null || :
				failed=1
				continue
			fi
			chown -R ldap:ldap "$dir" 2>/dev/null || :
			echo "openldap: reloaded $selector (backup in $dir/pre-2.7-backup)"
		done < "$MANIFEST"
		if [ "$failed" -ne 0 ]; then
			echo failed > "$STATE"
			echo "openldap: MDB reload failed. slapd will not start. See $UPGRADE_DIR/README and $UPGRADE_DIR/upgrade.log"
			exit 1
		fi
		echo reloaded > "$STATE"
		echo "openldap: MDB reload complete. Original MDB files kept under <dbdir>/pre-2.7-backup; dumps in $UPGRADE_DIR"
	fi
fi

TARGET_DN=$(slapcat -b cn=config 2>/dev/null | \
	awk '/^dn: / {dn=$2} /^olcDbDirectory:[[:space:]]*\/var\/lib\/ldap/ {print dn}')
if [[ -n "$TARGET_DN" ]]; then
	MIGRATE_LDIF="dn: $TARGET_DN
changetype: modify
replace: olcDbDirectory
olcDbDirectory: /srv/ldap"
	if slapcat -b cn=config 2>/dev/null |grep -qE '^olcDbDirectory:[[:space:]]*/var/lib/ldap$'; then
		echo "$MIGRATE_LDIF" | ldapmodify -Y EXTERNAL -H ldapi:/// 2>/dev/null || \
		echo "$MIGRATE_LDIF" | slapmodify -b cn=config 2>/dev/null || :
	fi
	# Just in case slapmodify changed it to root
	chown -R ldap:ldap /etc/openldap/slapd.d
fi
# End /var/lib/ldap to /srv/ldap move

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
%doc openldap-ppolicy-check-password-%{check_password_version}/README.check_pwd
%doc README.schema
%config(noreplace) %dir %attr(0750,ldap,ldap) %{_sysconfdir}/openldap/slapd.d
%config(noreplace) %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/check_password.conf
%{_tmpfilesdir}/slapd.conf
# Old name prior to 2.6.12-1, after 6.0, 2026-02-17
%ghost %{_sharedstatedir}/ldap
%dir %attr(0700,ldap,ldap) /srv/ldap
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
%{_libdir}/openldap/nestgroup*
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
%{_sysusersdir}/*.conf
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

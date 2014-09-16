%define apiversion 0.1
%define soversion 1

%define lib %mklibname abw %{apiversion} %{soversion}
%define devel %mklibname -d abw

Name: libabw
Version: 0.1.0
Release: 2
Summary: A library for import of AbiWord files

Group: System/Libraries
License: MPLv2.0
URL: http://www.freedesktop.org/wiki/Software/libabw/
Source0: http://dev-www.libreoffice.org/src/libabw/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gperf
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)

%description
%{name} is a library for import of AbiWord files.

%package -n %{lib}
Summary: %{summary}
Group: System/Libraries

%description -n %{lib}
%{description}

%package -n %{devel}
Summary: Development files for %{name}
Group: Development/C
Requires: %{lib} = %{EVRD}

%description -n %{devel}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
Group: Books/Computer books
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform AbiWord files into other formats
Group: Publishing
Requires: %{lib} = %{EVRD}

%description tools
Tools to transform AbiWord files into other formats. Currently
supported: XHTML, raw, text.

%prep
%setup -q
aclocal
automake -a
autoconf

%build
%configure --disable-silent-rules --disable-static --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{devel}
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%{_libdir}/libabw-%{apiversion}.so

%files -n %{lib}
%{_libdir}/libabw-%{apiversion}.so.%{soversion}*

%files doc
%doc COPYING.MPL
%doc docs/doxygen/html

%files tools
%{_bindir}/abw2raw
%{_bindir}/abw2text
%{_bindir}/abw2html

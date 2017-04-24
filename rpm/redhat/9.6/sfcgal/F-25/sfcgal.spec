%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	C++ wrapper library around CGAL for PostGIS
Name:		SFCGAL
Version:	1.2.2
Release:	1%{?dist}
License:	GLPLv2
Group:		System Environment/Libraries
Source:		https://github.com/Oslandia/%{name}/archive/v%{version}.tar.gz
URL:		http://sfcgal.org/
BuildRequires:	cmake, CGAL-devel
BuildRequires:	boost-thread, boost-system, boost-date-time, boost-serialization
BuildRequires:	mpfr-devel, gmp-devel, gcc-c++
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

SFCGAL provides standard compliant geometry types and operations, that
can be accessed from its C or C++ APIs. PostGIS uses the C API, to
expose some SFCGAL's functions in spatial databases (cf. PostGIS
manual).

Geometry coordinates have an exact rational number representation and
can be either 2D or 3D.

%package libs
Summary:	The shared libraries required for SFCGAL
Group:		Applications/Databases
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description libs
The sfcgal-libs package provides the essential shared libraries for SFCGAL.

%package devel
Summary:	The development files for SFCGAL
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description devel
Development headers and libraries for SFCGAL.

%prep
%setup -q

%build
%cmake	-D LIB_INSTALL_DIR=%{_lib} -DBoost_NO_BOOST_CMAKE=BOOL:ON .

make %{?_smp_mflags}

%install
make %{?_smp_mflags} install/fast DESTDIR=%{buildroot}

%post
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%post libs
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%postun
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif
%postun libs
%ifarch ppc64 ppc64le
%{atpath}/sbin/ldconfig
%else
/sbin/ldconfig
%endif

%files
%doc AUTHORS README.md NEWS
%license LICENSE
%{_bindir}/sfcgal-config

%files devel
%{_includedir}/%{name}/

%files libs
%{_libdir}/libSFCGAL.so*
/usr/lib/libSFCGAL.la

%changelog
* Thu Nov 19 2015 Oskari Saarenmaa <os@ohmu.fi> 1.2.2-1
- Update to 1.2.2 to support newer CGAL versions

* Fri Oct 30 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.2.0-1
- Initial build for PostgreSQL YUM Repository.

%undefine _debugsource_packages
%global postgismajorversion 3.1
%global postgissomajorversion 3
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global sname	postgis

%pgdg_set_gis_variables

%{!?utils:%global	utils 1}
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1315
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%else
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 0}
%endif
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1315
%{!?raster:%global     raster 1}
%else
%{!?raster:%global     raster 0}
%endif
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1315
%ifnarch ppc64 ppc64le
# TODO
%{!?sfcgal:%global     sfcgal 1}
%else
%{!?sfcgal:%global     sfcgal 0}
%endif
%else
%{!?sfcgal:%global    sfcgal 0}
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.0
Release:	alpha2_3%{?dist}
License:	GPLv2+
Source0:	https://download.osgeo.org/postgis/source/postgis-%{version}alpha2.tar.gz
Source2:	https://download.osgeo.org/postgis/docs/postgis-%{version}alpha2.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh
Patch0:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.0-gdalfpic.patch

URL:		http://www.postgis.net/

BuildRequires:	postgresql%{pgmajorversion}-devel geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	pgdg-srpm-macros >= 1.0.5 pcre-devel gmp-devel
Requires:	gmp
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libjson-c-devel proj%{projmajorversion}-devel >= %{projfullversion}
%endif
%else
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion} flex json-c-devel
%endif
BuildRequires:	libxml2-devel
%if %{shp2pgsqlgui}
BuildRequires:	gtk2-devel > 2.8.0
%endif
%if %{sfcgal}
BuildRequires:	SFCGAL-devel SFCGAL
Requires:	SFCGAL
%endif
%if %{raster}
  %if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:	gdal-devel >= 1.9.2-9
  %else
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
  %endif
%endif

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
BuildRequires:	protobuf-c-devel
%endif

Requires:	postgresql%{pgmajorversion} geos%{geosmajorversion} >= %{geosfullversion}
Requires:	postgresql%{pgmajorversion}-contrib proj%{projmajorversion} >= %{projfullversion}
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	pcre
%if 0%{?suse_version} >= 1315
Requires:	libjson-c2 gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
Requires:	libxerces-c-3_1
%else
Requires:	json-c xerces-c
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	gdal-libs >= 1.9.2-9
%else
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
%endif
%endif
Requires(post):	%{_sbindir}/update-alternatives

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
Requires:	protobuf-c
%endif

Provides:	%{sname} = %{version}-%{release}
Obsoletes:	%{sname}3_%{pgmajorversion} <= %{postgismajorversion}.0-1
Provides:	%{sname}3_%{pgmajorversion} => %{postgismajorversion}.0

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package client
Summary:	Client tools and their libraries of PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-client <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-client => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-devel <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-devel => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Obsoletes:	%{sname}2_%{pgmajorversion}-docs <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-docs => %{postgismajorversion}.0

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%if %{shp2pgsqlgui}
%package	gui
Summary:	GUI for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	gui
The %{name}-gui package provides a gui for PostGIS.
%endif

%if %utils
%package utils
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release} perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-utils <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-utils => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}alpha2
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0

%build
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{libspatialiteinstdir}/lib ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SFCGAL_LDFLAGS="$SFCGAL_LDFLAGS -L/usr/lib64";  export SFCGAL_LDFLAGS

%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif

LDFLAGS="$LDFLAGS -L/usr/lib64/ -L%{geosinstdir}/lib64 -lgeos_c -L%{projinstdir}/lib -L%{gdalinstdir}/lib -L%{libgeotiffinstdir}/lib -ltiff"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{projinstdir}/lib/pkgconfig

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
%if !%raster
	--without-raster \
%endif
%if %{sfcgal}
	--with-sfcgal=%{_bindir}/sfcgal-config \
%endif
%if %{shp2pgsqlgui}
	--with-gui \
%endif
	--enable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=/%{geosinstdir}/bin/geos-config \
	--with-gdalconfig=%{gdalinstdir}/bin/gdal-config

SHLIB_LINK="$SHLIB_LINK" %{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgissomajorversion}.so"

%{__make} -C extensions

%if %utils
 SHLIB_LINK="$SHLIB_LINK" %{__make} -C utils
%endif

%install
%{__rm} -rf %{buildroot}
SHLIB_LINK="$SHLIB_LINK" %{__make} install DESTDIR=%{buildroot}

%if %utils
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create alternatives entries for common binaries
%post client
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql %{pgmajorversion}0

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{pginstdir}/bin/pgsql2shp
	%{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{pginstdir}/bin/shp2pgsql
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.TXT
%else
%license LICENSE.TXT
%endif
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*topology*.sql
%{pginstdir}/lib/%{sname}-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%if %{sfcgal}
%{pginstdir}/share/extension/%{sname}_sfcgal*.sql
%{pginstdir}/share/extension/%{sname}_sfcgal.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_upgrade.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_sfcgal.sql

%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}_topology-%{postgissomajorversion}.so
%{pginstdir}/lib/address_standardizer-3.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_comments.sql
%if %{raster}
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis_legacy.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis_upgrade.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/uninstall_rtpostgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/extension/postgis_raster*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_legacy.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/lib/postgis_raster-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}_raster.control
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%endif
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/address_standardizer*.bc
   %{pginstdir}/lib/bitcode/address_standardizer-3/*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgissomajorversion}/*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgissomajorversion}/*.bc
   %if %raster
   %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}/*.bc
   %endif
  %endif
 %endif
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/pgsql2shp
%attr(755,root,root) %{pginstdir}/bin/raster2pgsql
%attr(755,root,root) %{pginstdir}/bin/shp2pgsql

%files devel
%defattr(644,root,root)

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}alpha2.pdf

%if %shp2pgsqlgui
%files gui
%defattr(-,root,root)
%{pginstdir}/bin/shp2pgsql-gui
%{pginstdir}/share/applications/shp2pgsql-gui.desktop
%{pginstdir}/share/icons/hicolor/*/apps/shp2pgsql-gui.png
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%changelog
* Fri Oct 30 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_3
- Fix various rpath issues, per Sandeep Thakkar.

* Tue Sep 29 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_2
- Rebuild against GDAL and libgeotiff 1.6

* Tue Jul 28 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_1
- Update to 3.1 alpha2

* Sun May 24 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha1_1
- Initial cut for PostGIS 3.1.0 Alpha 1

* Tue May 5 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-5
- Rebuild against Proj 7.0.1

* Thu Mar 12 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-4
- Rebuild against Proj 7.0.0 and GeOS 3.8.1
- Make sure that the package requires exact versions of Proj and GeOS.

* Thu Mar 12 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-3
- Fix alternatives error

* Tue Feb 25 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-2
- Use pkgconfig for Proj support, per warnings.

* Tue Feb 25 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-1
- Update to 3.0.1

* Wed Feb 5 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-2
- Rebuild for Proj 6.3.0 and GDAL 3.0.4

* Fri Oct 25 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Wed Oct 16 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0rc2
- Update to 3.0.0rc2

* Fri Oct 11 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0rc1
- Update to rc1

* Fri Oct 4 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0beta1
- Update to beta1
- Use Geos 3.8

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0alpha4-6
- Fix broken symlink, per report from Paul Ramsey:
  https://redmine.postgresql.org/issues/4776

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0alpha4-5
- Rebuild for GeOS 3.7.2

* Tue Sep 17 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-4
- Update GDAL dependency to 3.0.1
- Use a few more macros for easier maintenance.

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-3
- Update Proj to 6.2

* Thu Aug 29 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-2
- PostGIS 30: Use a few more macros, and also update Proj dependency to 6.1
- Add xerces-c dependency, per https://redmine.postgresql.org/issues/4672

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-1
- Update to 3.0.0 Alpha 4

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-4
- Add protobuf dependency only for RHEL 8 and Fedora, per
  https://redmine.postgresql.org/issues/4390#note-3

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-3
- Obsolete correct version. Patch from Alan Ivey

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-2
- Add protobuf-c dependency, so that related functions can be used.
  Per https://redmine.postgresql.org/issues/4390

* Wed Jun 5 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-1
- Initial cut for PostGIS 3.0.0 Alpha 2

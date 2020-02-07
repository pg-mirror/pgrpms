%global sname		pljava
%global debug_package %{nil}

Summary:	Java stored procedures, triggers, and functions for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	1.5.3
Release:	1%{?dist}
License:	BSD
URL:		http://tada.github.io/%{sname}/
Patch0:		%{sname}-pg%{pgmajorversion}-buildxml.patch

Source0:	https://github.com/tada/%{sname}/archive/V1_5_3.tar.gz
Source1:	%{sname}.pom

BuildRequires:	java-1.8.0-openjdk-devel, openssl-devel
Requires:	java-headless >= 1:1.8

%description
PL/Java is a free open-source extension for PostgreSQL™ that allows
stored procedures, triggers, and functions to be written in the Java™
language and executed in the backend.

%prep
%setup -q -n %{sname}-1_5_3
%patch0 -p0

%build
export CLASSPATH=
mvn clean install -Dso.debug=true -Psaxon-examples

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/lib
%{__cp} -f %{sname}-so/target/nar/%{sname}-so-%{version}-amd64-Linux-gpp-plugin/lib/amd64-Linux-gpp/plugin/libpljava-so-%{version}.so %{buildroot}%{pginstdir}/lib

%{__install} -d %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}/target/%{sname}-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-examples/target/%{sname}-examples-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-api/target/%{sname}-api-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--%{version}.sql
%{__cp} -f %{sname}-packaging/target/classes/%{sname}--unpackaged.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql

%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.control %{buildroot}%{pginstdir}/share/extension

%clean
%{__rm} -rf %{buildroot}

%files
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc COPYRIGHT README.md
%else
%doc README.md
%license COPYRIGHT
%endif
%{pginstdir}/lib/libpljava-so-%{version}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}--1*.sql
%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql
%{pginstdir}/share/%{sname}/%{sname}-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-examples-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-api-%{version}.jar

%changelog
* Sat Oct 5 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Create symlinks of .sql files for extension updates. Per Chapman.

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-b1_1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 20 2017 Devrim Gunduz <devrim@gunduz.org> 1.5.1-b1-1
- Update to 1.5.1 Beta 1

* Tue Mar 28 2017 Devrim Gunduz <devrim@gunduz.org> 1.5.0-2
- Fix packaging, per EnterpriseDB's spec file.

* Thu Jul 14 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Tue Feb 23 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0beta2-1
- Initial packaging for PostgreSQL RPM repository

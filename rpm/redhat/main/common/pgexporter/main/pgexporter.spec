Name:		pgexporter
Version:	0.2.0
Release:	1%{dist}
Summary:	Prometheus exporter for PostgreSQL
License:	BSD
URL:		https://github.com/%{name}/%{name}
Source0:	https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

BuildRequires:	gcc cmake3 make python3-docutils
BuildRequires:	libev libev-devel openssl openssl-devel systemd systemd-devel
Requires:	libev openssl systemd

%description
Prometheus exporter for PostgreSQL

%prep
%setup -q

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
%{__make}

%install

%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}%{_libdir}
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/etc
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__mkdir} -p %{buildroot}%{_mandir}/man5
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}

%{__install} -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
%{__install} -m 644 %{_builddir}/%{name}-%{version}/CODE_OF_CONDUCT.md %{buildroot}%{_docdir}/%{name}/CODE_OF_CONDUCT.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/ARCHITECTURE.md %{buildroot}%{_docdir}/%{name}/ARCHITECTURE.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/CLI.md %{buildroot}%{_docdir}/%{name}/CLI.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/CONFIGURATION.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/GETTING_STARTED.md %{buildroot}%{_docdir}/%{name}/GETTING_STARTED.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/RPM.md %{buildroot}%{_docdir}/%{name}/RPM.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.service %{buildroot}%{_docdir}/%{name}/etc/%{name}.service

%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}-admin.1 %{buildroot}%{_mandir}/man1/%{name}-admin.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}-cli.1 %{buildroot}%{_mandir}/man1/%{name}-cli.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}.conf.5 %{buildroot}%{_mandir}/man5/%{name}.conf.5

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name}-admin %{buildroot}%{_bindir}/%{name}-admin

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/libpgexporter.so.%{version} %{buildroot}%{_libdir}/libpgexporter.so.%{version}

chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}
chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}-cli
chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}-admin

cd %{buildroot}%{_libdir}/
%{__ln_s} -f libpgexporter.so.%{version} libpgexporter.so.0
%{__ln_s} -f libpgexporter.so.0 libpgexporter.so

%files
%license %{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/ARCHITECTURE.md
%{_docdir}/%{name}/CODE_OF_CONDUCT.md
%{_docdir}/%{name}/CLI.md
%{_docdir}/%{name}/CONFIGURATION.md
%{_docdir}/%{name}/GETTING_STARTED.md
%{_docdir}/%{name}/README.md
%{_docdir}/%{name}/RPM.md
%{_docdir}/%{name}/etc/%{name}.service
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-admin.1*
%{_mandir}/man1/%{name}-cli.1*
%{_mandir}/man5/%{name}.conf.5*
%config %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-admin
%{_libdir}/libpgexporter.so
%{_libdir}/libpgexporter.so.0
%{_libdir}/libpgexporter.so.%{version}

%changelog
* Fri Oct 22 2021 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Initial packaging for PostgreSQL RPM repository. Used upstream's
  spec file.

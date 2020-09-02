%global debug_package %{nil}
%global sname	pgbconsole

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	top-like console for Pgbouncer - PostgreSQL connection pooler
Name:		pgbconsole%{pgmajorversion}
Version:	0.1.1
Release:	2%{?dist}
License:	BSD
Source0:	https://github.com/lesovsky/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/lesovsky/%{sname}
BuildRequires:	postgresql%{pgmajorversion} ncurses-devel
BuildRequires:	libpq5-devel >= 10.0 pgdg-srpm-macros
Requires:	libpq5 >= 10.0

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
pgbConsole is the top-like console for Pgbouncer - PostgreSQL connection
pooler. Features:

 * top-like interface
 * show information about client/servers connections, pools/databases
   info and statistics.
 * ability to perform admin commands, such as pause, resume, reload and
   others.
 * ability to show log files or edit configuration in local pgbouncers.

%prep
%setup -q -n %{sname}-%{version}

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__install} -m 644 doc/*.gz %{buildroot}%{_mandir}/man1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/man1/pgbconsole.1.gz
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc README.md COPYRIGHT
%else
%doc README.md
%license COPYRIGHT
%endif

%{_bindir}/%{sname}

%changelog
* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-2
- Use our own libpq5
- Switch to pgdg-srpm-macros

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-1.1
- Rebuild against PostgreSQL 11.0

* Sun Nov 6 2016 - Devrim Gündüz <devrim@gunduz.org> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
